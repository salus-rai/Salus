'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024 Infosys Ltd
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

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

