"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
from math import ceil
import time
import requests

import base64
from io import BytesIO
import shutil
# from questionnaire.mapper.mapper import DocList
import os 

# from fastapi.responses import FileResponse, StreamingResponse
from questionnaire.dao.Questionnaires.ResponseDb import ResponseDb
from questionnaire.dao.Questionnaires.QuestionOptionDb import QuestionOptionDb
from questionnaire.dao.Questionnaires.QuesPrincipalMappingDb import QuesPrinMappDb
from questionnaire.dao.Questionnaires.PrincipalGuidanceDb import PrincipalGuidanceDb
from questionnaire.dao.Questionnaires.SubDimensionDb import SubDimensionDb
from questionnaire.dao.Questionnaires.DimensionDb import DimensionDb
from questionnaire.dao.Questionnaires.QuestionDb import QuestionDb
from questionnaire.dao.Questionnaires.ImpactDb import ImpactDb
# from questionnaire.mapper.Questionnaires.mapper import DimensionResponse, PrincipalGuidanceResponse, QuestionOptionResponse, QuestionResponse, QusPrincipalMappingResponse, SubDimensionResponse, SubmissionResponse
from questionnaire.mapper.Questionnaires.mapper import  SubmissionResponse
# from questionnaire.dao.DocProccessDb import docDb
from questionnaire.dao.fileStoreDb import fileStoreDb as fileDb
from questionnaire.config.logger import request_id_var
from questionnaire.dao.ExceptionDb import ExceptionDb
from questionnaire.config.logger import CustomLogger
log = CustomLogger()
from questionnaire.dao.Questionnaires.UseCaseDetailDb import *

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Questionnaires:

    # def addDimension(payload) ->DimensionResponse:

    #     print("payload Inside addDimesnion===",payload)
    #     payload = AttributeDict(payload)
    #     dimensionDtl = DimensionDb.findall({"DimensionName":payload.dimensionName})

    #     if(len(dimensionDtl) > 0):
    #         return "Dimension Already Exists"
    #     else:
    #         dimensionCreatedData = DimensionDb.create({"dID":payload.dimensionID,"DimensionName":payload.dimensionName,"DimensionDesc":payload.dimensionDesc})

    #         dimdtl = DimensionDb.findall({"Id":dimensionCreatedData})[0]
    #         print("DimensionDtlCreated===",dimdtl)
    #         obj = DimensionResponse
    #         res = [dimdtl]
    #         obj.result = res
    #         print("onj==",obj.result)

    
    #     return obj
    


    # def addSubDimension(payload) ->SubDimensionResponse:

    #     print("payload Inside addDimesnion===",payload)
    #     payload = AttributeDict(payload)
    #     dimensionDtl = SubDimensionDb.findall({"SubDimensionName":payload.subDimensionName})
    #     if(len(dimensionDtl) > 0):
    #         return "SubDimension Already Exists"
    #     else:
    #         SubdimensionCreatedData = SubDimensionDb.create({"dID":payload.dimensionId,"SDId":payload.subDimensionId,"SubDimName":payload.subDimensionName,"SubDimDesc":payload.subDimensionDesc})

    #         dimdtl = SubDimensionDb.findall({"Id":SubdimensionCreatedData})[0]
    #         print("DimensionDtlCreated===",dimdtl)
    #         obj = SubDimensionResponse
    #         res = [dimdtl]
    #         obj.result = res
    #         print("onj==",obj.result)
        
    #     # obj="Successs"
    #     return obj
    



    # def addQuestion(payload) -> QuestionResponse:
    #     print("payload Inside addDimesnion===",payload)
    #     payload = AttributeDict(payload)


    #     questionDtl = QuestionDb.create({"QuestionId":payload.questionId,"SubDimenrsionId":payload.subDimenrsionId,"QuestionDesc":payload.questionDesc,"QuestionType":payload.questionType,
    #                                      "RiskClassification":payload.riskClassification,"isPIIData":payload.isPIIData,"Question_Weightage":payload.Question_Weightage})
        
    #     print(questionDtl)
    #     dimdtl = QuestionDb.findall({"Id":questionDtl})[0]
    #     print("DimensionDtlCreated===",dimdtl)
    #     obj = QuestionResponse
    #     res = [dimdtl]
    #     obj.result = res
    #     print("res====",obj.result)

    #     # obj=3
    #     return obj
    


    # def addPrincipalGuidance(payload) ->PrincipalGuidanceResponse:
        
    #     payload = AttributeDict(payload)
    #     pringuiData = PrincipalGuidanceDb.create({"PrincipalGuidanceId":payload.PrincipalGuidanceId,"PrincipalKey":payload.PrincipalKey})

    #     print("pricguid==",pringuiData)

    #     pgdtl = PrincipalGuidanceDb.findall({"Id":pringuiData})[0]
    #     obj = PrincipalGuidanceResponse
    #     res= [pgdtl]
    #     obj.result = res

    #     return obj
    

    # def addQusPrincipalMapping(payload) ->QusPrincipalMappingResponse:
    #     payload = AttributeDict(payload)

    #     qusPrinData = QuesPrinMappDb.create({"QuestionId":payload.QuestionId,"PrincipalGuidanceId":payload.PrincipalGuidanceId,"PrincipalValues":payload.PrincipalValues})

    #     print("QstPrinMapp====",qusPrinData)

    #     qusdtl = QuesPrinMappDb.findall({"Id":qusPrinData})[0]

    #     obj = QusPrincipalMappingResponse
    #     res= [qusdtl]
    #     obj.result = res

    #     return obj
    

    # def addQuestionOption(payload) ->QuestionOptionResponse:

    #     payload = AttributeDict(payload)
        

    #     questOption = QuestionOptionDb.create({"QuestionId":payload.QuestionId,"OptionsValue":payload.OptionsValue,
    #                                            "MaxScore":payload.MaxScore,"MinScore":payload.MinScore})
        
    #     print("QuestionOptionvalue==",questOption)

    #     qoptionDtl = QuestionOptionDb.findall({"Id":questOption})[0]

    #     obj = QuestionOptionResponse
    #     res= [qoptionDtl]
    #     obj.result = res

    #     return obj
    

    def createImpact(payload):
        """
        Creates or updates an impact entry in the database based on the provided payload.
        Args:
            payload (object): An object containing the following attributes:
                - Dimension (str): The dimension associated with the impact.
                - Impact (str): The name or type of the impact.
                - MinScore (int): The minimum score for the impact.
                - MaxScore (int): The maximum score for the impact.
        Returns:
            dict: A dictionary containing:
                - "id" (str): The ID of the created or updated impact entry.
                - "status" (str): A string indicating whether the entry was "Created" or "Updated".
        """
        
        impValue=ImpactDb.findall({"Dimension":payload.Dimension,"Impact":payload.Impact})
        res={}
        if(len(impValue)>0):
            res["id"]=ImpactDb.update(impValue[0]._id,{"MinScore":payload.MinScore,"MaxScore":payload.MaxScore})
            res["status"]="Updated"
        else:
            res["id"]=ImpactDb.create(payload)
            res["status"]="Created"
        return res
    
    
    
    
    def getQuestionnaries():
        """
        Retrieves a hierarchical structure of questionnaires, including dimensions, sub-dimensions, 
        questions, and their associated options.
        The function fetches data from multiple database collections:
        - Dimensions
        - Sub-dimensions (linked to dimensions)
        - Questions (linked to sub-dimensions)
        - Options (linked to questions)
        Returns:
            list: A list of dimensions, where each dimension contains its sub-dimensions, 
                  each sub-dimension contains its questions, and each question contains its options.
        Raises:
            Exception: Logs the error details and raises an exception if any error occurs during 
                       the data retrieval process. The error details include the exception type, 
                       message, and the line number where the error occurred.
        """
        
        try:
            dimensionDetails = DimensionDb.findall({})
            # result=[]
            # print("dimensionDetails===",dimensionDetails)
            # res=[]
            # dict1["Dimesnion"]=subDimensionDetails
            for i in dimensionDetails:
                subDimensionDetails = SubDimensionDb.findall({"DimensionId":i.DimensionId})
                i["SubDimesnion"]=subDimensionDetails
                # print("SubDimensionDetails====",subDimensionDetails)
                # res1=[]
                for j  in i["SubDimesnion"]:
                    questionDetails = QuestionDb.findall({"SubDimenrsionId":j.SubDimensionId})
                    j["QuestionDetails"]=questionDetails
                    # res2=[]
                    for k in j["QuestionDetails"]:
                        # op = QuestionOptionDb.mycol.distinct( "OptionsValue", {"QuestionId":k.QuestionId})
                        op = QuestionOptionDb.findall({"QuestionId":k.QuestionId})
                        k["OptionsDetail"]=op
            # print("dimensionDetails",dimensionDetails)
            # print("Result111111====",result[2])
            return dimensionDetails
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getQuestionnariesFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)


    def addResponseDetail(payload) :
        
        """
            Adds or updates response details in the database based on the provided payload.
            Args:
                payload (dict): A dictionary containing the following keys:
                    - UserId (str): The ID of the user.
                    - UseCaseName (str): The name of the use case.
                    - QuestionId (str): The ID of the question.
                    - QuestionOptionId (str): The ID of the selected question option.
                    - ResponseDesc (str): The description of the response.
            Returns:
                str: A message indicating whether the response was added or updated successfully.
            Raises:
                Exception: If an error occurs during the execution, it logs the error details
                           and raises the exception.
            Notes:
                - If no existing response is found for the given question, user, and use case,
                  a new response is created.
                - If an existing response is found, it is updated with the new details.
                - Logs the execution time for creating a new response.
                - Logs errors with details such as the line number and traceback frame.
            """
        
        try:
#             def addResponseDetail(payload) :
            payload = AttributeDict(payload)
            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
            resDtlData = ResponseDb.findall({"QuestionId":payload.QuestionId,"UserId":payload.UserId,"UseCaseNameID":useCaseDtl[0]._id})
            log.debug("resDtlData===="+str(resDtlData))
            # value = {"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc}
            value = {"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc}
            response=""
            # 
            # RAI_Risk_Index
            # Q_Weightage
            if(len(resDtlData) == 0):
                
                s = time.time()
                responseDtl = ResponseDb.create({"QuestionId":payload.QuestionId,"UseCaseNameID":useCaseDtl[0]._id,"UserId":payload.UserId,"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc})
                
                e = time.time()
                time.sleep(1/1000)
    
                log.debug("toatal time=="+str(e-s))
                response= "Response Added Successfully..."
            else:
                # value = {"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc,"Q_Weightage":payload.Q_Weightage,"RAI_Risk_Index":payload.RAI_Risk_Index}
                data = resDtlData[0]
                
                responseUpdateDtl = ResponseDb.update(data["_id"],value)
                time.sleep(1/1000)
                
                # print("responseUpdateDtl",responseUpdateDtl)
                response = "Response Updated Successfully..."
            # print("responseDtl===",responseDtl)
            # time.sleep(1/1000)
    
            # resDtl = ResponseDb.findall({"Id":responseDtl})[0]
            # print("Result===",resDtl)
    
            # res= [resDtl]
    
            # obj = SubmissionResponse
            # obj.result = res

            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"addResponseDetailFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
    

    def addMultipleResponse(payload) : 
                                                                                                                    
        try:
#             def addResponseDetail(payload) :
            for i in payload:

                # payload = AttributeDict(i)
                payload = json.loads(i)
                # print("pauload of i=====",payload)
                useCaseDtl = UseCaseNameDb.findall({"UserId":payload["UserId"],"UseCaseName":payload["UseCaseName"]})
                log.debug("useCaseDtl of i====="+str(useCaseDtl))
                resDtlData = ResponseDb.findall({"QuestionId":payload["QuestionId"],"UserId":payload["UserId"],"UseCaseNameID":useCaseDtl[0]._id})
                log.debug("resDtlData===="+str(resDtlData))
                # value = {"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc}
                value = {"QuestionOptionId":payload["QuestionOptionId"],"ResponseDesc":payload["ResponseDesc"]}
                response=""
                # 
                # RAI_Risk_Index
                # Q_Weightage
                if(len(resDtlData) == 0):
                    
                    s = time.time()
                    responseDtl = ResponseDb.create({"QuestionId":payload["QuestionId"],"UseCaseNameID":useCaseDtl[0]._id,"UserId":payload["UserId"],"QuestionOptionId":payload["QuestionOptionId"],"ResponseDesc":payload["ResponseDesc"]})
                    
                    e = time.time()
                    time.sleep(1/1000)
        
                    log.debug("toatal time=="+str(e-s))
                    response= "Response Added Successfully..."
                else:
                    # value = {"QuestionOptionId":payload.QuestionOptionId,"ResponseDesc":payload.ResponseDesc,"Q_Weightage":payload.Q_Weightage,"RAI_Risk_Index":payload.RAI_Risk_Index}
                    data = resDtlData[0]
                    
                    responseUpdateDtl = ResponseDb.update(data["_id"],value)
                    time.sleep(1/1000)
                    
                    # print("responseUpdateDtl",responseUpdateDtl)
                    response = "Response Updated Successfully..."
                # print("responseDtl===",responseDtl)
                # time.sleep(1/1000)
        
                # resDtl = ResponseDb.findall({"Id":responseDtl})[0]
                # print("Result===",resDtl)
        
                # res= [resDtl]
        
            # obj = SubmissionResponse
            # obj.result = res
            
            data = Questionnaires.getriskDashboardDetails(payload["UserId"],payload["UseCaseName"])
            print("value of x========",data)
            for item in data:
                if item['DimensionName'] == 'Total':
                    total_risk_index = item['riskIndex']
                    total_classification = item['classification']
                    break
            UseCaseNameDb.update({"UserId":payload["UserId"],"UseCaseName":payload["UseCaseName"]},{"Score":total_risk_index,"Risk_Classification":total_classification})
            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"addResponseDetailFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
    


    def classification(dimName,score):
        """
        Classifies a given score into an impact category based on the specified dimension.
        Args:
            dimName (str): The name of the dimension to classify the score under.
            score (float): The score to be classified.
        Returns:
            str: The impact category corresponding to the given score and dimension.
        Raises:
            IndexError: If no matching impact category is found in the database.
        Notes:
            - This function queries the `ImpactDb` database to find an entry where:
              - The dimension matches `dimName`.
              - The score is within the range defined by `MinScore` and `MaxScore`.
            - The function assumes that the query will return at least one result.
        """
        
        
        result=ImpactDb.findall({"Dimension":dimName,"MinScore":{'$lte':score},"MaxScore":{'$gte':score}})
        result=result[0]["Impact"]
        print(result)
        return result
    

    def getriskDashboardDetails(userId:str,useCaseName):
        
        """
            Retrieves risk dashboard details for a specific user and use case.
            Args:
                userId (str): The unique identifier of the user.
                useCaseName (str): The name of the use case.
            Returns:
                list: A list of dictionaries containing dimension-wise and total risk details.
                      Each dictionary includes:
                      - DimensionName (str): The name of the dimension.
                      - totalQuestion (int): The total number of questions in the dimension.
                      - weightage (int): The total weightage of the questions in the dimension.
                      - riskIndex (int): The calculated risk index for the dimension.
                      - classification (str): The risk classification (e.g., "Unacceptable").
                      If no records are found, returns a string: "No Record Found...".
            Raises:
                Exception: If an error occurs during execution, logs the error details and raises the exception.
            """
        
        # UserId
        try:
            riskClassificationFlag=False
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
            responseDetails = ResponseDb.findall({"UserId":userId,"UseCaseNameID":useCaseDtl[0]._id})


            if(len(responseDetails) == 0):
                return "No Record Found..."
            dimensionDetails = DimensionDb.findall({})
            res=[]
            totalQues= 0
            totalWeightage=0
            totalRisk = 0
            
            for i in dimensionDetails:
                l =0
                w=0
                r=0
                subDimensionDetails = SubDimensionDb.findall({"DimensionId":i.DimensionId})
                i["SubDimesnion"]=subDimensionDetails
    
                for j  in i["SubDimesnion"]:
                    
                    questionDetails = QuestionDb.findall({"SubDimenrsionId":j.SubDimensionId})
                    j["QuestionDetails"]=questionDetails
                    # print("No of Questions===",len(questionDetails))
                    l=l+len(questionDetails)
                    totalQues = totalQues + len(questionDetails)
    
                    for k in j["QuestionDetails"]:
                        
                        # op = QuestionOptionDb.mycol.distinct( "OptionsValue", {"QuestionId":k.QuestionId})
                        op = ResponseDb.findall({"QuestionId":k.QuestionId,"UserId":userId,"UseCaseNameID":useCaseDtl[0]._id})
                        wi = QuestionDb.findall({"QuestionId":k.QuestionId})
                    # print("wiii=========",wi)
                        w=w+ wi[0].Question_Weightage
                    # totalWeightage = totalWeightage + k["Question_Weightage"]
                        totalWeightage = totalWeightage + wi[0].Question_Weightage
                        # w=w+ k["Question_Weightage"]
                        # totalWeightage = totalWeightage + k["Question_Weightage"]
                        for m in op:
                            raiI = QuestionOptionDb.findall({"_id":m["QuestionOptionId"]})
                        # print("rai=======",raiI)
                            r=r+ raiI[0].ImpactIndexScore
                            totalRisk = totalRisk + raiI[0].ImpactIndexScore
                            # r=r+ m["RAI_Risk_Index"]
                            # totalRisk = totalRisk + m["RAI_Risk_Index"]
                            # print("m=============",m)
    
                # print("\n\n",i["DimensionName"],"has ",l , " no of questions","and it's weithage is ",w,"and has rai risk index value ,",r,"\n\n")
                imapctClass = Questionnaires.classification(i["DimensionName"],r)
                if(imapctClass == "Unacceptable"):
                    riskClassificationFlag=True
                dic = {"DimensionName":i["DimensionName"],"totalQuestion":l,"weightage":ceil(w),"riskIndex":r,"classification":imapctClass}
                res.append(dic)
            log.debug("value 0f l,w,r===="+str(l)+str(w)+str(r))
            if riskClassificationFlag == True:
                classification = "Unacceptable"
            else:
                classification = Questionnaires.classification("Total",totalRisk)
            res.append({"DimensionName":"Total","totalQuestion":totalQues,"weightage":ceil(totalWeightage),"riskIndex":totalRisk,"classification":classification})
    
            # print("Res=====",res)
            return res
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getriskDashboardDetailsFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)

    # def getResetQuestionnaries(userId,useCaseName):
    #     # print("dimensionDetails===",dimensionDetails)
    #     dimensionDetails = DimensionDb.findall({})
    #     res=[]
        
    #     # dict1["Dimesnion"]=subDimensionDetails
    #     for i in dimensionDetails:
            
            
    #         subDimensionDetails = SubDimensionDb.findall({"DimensionId":i.DimensionId})
    #         i["SubDimesnion"]=subDimensionDetails
    #         # print("SubDimensionDetails====",subDimensionDetails)
            
    #         res1=[]
    #         for j  in i["SubDimesnion"]:
                
    #             questionDetails = QuestionDb.findall({"SubDimenrsionId":j.SubDimensionId})
    #             j["QuestionDetails"]=questionDetails

    #             # responseDetails = ResponseDb.findall({})
                
                
               
    #             res2=[]
                
    #             for k in j["QuestionDetails"]:
                    
    #                 # op = QuestionOptionDb.mycol.distinct( "OptionsValue", {"QuestionId":k.QuestionId})
    #                 op = QuestionOptionDb.findall({"QuestionId":k.QuestionId})
                    
    #                 k["OptionsDetail"]=op
    #                 useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
    #                 responseDetails = ResponseDb.findall({"UserId":userId,"QuestionId":k.QuestionId,"UseCaseNameID":useCaseDtl[0]._id})
    #                 # responseDetails = ResponseDb.findall({"UserId":userId})

    #                 # print("responseDetails386====",responseDetails[0])
    #                 if(len(responseDetails) != 0):
    #                     k["Selected_Option"]=responseDetails[0].QuestionOptionId
    #                 else:
    #                     k["Selected_Option"]=0.0

    #                 # print("k=========",k)


                    





    def getResetQuestionnaries(userId,useCaseName):
        
        """
            Retrieves and resets the questionnaire data for a specific user and use case.
            This function fetches all dimensions, their associated sub-dimensions, 
            questions, and options from the database. It also retrieves the user's 
            responses for the specified use case and marks the selected options for 
            each question.
            Args:
                userId (str): The unique identifier of the user.
                useCaseName (str): The name of the use case for which the questionnaire 
                                   data is being retrieved.
            Returns:
                list: A list of dimensions, each containing sub-dimensions, questions, 
                      and their associated options and user responses.
            Raises:
                Exception: If any error occurs during the execution, it logs the error 
                           details and raises the exception.
            Database Collections Accessed:
                - DimensionDb: To fetch all dimensions.
                - SubDimensionDb: To fetch sub-dimensions for each dimension.
                - QuestionDb: To fetch questions for each sub-dimension.
                - QuestionOptionDb: To fetch options for each question.
                - UseCaseNameDb: To fetch the use case details for the user.
                - ResponseDb: To fetch the user's responses for the questions.
                - ExceptionDb: To log exceptions in case of errors.
            Notes:
                - If a response exists for a question, the "Selected_Option" field is 
                  populated with the corresponding option ID. Otherwise, it is set to 0.0.
                - Logs errors with details such as the exception message, line number, 
                  and traceback frame in case of failures.
            """
        
        try:
            dimensionDetails = DimensionDb.findall({})
            # result=[]
            # print("dimensionDetails===",dimensionDetails)
            # res=[]
            # dict1["Dimesnion"]=subDimensionDetails
            for i in dimensionDetails:
            
            
                subDimensionDetails = SubDimensionDb.findall({"DimensionId":i.DimensionId})
                i["SubDimesnion"]=subDimensionDetails
                # print("SubDimensionDetails====",subDimensionDetails)
  
                res1=[]
                for j  in i["SubDimesnion"]:
  
                    questionDetails = QuestionDb.findall({"SubDimenrsionId":j.SubDimensionId})
                    j["QuestionDetails"]=questionDetails

                    # responseDetails = ResponseDb.findall({})
  
  
  
                    res2=[]
  
                    for k in j["QuestionDetails"]:
  
                        # op = QuestionOptionDb.mycol.distinct( "OptionsValue", {"QuestionId":k.QuestionId})
                        op = QuestionOptionDb.findall({"QuestionId":k.QuestionId})
  
                        k["OptionsDetail"]=op
                        useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
                        responseDetails = ResponseDb.findall({"UserId":userId,"QuestionId":k.QuestionId,"UseCaseNameID":useCaseDtl[0]._id})
                        # responseDetails = ResponseDb.findall({"UserId":userId})

                        # print("responseDetails386====",responseDetails[0])
                        if(len(responseDetails) != 0):
                            k["Selected_Option"]=responseDetails[0].QuestionOptionId
                        else:
                            k["Selected_Option"]=0.0
            return dimensionDetails
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getResetQuestionnariesFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)


