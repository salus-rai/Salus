"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime
from questionnaire.dao.Questionnaires.CanvasDb import CanvasDb
from questionnaire.mapper.Questionnaires.canvasMapper import *

from questionnaire.config.logger import CustomLogger
from questionnaire.config.logger import request_id_var
from questionnaire.dao.ExceptionDb import ExceptionDb

from questionnaire.dao.Questionnaires.UseCaseDetailDb import *


log = CustomLogger()
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class CanvasContent:
    def addCanvasResponse(payload):
        """
        Adds or updates a canvas response in the database.
        Args:
            payload (dict): A dictionary containing the following keys:
                - UserId (str): The ID of the user.
                - UseCaseName (str): The name of the use case.
                - CanvasResponse (dict): The canvas response data.
        Returns:
            str: A message indicating whether the canvas response was added or updated successfully.
        Raises:
            Exception: If an error occurs during the process, it logs the error details and raises the exception.
        Notes:
            - If no existing canvas response is found for the given user and use case, a new entry is created.
            - If an existing canvas response is found, it is updated with the new data.
            - Logs detailed error information, including the line number and traceback frame, in case of an exception.
            - Error details are also stored in the ExceptionDb for further analysis.
        """
        
        

        log.debug("payload===="+str(payload))
        try:
            payload = AttributeDict(payload)
            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
            res = CanvasDb.findall({"UserId":payload.UserId,"useCaseNameId":useCaseDtl[0]._id})
            log.debug("resDtlData===="+str(res))
            value = {"CanvasResponse":payload.CanvasResponse.dict(),"LastUpdatedDateTime": datetime.datetime.now()}
            response =""
            if(len(res) == 0):
                responseDtl = CanvasDb.create({"useCaseNameId":useCaseDtl[0]._id,"UserId":payload.UserId,"CanvasResponse":payload.CanvasResponse})
                response="Added Successfully"
            else:
                data = res[0]
                responseUpdateDtl = CanvasDb.update(data["_id"],value)
                response = " Updated Successfully..."
            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"addCanvasResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
        
    def getSubmittedResponse(userId,useCaseName):
        
        """
            Retrieves the submitted response for a specific user and use case.
            Args:
                userId (str): The ID of the user whose response is being retrieved.
                useCaseName (str): The name of the use case for which the response is being retrieved.
            Returns:
                str: The CanvasResponse if a record is found, or "No Record Found" if no response exists.
            Raises:
                Exception: If an error occurs during the retrieval process, the exception is logged 
                           and re-raised with additional details.
            Notes:
                - The function queries two databases: UseCaseNameDb and CanvasDb.
                - If no matching record is found in CanvasDb, it returns "No Record Found".
                - Errors are logged with details including the exception type, message, and line number.
                - Any exceptions are also recorded in the ExceptionDb for further analysis.
            """
        
        
        
        try:
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
            responseDetails = CanvasDb.findall({"UserId":userId,"useCaseNameId":useCaseDtl[0]._id})
            if(len(responseDetails) == 0):
                return "No Record Found"
            else:
            # obj = CanvasDataResponse       
            # obj_ResponseData = Canvas(CanvasResponse=responseDetails[0].CanvasResponse)
            # obj.dataResponseList = [obj_ResponseData]
                return responseDetails[0].CanvasResponse 
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getSubmittedResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)

           



