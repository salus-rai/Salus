"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
import logging
import tempfile
from presidio_analyzer import AnalyzerEngine, BatchAnalyzerEngine
from presidio_anonymizer import BatchAnonymizerEngine
from privacy.service.imagePrivacy import AttributeDict, ImagePrivacy
from privacy.service.api_req import ApiCall
from privacy.service.__init__ import *
from privacy.util.special_recognizers.DataListRecognizer import DataListRecognizer
from privacy.config.logger import request_id_var

log = logging.getLogger(__name__)

class JSONService:
    @staticmethod
    def anonymize_json(payload):
        """
        Anonymizes the given JSON payload by redacting specified PII entities and skipping specified keys.

        Args:
            payload (dict): The JSON payload to be anonymized.

        Returns:
            str: The anonymized JSON as a string.

        Raises:
            ValueError: If the data type of the payload is not supported.
            Exception: If an error occurs during the anonymization process.
        """
        try:
            log.debug("Entering anonymize_json function")

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
            scoreThreshold=0
            if payload["scoreThreshold"] is not None:
                 scoreThreshold=payload["scoreThreshold"]
                 
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
            # language = payload["language"]
             

            # Read the JSON file into a dictionary or list
            data = json.load(file.file)
            log.debug("Original JSON: " + str(data))

            # Initialize the analyzer and anonymizer engines
            
            batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
            batch_anonymizer = BatchAnonymizerEngine()

            # Process the input dynamically based on its type
            if isinstance(data, dict):
                anonymized_data = JSONService.process_dict(data, batch_analyzer, batch_anonymizer, "en", keys_to_skip,accName,exclusion,piiEntitiesToBeRedacted,scoreThreshold,spRecog)
            elif isinstance(data, list):
                anonymized_data = JSONService.process_list(data, batch_analyzer, batch_anonymizer, "en", keys_to_skip,accName,exclusion,piiEntitiesToBeRedacted,scoreThreshold,spRecog)
            else:
                raise ValueError("Unsupported data type")

            # Convert the anonymized data to JSON with indentation
            anonymized_json = json.dumps(anonymized_data, indent=3)
            log.debug("Anonymized JSON: " + anonymized_json)

            # Save the JSON to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
                temp_file.write(anonymized_json.encode())
                temp_file_path = temp_file.name

            log.debug("Returning from anonymize_json function")
            return anonymized_json
        except Exception as e:
            log.error(str(e))
            raise e

    @staticmethod
    def process_dict(data, batch_analyzer, batch_anonymizer, language, keys_to_skip,accName,exclusion,piiEntitiesToBeRedacted,scoreThreshold,spRecog):
        """
        Process a dictionary of data by analyzing and anonymizing its values.

        Args:
            data (dict): The dictionary of data to be processed.
            batch_analyzer (BatchAnalyzer): The batch analyzer object used to analyze the data.
            batch_anonymizer (BatchAnonymizer): The batch anonymizer object used to anonymize the data.
            language (str): The language used for analysis.
            keys_to_skip (list): The list of keys to skip during analysis.
            accName (str): The account name for API call.
            exclusion (list): The list of keys to exclude from analysis.
            piiEntitiesToBeRedacted (list): The list of PII entities to be redacted.
            scoreThreshold (float): The score threshold for analysis.
            spRecog (list): The list of ad hoc recognizers for analysis.

        Returns:
            dict: The processed dictionary with anonymized values.
        """
        anonymized_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                anonymized_list = []
                for item in value:
                    if isinstance(item, dict):
                        # Flatten the nested structure
                        flattened_item = JSONService.flatten_json(item)
                        # Analyze the data
                        analyzer_results = []
                        if(accName==None):
                            if(piiEntitiesToBeRedacted == None):
                                analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,return_decision_process = True,score_threshold=scoreThreshold,ad_hoc_recognizers=spRecog)
                            else:
                                try:
                                    analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=piiEntitiesToBeRedacted,return_decision_process = True,score_threshold=scoreThreshold,ad_hoc_recognizers=spRecog)
                                except Exception as e:
                                        log.error(str(e))
                                        raise e
                        
                        # analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip)
                        # log.debug("Analyzer results: " + str(analyzer_results))

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
                        # Anonymize the data
                            analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=entityType+preEntity,score_threshold=admin_par[request_id_var.get()]["scoreTreshold"],ad_hoc_recognizers=spRecog)

                        anonymizer_results = batch_anonymizer.anonymize_dict(analyzer_results)
                        log.debug("Anonymizer results: " + str(anonymizer_results))

                        anonymized_list.append(anonymizer_results)
                    else:
                        anonymized_list.append(item)
                anonymized_data[key] = anonymized_list
            else:
                anonymized_data[key] = value
        return anonymized_data

    @staticmethod
    def process_list(data, batch_analyzer, batch_anonymizer, language, keys_to_skip,accName,exclusion,piiEntitiesToBeRedacted,scoreThreshold,spRecog):
        """
        Process a list of data items by analyzing and anonymizing them.

        Args:
            data (list): The list of data items to be processed.
            batch_analyzer (BatchAnalyzer): The batch analyzer object used for analyzing the data.
            batch_anonymizer (BatchAnonymizer): The batch anonymizer object used for anonymizing the data.
            language (str): The language of the data items.
            keys_to_skip (list): The list of keys to skip during analysis.
            accName (str): The account name.
            exclusion (list): The list of terms to be excluded from analysis.
            piiEntitiesToBeRedacted (list): The list of PII entities to be redacted.
            scoreThreshold (float): The score threshold for decision making during analysis.
            spRecog (list): The list of ad hoc recognizers.

        Returns:
            list: The list of anonymized data items.
        """        
        anonymized_list = []
        for item in data:
            if isinstance(item, dict):
                # Flatten the nested structure
                flattened_item = JSONService.flatten_json(item)
                        # Analyze the data
                analyzer_results = []
                if(accName==None):
                    if(piiEntitiesToBeRedacted == None):
                        analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,return_decision_process = True,score_threshold=scoreThreshold,ad_hoc_recognizers=spRecog)
                    else:
                        try:
                            analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=piiEntitiesToBeRedacted,return_decision_process = True,score_threshold=scoreThreshold,ad_hoc_recognizers=spRecog)
                        except Exception as e:
                                log.error(str(e))
                                raise e
                
                # analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip)
                # log.debug("Analyzer results: " + str(analyzer_results))

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
                # Anonymize the data
                    analyzer_results = batch_analyzer.analyze_dict(flattened_item, language="en", keys_to_skip=keys_to_skip,allow_list=exclusion,entities=entityType+preEntity,score_threshold=admin_par[request_id_var.get()]["scoreTreshold"],ad_hoc_recognizers=spRecog)

                anonymizer_results = batch_anonymizer.anonymize_dict(analyzer_results)
                log.debug("Anonymizer results: " + str(anonymizer_results))

                anonymized_list.append(anonymizer_results)
                 
            else:
                anonymized_list.append(item)
        return anonymized_list

    @staticmethod
    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    @staticmethod
    def reconstruct_json(flattened_json):
        if isinstance(flattened_json, list):
            return [JSONService.reconstruct_json(item) if isinstance(item, dict) else item for item in flattened_json]
        reconstructed = {}
        for key, value in flattened_json.items():
            parts = key.split('_')
            current = reconstructed
            for part in parts[:-1]:
                if part.isdigit():
                    part = int(part)
                    if not isinstance(current, list):
                        current = []
                    while len(current) <= part:
                        current.append({})
                    current = current[part]
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
            current[parts[-1]] = value
        return reconstructed