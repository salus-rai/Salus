"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime
from questionnaire.dao.Questionnaires.AiCanvasDb import AICanvasDb
from questionnaire.mapper.Questionnaires.canvasMapper import *
from questionnaire.mapper.Questionnaires.aiCanvasMapper import *
from questionnaire.dao.Questionnaires.UseCaseDetailDb import *
from questionnaire.dao.ExceptionDb import ExceptionDb
from questionnaire.config.logger import request_id_var

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class AICanvasContent:
    def addAICanvasResponse(payload):
        """
        Adds or updates an AI Canvas response in the database.
        This function processes the provided payload to either create a new AI Canvas 
        response entry or update an existing one in the database. It handles exceptions 
        and logs errors if any issues occur during the operation.
        Args:
            payload (dict): A dictionary containing the following keys:
                - UserId (str): The ID of the user.
                - UseCaseName (str): The name of the use case.
                - AICanvasResponse (dict): The AI Canvas response data.
        Returns:
            str: A message indicating whether the operation was successful:
                - "Added Successfully" if a new entry was created.
                - "Updated Successfully..." if an existing entry was updated.
        Raises:
            Exception: If an error occurs during the operation, it logs the error details 
            and raises the exception.
        Notes:
            - The function uses `AttributeDict` to convert the payload into an object-like 
              structure for easier access.
            - It interacts with two database collections: `UseCaseNameDb` and `AICanvasDb`.
            - Error details are logged and stored in the `ExceptionDb` collection for 
              debugging purposes.
        """
        
        try:
            payload = AttributeDict(payload)

            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
            res = AICanvasDb.findall({"UserId":payload.UserId,"useCaseNameId":useCaseDtl[0]._id})
            # print("payload16====",payload)
            log.debug("payload===="+str(payload))
            value = {"AICanvasResponse":payload.AICanvasResponse.dict(),"LastUpdatedDateTime": datetime.datetime.now()}
            response =""
            if(len(res) == 0):
                # useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
                # print("us3eCase dteails====",useCaseDtl)
                log.debug("useCaseDtl===="+str(useCaseDtl))
                responseDtl = AICanvasDb.create({"useCaseNameId":useCaseDtl[0]._id,"UserId":payload.UserId,"AICanvasResponse":payload.AICanvasResponse})
                # print("ResponseDtl23=====",responseDtl)
                log.debug("ResponseDtl===="+str(responseDtl))
                response="Added Successfully"
            else:
                data = res[0]
                responseUpdateDtl = AICanvasDb.update(data["_id"],value)
                response = " Updated Successfully..."
            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"addAICanvasResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
        
    def getSubmittedAICanvasResponse(userId,useCaseName):
        
        """
            Retrieves the submitted AI Canvas response for a specific user and use case.
            Args:
                userId (str): The unique identifier of the user.
                useCaseName (str): The name of the use case.
            Returns:
                str: The AI Canvas response if found, or "No Record Found" if no response exists.
            Raises:
                Exception: If an error occurs during the process, the exception is logged, 
                           and re-raised with additional details.
            Notes:
                - This function queries two databases: `UseCaseNameDb` to find the use case details 
                  and `AICanvasDb` to retrieve the corresponding AI Canvas response.
                - If no response is found in the `AICanvasDb`, the function returns "No Record Found".
                - In case of an exception, detailed error information is logged, including the 
                  exception type, message, and line number, and the error is recorded in the 
                  `ExceptionDb` for further analysis.
            """
        
        try:
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
            responseDetails = AICanvasDb.findall({"UserId":userId,"useCaseNameId":useCaseDtl[0]._id})
            if(len(responseDetails) == 0):
                return "No Record Found"
            else:
                # obj = CanvasDataResponse       
                # obj_ResponseData = Canvas(CanvasResponse=responseDetails[0].CanvasResponse)
                # obj.dataResponseList = [obj_ResponseData]
                return responseDetails[0].AICanvasResponse 
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getSubmittedAICanvasResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)   
           



