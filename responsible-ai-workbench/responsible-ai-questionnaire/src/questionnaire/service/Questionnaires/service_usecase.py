"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from questionnaire.dao.Questionnaires.UseCaseDetailDb import *

from questionnaire.mapper.Questionnaires.mapper import UseCaseNameRequest
from questionnaire.config.logger import request_id_var
from questionnaire.dao.ExceptionDb import ExceptionDb

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class UseCase:

    def createUseCase(payload) -> UseCaseNameRequest:
        """
        Creates a new use case or checks if the use case already exists for a given user.
        Args:
            payload (dict): A dictionary containing the details of the use case to be created.
                Expected keys:
                    - UserId (str): The ID of the user.
                    - UseCaseName (str): The name of the use case.
        Returns:
            str: A message indicating whether the use case was successfully created or if it already exists.
        Raises:
            Exception: If an error occurs during the process, it logs the error details and raises the exception.
        Notes:
            - Logs debug information about the payload and response.
            - Logs error details including the exception type, message, and line number in case of failure.
            - Records exceptions in the ExceptionDb for tracking purposes.
        """
        
        # UseCaseNameDb
        try:
            payload =  AttributeDict(payload)
            # print("payload========",payload)
            log.debug("payload===="+str(payload))
            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId, "UseCaseName":payload.UseCaseName})
            if(len(useCaseDtl) > 0):
                response = "Use Case Already Created !!!!" 
            else:
                res = UseCaseNameDb.create({"UserId":payload.UserId, "UseCaseName":payload.UseCaseName})
                # print("Response======",res)
                log.debug("Response===="+str(res))
                response = "Use Case Created Successfully !!!!"


            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"createUseCaseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
    

    def getUseCaseDetail(userId):
        """
        Retrieves detailed information about use cases associated with a given user ID.
        Args:
            userId (str): The unique identifier of the user whose use case details are to be retrieved.
        Returns:
            list: A list containing a dictionary with the user's use case details. Each use case includes:
                - "UseCaseName" (str): The name of the use case.
                - "Score" (int): The score associated with the use case (default is 0 if not available).
                - "Risk_Classification" (str): The risk classification of the use case (default is "NA" if not available).
        Raises:
            Exception: If an error occurs during the retrieval or processing of use case details, 
                       the exception is logged and re-raised with additional context.
        Logging:
            - Logs the user ID and the retrieved use case details for debugging purposes.
            - Logs errors, including the exception type, description, and line number, in case of failure.
        Notes:
            - This function interacts with a database (UseCaseNameDb) to fetch use case details.
            - Errors are also recorded in an ExceptionDb for tracking purposes.
        """
        
        try:
            # print("userID=====",userId)
            log.debug("userID===="+str(userId))
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId})
            res=[]
            # print("useCaseDtl=========",useCaseDtl)
            log.debug("useCaseDtl===="+str(useCaseDtl))
            # res.append({"userid":userId})
            useCase=[]
            for i in useCaseDtl:
                useCaseData = {"UseCaseName": i.UseCaseName}
                use_case_data = {
                "UseCaseName": i.get("UseCaseName", None),
                "Score": i.get("Score", 0),
                "Risk_Classification": i.get("Risk_Classification", "NA")
                }
                useCase.append(use_case_data)
                # if hasattr(i, "UseCaseName"):
                #     print("True53========")
                #     print("i======",i)
                # try:
                #     useCaseData["Score"] = i.Score
                # except AttributeError:
                #     useCaseData["Score"] = None
                # if hasattr(i, "Score"):
                #     print("Inside if")
                #     useCaseData["Score"] = i.Score
                # else:
                #     print("Inside else")
                #     useCaseData["Score"] = None
                
                # if hasattr(i, 'Risk_Classification'):
                #     useCaseData["Risk_Classification"] = i.Risk_Classification
                # else:
                #     useCaseData["Risk_Classification"] = None
                
                # useCase.append(useCaseData)
            # for i in useCaseDtl:
            #     useCase.append({"UseCaseName":i.UseCaseName,"Score":i.Score,"Risk_Classification":i.Risk_Classification})
               
            # if(len)
            print("useCase=====",useCase)
            res.append({"useCaseName":useCase})
            return res
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getUseCaseDetailFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)