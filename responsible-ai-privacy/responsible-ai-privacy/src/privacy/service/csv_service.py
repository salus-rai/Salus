"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import pandas as pd
import io
import logging
import tempfile
from presidio_analyzer import AnalyzerEngine, BatchAnalyzerEngine, DictAnalyzerResult
from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine
from privacy.service.imagePrivacy import AttributeDict, ImagePrivacy
from privacy.service.api_req import ApiCall
from privacy.config.logger import request_id_var

from privacy.service.__init__ import *
from privacy.util.special_recognizers.DataListRecognizer import DataListRecognizer
from privacy.util.special_recognizers.fakeData import FakeDataGenerate
from privacy.util.special_recognizers.fakeDataCSV import *




log = logging.getLogger(__name__)

class CSVService:
    @staticmethod
    def csv_anonymize(payload):
        """
        Anonymizes the data in a CSV file based on the provided payload.

        Args:
            payload (dict): The payload containing the necessary information for anonymization.

        Returns:
            io.StringIO: The anonymized CSV data as a StringIO object.

        Raises:
            Exception: If an error occurs during the anonymization process.
        """
        try:
            
            payload = AttributeDict(payload)
            analyzer,imageAnalyzerEngine,imageRedactorEngine,imagePiiVerifyEngine,encryptImageEngin=selectNlp(payload.nlp)
            if(payload.portfolio!=None or payload.account!=None):
                response_value=ApiCall.request(AttributeDict({"portfolio":payload.portfolio,"account":payload.account}))
                if(response_value==None):
                        return None
                
             
            file = payload["file"]
            keys_to_skip = payload["keys_to_skip"]
            piiEntitiesToBeRedacted=[]
            if payload["piiEntitiesToBeRedacted"] is not None:
               piiEntitiesToBeRedacted=payload["piiEntitiesToBeRedacted"].split(',')
             

            accName=None
            if(payload.portfolio!=None):
                accName=AttributeDict({"portfolio":payload.portfolio,"account":payload.account})
            nlp=payload["nlp"]
            exclusion=payload.exclusion.split(',') if payload.exclusion != None else []
             
            spRecog=None
            if(nlp=="roberta"):
                spRecog=[roberta_recog]
            if(nlp=="ranha"):
                # registry.add_recognizer(ranha_recog)
                if(piiEntitiesToBeRedacted==None and  accName==None):
                    piiEntitiesToBeRedacted=list(set(ranha_recog.supported_entities+registry.get_supported_entities()))
                spRecog=[ranha_recog]

            # Initialize the analyzer and anonymizer engines
            

            # analyzer = AnalyzerEngine()

            

            batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
            batch_anonymizer = BatchAnonymizerEngine()
            
            
            
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file.file,encoding='utf-8', encoding_errors='ignore')
            log.debug("Original DataFrame: " + str(df))
            
            # Convert DataFrame to dictionary
            dff = df.to_dict(orient="list")
            log.debug("CSV to dict: " + str(dff))
             
             
            # Analyze the data
            analyzer_results = []
            if(accName==None):
                
                if(piiEntitiesToBeRedacted == None):
                    analyzer_results = batch_analyzer.analyze_dict(dff, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,return_decision_process = True,score_threshold=payload.scoreThreshold if payload.scoreThreshold is not None else 0,ad_hoc_recognizers=spRecog)
                else:
                    try:
                        analyzer_results = batch_analyzer.analyze_dict(dff, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=piiEntitiesToBeRedacted,return_decision_process = True,score_threshold=payload.scoreThreshold if payload.scoreThreshold != None else 0,ad_hoc_recognizers=spRecog)
                    except Exception as e:
                        log.error(str(e))
                        raise e
            else:
                preEntity=[]
                dataistEnt = []
                
                response_value = ApiCall.request(accName)
                if response_value == None:
                        return None
                if(response_value==404):
                        
                        return response_value
                
                entityType,datalist,preEntity=response_value
                
                for d in range(len(datalist)):
                    record=ApiCall.getRecord(entityType[d])
                    record=AttributeDict(record)
                    log.debug("Record====="+str(record))

                        # predefined_recognizers.data_recognizer.DataList.entity.clear()
                        # predefined_recognizers.data_recognizer.DataList.resetData()
                    if(record.RecogType=="Data"):
                                
                            dataRecog=(DataListRecognizer(terms=datalist[d],entitie=[entityType[d]]))
                            registry.add_recognizer(dataRecog)
                                # predefined_recognizers.data_recognizer.DataList.entity.append(entityType[d])
                                # predefined_recognizers.data_recognizer.DataList.setData(datalist[d])
                                 
                                
                            update_session_dict(entityType[d], datalist[d])
                            data = {entityType[d]: datalist[d]}
                            dataistEnt.append(data)
                    
                    elif(record.RecogType=="Pattern" and record.isPreDefined=="No"):
                            contextObj=record.Context.split(',')
                            pattern="|".join(datalist[d])
                             
                            log.debug("pattern="+str(pattern))
                            patternObj = Pattern(name=entityType[d],
                                                        regex=pattern,
                                                        score=record.Score)
                            patternRecog = PatternRecognizer(supported_entity=entityType[d],
                                                                    patterns=[patternObj],context=contextObj)
                            registry.add_recognizer(patternRecog)  
                                            

                analyzer_results=batch_analyzer.analyze_dict(dff,language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=entityType+preEntity,score_threshold=admin_par[request_id_var.get()]["scoreTreshold"],return_decision_process = True,ad_hoc_recognizers=spRecog)
                log.debug("Analyzer results: " + str(analyzer_results))


            
            # print("analyzer_results====",analyzer_results)
            # print("dff====",dff)

             

            dfs=list(analyzer_results)
            
            dict_operators = {} 
            # print("======",dfs)
            # omm
            if payload.fakeData == True:
                fake_dict_operator,dfs = FakeDataCSVGenerate.fakeDataGeneration(dfs,list(dff))
                dict_operators.update(fake_dict_operator)
            # print("fake_dict_operator===",fake_dict_operator)
                # print( "Fake Data Generated DataFrame: " + str(df1))
           
            anonymizer_results = batch_anonymizer.anonymize_dict(dfs, operators=dict_operators)   #
            log.debug("Anonymizer results: " + str(anonymizer_results))

            # Convert the anonymized data back to a DataFrame
            anonymized_df = pd.DataFrame(anonymizer_results)
            log.debug("Anonymized DataFrame: " + str(anonymized_df))

            # Convert the DataFrame to CSV
            output = io.StringIO()
            anonymized_df.to_csv(output, index=False)
            output.seek(0)

            # Save the CSV to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(output.getvalue().encode())
                temp_file_path = temp_file.name

            log.debug("Returning from csv_anonymize function")
            return output
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            raise e