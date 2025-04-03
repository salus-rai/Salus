"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from io import BytesIO
import uuid
from fastapi import Body, Depends, File, Form,Request,APIRouter, HTTPException, UploadFile
from typing import List, Optional, Union
from pydantic import BaseModel

from questionnaire.service.Questionnaires.service_question import Questionnaires
from questionnaire.service.Questionnaires.service_usecase import *

# from questionnaire.mapper.Questionnaires.mapper import DimensionRequest, PrincipalGuidanceRequest, PrincipalGuidanceResponse, QuestionOptionRequest, QuestionOptionResponse, QuestionRequest, QuestionResponse, QusPrincipalMappingRequest, QusPrincipalMappingResponse, SubDimensionRequest, SubDimensionResponse,
from questionnaire.mapper.Questionnaires.mapper import ImpactRequest, SubmissionResponse,SubmissionRequest,UseCaseNameRequest

# from questionnaire.mapper.Questionnaires.mapper import DimensionResponse

from questionnaire.exception.exception import PrivacyException;

from questionnaire.config.logger import CustomLogger
from questionnaire.config.logger import request_id_var

from questionnaire.service.Questionnaires.service_canvas import CanvasContent
from questionnaire.service.Questionnaires.service_aicanvas import AICanvasContent
from questionnaire.mapper.Questionnaires.canvasMapper import *

from questionnaire.dao.UserLotAllocationDb import *
from questionnaire.dao.TelemetryUrlStore import *
from questionnaire.mapper.Questionnaires.lotAllocateMapper import *
from questionnaire.dao.ExceptionDb import ExceptionDb

from questionnaire.mapper.Questionnaires.aiCanvasMapper import *


router = APIRouter()
log=CustomLogger()


class LargeDataInput(BaseModel):
    data:list


@router.post('/questionnaire/createImpactClassification')
def useCase(payload:ImpactRequest):
   
    """
        Handles the creation of a use case by routing the provided payload to the appropriate service.
        Args:
            payload (ImpactRequest): The input data required to create a use case.
        Returns:
            Any: The response from the `createImpact` service.
        Raises:
            HTTPException: If a `PrivacyException` occurs, it raises an HTTP exception with the relevant details.
            HTTPException: If any other exception occurs, it raises an HTTP exception with a status code of 500 
                           and logs the error details for further investigation.
        Notes:
            - Generates a unique request ID for tracking purposes.
            - Logs the flow of execution for debugging and monitoring.
            - Handles exceptions gracefully and logs them in the database for debugging.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered useCase routing method")
    try:
        
        log.debug("before invoking create usecase service ")
        log.debug("payload====="+str(payload))
        
        # response=questionnaire.uploadFile(payload)
        response = Questionnaires.createImpact(payload)
        # response = "Hello"

        log.debug("after invoking create usecase service ")
        log.debug("res:"+str(response))
        log.info("exit create usecase routing method")
        # print("res----",response)
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"createUsecaseRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@router.post('/questionnaire/createUsecase')
def useCase(payload:UseCaseNameRequest):
    
    """
        Handles the creation of a use case by routing the request to the appropriate service.
        Args:
            payload (UseCaseNameRequest): The request payload containing the details for creating a use case.
        Returns:
            Any: The response from the UseCase creation service.
        Raises:
            HTTPException: If a PrivacyException occurs or any other exception is raised during processing.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered useCase routing method")
    try:
        
        log.debug("before invoking create usecase service ")
        log.debug("payload====="+str(payload))
        
        # response=questionnaire.uploadFile(payload)
        response = UseCase.createUseCase(payload)
        # response = "Hello"

        log.debug("after invoking create usecase service ")
        log.debug("res:"+str(response))
        log.info("exit create usecase routing method")
        # print("res----",response)
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"createUsecaseRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    

@router.get('/questionnaire/useCaseDetails/{userid}')


def process(userid):
    """
Endpoint to retrieve use case details for a specific user.
This function handles HTTP GET requests to fetch the details of a use case
associated with a given user ID. It logs the request, processes the request
through the UseCase service, and returns the response. In case of errors,
appropriate exceptions are raised and logged.
Args:
    userid (str): The unique identifier of the user for whom the use case
                  details are to be retrieved.
Returns:
    dict: A dictionary containing the use case details for the specified user.
Raises:
    HTTPException: Raised when a PrivacyException occurs or for any other
                   unexpected errors. The exception includes an appropriate
                   status code and error message.
"""
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered useCaseDetails routing method")
    try:
        log.debug("before invoking useCaseDetails usecase service ")
        # print(payload)
        
        response=UseCase.getUseCaseDetail(userid)
        log.debug("after invoking useCaseDetails usecase service ")
        log.debug("res:"+str(response))
        log.info("exit create useCaseDetails routing method")
        # print("res----",response)
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"useCaseDetailsRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    


  


# @router.post('/questionnaire/submitResponse')
# def subDimension(payload:SubmissionRequest):
#     id = uuid.uuid4().hex
#     request_id_var.set(id)
#     log.info("Entered subDimension routing method")

#     try:
#         # re = payload.file._file
#         # b = io.BytesIO()
#         # print(b.read)
#         # print("ressssss",re)
#         # payload={"file":file,"userId":userId,"exclusionList":exclusionList,"categories":categories}
#         log.debug("before invoking subDimension service ")
#         log.debug("payload:"+str(payload))
        
#         # response=questionnaire.uploadFile(payload)
#         response = Questionnaires.addResponseDetail(payload)
#         # response = "Hello"

#         log.debug("after invoking subDimension service ")
#         log.debug("res:"+str(response))
        
#         log.info("exit subDimension routing method")
#         return response
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit subDimension routing method")
#         raise HTTPException(**cie.__dict__)
#     except Exception as e:
#         log.error(str(e))
#         ExceptionDb.create({"UUID":request_id_var.get(),"function":"submitResponseRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
#         raise HTTPException(
#             status_code=500,
#             detail="Please check with administration!!",
#             headers={"X-Error": "Please check with administration!!"})
    



@router.post('/questionnaire/submitResponse')
def subDimension(input_data:LargeDataInput):
    
    """
        Handles the routing logic for processing sub-dimension data.
        This method generates a unique request ID, logs the entry and exit points, 
        and processes the input data by invoking the `addMultipleResponse` method 
        from the `Questionnaires` service. It also handles exceptions and logs 
        errors appropriately.
        Args:
            input_data (LargeDataInput): The input data containing the payload 
                                         to be processed.
        Returns:
            Any: The response from the `addMultipleResponse` method.
        Raises:
            HTTPException: If a `PrivacyException` occurs or any other exception 
                           is encountered during processing. The exception includes 
                           details about the error and a message to contact the 
                           administration.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered subDimension routing method")
    data=input_data.data
    # print("Data====",data)
    try:
       
        log.debug("before invoking subDimension service ")
        # log.debug("payload:"+str(input_data.data))

        data=input_data.data
        log.debug("Data165========"+str(data))
        
        # response=questionnaire.uploadFile(payload)
        response = Questionnaires.addMultipleResponse(data)
        # response = "Hello"

        log.debug("after invoking subDimension service ")
        log.debug("res:"+str(response))
        
        log.info("exit subDimension routing method")
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit subDimension routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"submitResponseRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    






@router.get('/questionnaire/Details')
def process():
    """
    Handles the routing logic for fetching questionnaires.
    This function generates a unique request ID, logs the entry and exit points,
    and invokes the `getQuestionnaries` service to fetch the required data. It
    also handles exceptions, including custom `PrivacyException` and generic
    exceptions, logging the errors and raising appropriate HTTP exceptions.
    Returns:
        response: The response object returned by the `getQuestionnaries` service.
    Raises:
        HTTPException: If a `PrivacyException` or any other exception occurs,
        an HTTPException is raised with appropriate status code and details.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getQuestionnariesRouter routing method")
    
    try:
        
        log.debug("before invoking create getQuestionnariesRouter service ")
        # print(payload)
        
        response=Questionnaires.getQuestionnaries()
        log.debug("after invoking create getQuestionnariesRouter service ")
        log.debug("res:"+str(response))
        log.info("exit create getQuestionnariesRouter routing method")
        # print("res----",response)
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        
        log.info("exit create getQuestionnariesRouter routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"DetailsRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    




@router.get('/questionnaire/riskDashboardDetails/{userid}/{useCaseName}')
def process(userid,useCaseName):
    
    """
        Processes the request to retrieve risk dashboard details for a given user and use case.
        Args:
            userid (str): The unique identifier of the user.
            useCaseName (str): The name of the use case for which the risk dashboard details are requested.
        Returns:
            dict: The response containing the risk dashboard details.
        Raises:
            HTTPException: If a PrivacyException occurs or any other exception is raised during processing.
                - For PrivacyException: The exception details are logged and re-raised as an HTTPException.
                - For other exceptions: The exception details are logged in the database, and an HTTPException
                  with a generic error message is raised.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getriskDashboardDetailssRouter routing method")
    try:
        log.debug("before invoking create getriskDashboardDetailssRouter service ")
        # print(payload)
        

        response=Questionnaires.getriskDashboardDetails(userid,useCaseName)
        log.debug("after invoking create getriskDashboardDetailssRouter service ")
        log.debug("res:"+str(response))
        log.info("exit create getriskDashboardDetailssRouter routing method")

        # print("res----",response)
        return response
        
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create getriskDashboardDetailssRouter routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"riskDashboardDetailsRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    

@router.post('/questionnaire/canvas/submitResponse')
def canvasRequest(payload :CanvasRequest):
    
    """
        Handles the routing logic for processing a canvas request.
        This function generates a unique request ID, logs the incoming payload, 
        and invokes the `addCanvasResponse` service to process the request. 
        It also handles exceptions and logs errors appropriately.
        Args:
            payload (CanvasRequest): The input payload containing the canvas request data.
        Returns:
            Response: The response object returned by the `addCanvasResponse` service.
        Raises:
            HTTPException: If a `PrivacyException` occurs or any other exception is raised, 
                           an HTTPException is thrown with appropriate details.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create addCanvasResponseRouter routing method")

    try:
        log.debug("before invoking create addCanvasResponseRouter service ")
        # print("payload=====",payload)
        log.debug("payload:"+str(payload))
        response = CanvasContent.addCanvasResponse(payload)
        log.debug("after invoking create addCanvasResponseRouter service ")  
        # print("res----",response)
        log.debug("res:"+str(response))
        log.info("exit create addCanvasResponseRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create addCanvasResponseRouter routing method")
        raise HTTPException(**cie.__dict__)

    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"submitResponseRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
@router.get('/questionnaire/canvas/getResponse/{userId}/{useCasename}' )
def get_responses(userId,useCasename):
    
    """
        Fetches the submitted responses for a given user and use case.
        This function generates a unique request ID, logs the process, and invokes
        the `CanvasContent.getSubmittedResponse` service to retrieve the responses.
        It handles specific exceptions such as `PrivacyException` and generic
        exceptions, logging errors and raising appropriate HTTP exceptions.
        Args:
            userId (str): The ID of the user whose responses are to be fetched.
            useCasename (str): The name of the use case for which responses are required.
        Returns:
            dict: The response data retrieved from the `CanvasContent.getSubmittedResponse` service.
        Raises:
            HTTPException: Raised in case of a `PrivacyException` or any other exception,
                           with appropriate status codes and error details.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getSubmittedResponseRouter routing method")

    try:
        log.debug("before invoking create getSubmittedResponseRouter service ")
        response = CanvasContent.getSubmittedResponse(userId,useCasename)
        log.debug("after invoking create getSubmittedResponseRouter service ")  
        # print("res----",response)
        log.debug("res:"+str(response))
        log.info("exit create getSubmittedResponseRouter routing method")

        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create getSubmittedResponseRouter routing method")
        raise HTTPException(**cie.__dict__)

    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"get_responsesRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

    


@router.post('/questionnaire/aicanvas/submitResponse')
def AIcanvasRequest(payload :AICanvasRequest):
    
    """
        Handles the routing of AI Canvas requests.
        This function processes the incoming payload, generates a unique request ID, 
        logs the request details, and invokes the AICanvasContent service to handle 
        the request. It also manages exceptions and logs errors appropriately.
        Args:
            payload (AICanvasRequest): The input data for the AI Canvas request.
        Returns:
            Response: The response generated by the AICanvasContent service.
        Raises:
            HTTPException: If a PrivacyException occurs or any other exception is raised, 
                           an HTTPException is returned with appropriate details.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered AIcanvasRequest routing method")
    try:
        log.debug("before invoking AIcanvasRequest usecase service ")
        # print("payload=====",payload)
        log.debug("payload:"+str(payload))
        response = AICanvasContent.addAICanvasResponse(payload)
        log.debug("after invoking AIcanvasRequest usecase service ")  
        # print("res----",response)
        log.debug("res:"+str(response))
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit AIcanvasRequest usecase routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"AIcanvasRequestRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
    
@router.get('/questionnaire/aicanvas/getResponse/{userId}/{useCasename}' )
def get_aicanvasresponses(userId,useCasename):
    
    """
        Retrieves the AI Canvas responses for a given user and use case.
        This function interacts with the AICanvasContent service to fetch the 
        submitted AI Canvas responses for the specified user and use case name. 
        It also handles exceptions and logs relevant information for debugging 
        and error tracking.
        Args:
            userId (str): The ID of the user for whom the AI Canvas responses are to be retrieved.
            useCasename (str): The name of the use case for which the AI Canvas responses are to be retrieved.
        Returns:
            dict: The AI Canvas responses retrieved from the AICanvasContent service.
        Raises:
            HTTPException: If a PrivacyException occurs or any other exception is raised during execution.
                           - For PrivacyException, the exception details are passed.
                           - For other exceptions, a generic error message is returned with a 500 status code.
        """
    
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered get_aicanvasresponses routing method")
    try:
        log.debug("before invoking get_aicanvasresponses usecase service ")
        response = AICanvasContent.getSubmittedAICanvasResponse(userId,useCasename)
        log.debug("after invoking get_aicanvasresponses usecase service ")  
        # print("res----",response)
        log.debug("res:"+str(response))
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create get_aicanvasresponses routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"get_aicanvasresponsesRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
    


@router.get('/questionnaire/ResubmitDetails/{userid}/{useCaseName}')
def process(userid,useCaseName):
    
    """
        Processes a request to reset questionnaires for a given user and use case.
        Args:
            userid (str): The unique identifier of the user.
            useCaseName (str): The name of the use case for which the questionnaires need to be reset.
        Returns:
            dict: The response from the `getResetQuestionnaries` service containing the reset questionnaire details.
        Raises:
            HTTPException: If a `PrivacyException` occurs or any other exception is encountered during processing.
                - For `PrivacyException`, the exception details are logged and re-raised as an HTTPException.
                - For other exceptions, the error is logged, recorded in the database, and an HTTPException with a 
                  generic error message is raised.
        """
    
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getResetQuestionnariesRouter routing method")


    try:
        log.debug("before invoking create getResetQuestionnariesRouter service ")
        # print(payload)
        

        response=Questionnaires.getResetQuestionnaries(userid,useCaseName)
        log.debug("after invoking create getResetQuestionnariesRouter service ")
        log.debug("res:"+str(response))
        log.info("exit create getResetQuestionnariesRouter routing method")

        # print("res----",response)
        return response
        

    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create getResetQuestionnariesRouter routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"ResubmitDetailsRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    

@router.post('/questionnaire/lotAssign')
def slotAssign(payload : lotAssignRequest):
    
    """
        Handles the slot assignment process by invoking the UserLotAllocationDb service.
        Args:
            payload (lotAssignRequest): The request payload containing the necessary data for slot assignment.
        Returns:
            Response: The response object returned by the UserLotAllocationDb.create method.
        Raises:
            HTTPException: If a PrivacyException occurs, it raises an HTTPException with the details of the exception.
            HTTPException: If any other exception occurs, it logs the error, stores the exception details in the ExceptionDb, 
                           and raises an HTTPException with a generic error message.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create slotAssignRouter routing method")

    try:
        log.debug("before invoking create slotAssignRouter service")
        log.debug("request payload: "+ str(payload))
        response = UserLotAllocationDb.create(payload)
        log.debug("after invoking create slotAssignRouter service")
        log.debug("response: "+ str(response))
        log.info("exit create slotAssignRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create slotAssignRouter routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"lotAssignRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
@router.get('/questionnaire/allLotDetails/{userId}')
def getAllSlotAssign(userId):
    """
    Retrieves all slot assignments for a given user.
    This function generates a unique request ID, logs the entry into the method, 
    and attempts to fetch all slot assignments associated with the provided user ID. 
    The response is reversed before being returned. In case of exceptions, appropriate 
    error handling is performed, including logging and raising HTTP exceptions.
    Args:
        userId (str): The ID of the user for whom slot assignments are to be retrieved.
    Returns:
        list: A reversed list of slot assignments associated with the user.
    Raises:
        HTTPException: If a PrivacyException occurs or any other exception is encountered.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getAllSlotAssignRouter routing method")

    try:
        log.debug("before invoking get getAllSlotAssignRouter service")
        response = UserLotAllocationDb.findAllOnUser(userId)
        response=response[::-1]
        # response=[1,2]
        log.debug("after invoking get getAllSlotAssignRouter service")
        log.debug("response: "+ str(response))
        log.info("exit create getAllSlotAssignRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create getAllSlotAssignRouter routing method")
        raise HTTPException(**cie.__dict__) 
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"getAllSlotAssignRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
@router.post('/questionnaire/telemetryUrlAdd')
def addTelemetryUrl(payload:linkRequest):
    
    """
        Handles the addition of a telemetry URL by processing the provided payload.
        This function generates a unique request ID, logs the process, and invokes
        the TelemetryUrlStore service to create a telemetry URL. It also handles
        exceptions, including privacy-related exceptions and general exceptions,
        logging relevant details and raising appropriate HTTP exceptions.
        Args:
            payload (linkRequest): The request payload containing the necessary
            data to create a telemetry URL.
        Returns:
            Response: The response from the TelemetryUrlStore service after
            successfully creating the telemetry URL.
        Raises:
            HTTPException: If a PrivacyException occurs, it raises an HTTPException
            with the details of the privacy error. For other exceptions, it raises
            an HTTPException with a generic error message and logs the exception
            details to the database.
        """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create addTelemetryUrlRouter routing method")

    try:
        log.debug("before invoking get addTelemetryUrlRouter service")
        log.debug("request payload: "+ str(payload))
        response = TelemetryUrlStore.create(payload)
        log.debug("after invoking get addTelemetryUrlRouter service")
        log.debug("response: "+ str(response))
        log.info("exit create addTelemetryUrlRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create addTelemetryUrlRouter routing method")
        raise HTTPException(**cie.__dict__) 
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"addTelemetryUrlRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
@router.get('/questionnaire/telemetryUrlGet/{tenant}')
def getAllTelemetryUrl(tenant):
    """
    Retrieves telemetry URL information for a given tenant.
    This function generates a unique request ID, logs the entry and exit points,
    and attempts to fetch telemetry URL data for the specified tenant using the
    `TelemetryUrlStore.findOne` method. It handles specific exceptions and logs
    errors appropriately.
    Args:
        tenant (str): The tenant identifier for which telemetry URL information
                      is to be retrieved.
    Returns:
        dict: The telemetry URL information retrieved from the data store.
    Raises:
        HTTPException: If a `PrivacyException` occurs or any other exception is
                       encountered during the process. The exception includes
                       details about the error and a message to contact the
                       administration.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create getAllTelemetryUrlRouter routing method")

    try:
        log.debug("before invoking get getAllTelemetryUrlRouter service")
        response = TelemetryUrlStore.findOne(tenant)
        log.debug("after invoking get getAllTelemetryUrlRouter service")
        log.debug("response: "+ str(response))
        log.info("exit create getAllTelemetryUrlRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create getAllTelemetryUrlRouter routing method")
        raise HTTPException(**cie.__dict__) 
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"getAllTelemetryUrlRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
from questionnaire.service.workbench.service import WorkBench

@router.post('/questionnaire/workbench/uploadFile')
def slotAssign(file: UploadFile = File(...), userId: str = Form(...), tenant: List[str] = Form(...)):
    """
    Handles the slot assignment process by uploading a file and associating it with a user and tenant.
    Args:
        file (UploadFile): The file to be uploaded, provided as a form input.
        userId (str): The ID of the user, provided as a form input.
        tenant (List[str]): A list of tenant strings, provided as a form input. The first element is expected to be a 
                            comma-separated string of tenant values.
    Returns:
        Response: The response from the WorkBench.uploadFile service after processing the request.
    Raises:
        HTTPException: If a PrivacyException occurs, it raises an HTTPException with the details of the exception.
        HTTPException: If any other exception occurs, it raises an HTTPException with a status code of 500 and a 
                       generic error message. The exception details are also logged in the database.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create slotAssignRouter routing method")

    try:
        payload={"file":file,"userId":userId,"tenant":tenant[0].split(',')}
        log.debug("before invoking create slotAssignRouter service")
        log.debug("request payload: "+ str(payload))
        response =WorkBench.uploadFile(payload)
        log.debug("after invoking create slotAssignRouter service")
        log.debug("response: "+ str(response))
        log.info("exit create slotAssignRouter routing method")
        return response
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create slotAssignRouter routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"lotAssignRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

