"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from io import BytesIO
import os
import threading
import uuid
from bson import Binary, ObjectId
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
from questionnaire.dao.LegalAgent.legalAgentQuestionsdb import *
from questionnaire.dao.LegalAgent.legalAgentArticlesdb import *
from questionnaire.dao.LegalAgent.legalAgentAnnex import *
from questionnaire.dao.LegalAgent.agentPredictRisk import *
from questionnaire.dao.LegalAgent.LegalAgentFileProcDb import *

from questionnaire.mapper.Questionnaires.aiCanvasMapper import *

from questionnaire.service.LegalAgent.compliance_advisor import process_compliance_advisor
from questionnaire.service.LegalAgent.helper import processCanvasData

from questionnaire.service.LegalAgent.service import AgentService


agentRouter = APIRouter(
    prefix="/legalAgent",
    tags=["Legal Agent"],
)
log=CustomLogger()

@agentRouter.post('/uploadFile')
async def uploadFile(file: UploadFile = File(...), user_id: str = Form(...)):
    try:
        processing_id = str(ObjectId())
        pdf_content = await file.read()
        
        pdf_content = pdf_content.decode('utf-8', errors='replace')
        LegalAgentFileProcessing.create({
            "_id": ObjectId(processing_id),
            "user_id": user_id,
            "file_name": file.filename,
            "status": "Processing",  # "Processing", "Completed", "Failed"
            "reportLink": None,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        thread = threading.Thread(target=process_compliance_advisor, args=(processing_id, pdf_content, user_id))
        thread.start()
        
        return {"message": "Processing started.", "processing_id": processing_id}
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit legal agent upload file method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"uploadFile","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Failed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})


@agentRouter.get('/generateReport')
def generateReport(userId: str, useCaseName: str):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    processing_id = str(ObjectId())
    log.info("Entered create generateReport routing method")
    try:
        log.debug("before saving processing details")
        LegalAgentFileProcessing.create({
            "_id": ObjectId(processing_id),
            "user_id": userId,
            "file_name": useCaseName,
            "status": "Processing",  # "Processing", "Completed", "Failed"
            "reportLink": None,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        log.debug("after saving processing details")
        log.debug("before fetching canvas data")
        canvasData = CanvasContent.getSubmittedResponse('"' + userId + '"',useCaseName)
        aiCanvasData = AICanvasContent.getSubmittedAICanvasResponse('"' + userId + '"',useCaseName)
        
        combinedData = processCanvasData(canvasData, aiCanvasData)
        
        log.debug("after fetching canvas data")  
        
        thread = threading.Thread(target=process_compliance_advisor, args=(processing_id, combinedData, userId))
        thread.start()

        log.info("exit create generateReport routing method after thread start")

        return {"message": "Processing started.", "processing_id": processing_id}
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit create generateReport routing method")
        raise HTTPException(**cie.__dict__)

    except Exception as e:
        # log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"generateReport","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Failed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'errorMessage': str(e)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@agentRouter.get('/getAllReports')
def getAllReports(user_id: str):
    id = uuid.uuid4().hex
    try:
        # log.debug("before invoking findall service")
        reports = LegalAgentFileProcessing.findall(user_id)
        # log.debug("after invoking findall service")
        # log.debug("res:" + str(reports))
        # log.info("exit getAllReports routing method")
        return reports
    except PrivacyException as cie:
        print("exit get reports method")
    #     log.error(cie.__dict__)
    #     log.info("exit get reports method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        # log.error(str(e))
        print(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"getAllReports","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})


@agentRouter.post('/predictRiskFileUpload')
async def predictRiskFileUpload(file: UploadFile = File(...), user_id: str = Form(...)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    try:
        log.info("Predict Risk Upload Starts")
        pdf_content = await file.read()
        pdf_content = pdf_content.decode('utf-8', errors='replace')
        agentService = AgentService()
        log.info("Before PredictRisk Check")
        response = agentService.predict_risk(pdf_content)
        log.info("After PredictRisk Check")
        if response['risk'] == None:
            raise HTTPException(
                status_code=500,
                detail="Please check with administration!!",
                headers={"X-Error": "Please check with administration!!"})
        payload = {
            "user_id": user_id,
            "risk": response['risk'],
            "reason": response['reason'],
            "file_name": file.filename,
            "file_data": Binary(pdf_content.encode()),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        log.info("Before Storing the risk in DB")
        result = PredictRisk.create(payload)
        log.info("After Storing the risk in DB")
        log.info("Predict Risk Upload ENDS")
        return {"status": "Success" ,"data": response,"id": str(result.inserted_id)}
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit predictRisk routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"predictRisk","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
@agentRouter.get('/getAllPredictRisk')
def getAllPredictRisk(user_id: str):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    try:
        log.info("Get All Predict Risk STARTS")
        reports = PredictRisk.findall(user_id)
        log.info("Get All Predict Risk ENDS")
        return reports
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit getAllPredictRisk routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"getAllPredictRisk","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
@agentRouter.get('/getPredictRisk')
def getPredictRisk(id: str):
    request_id_var.set(uuid.uuid4().hex)
    try:
        report = PredictRisk.findOne(id)
        return report
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit getPredictRisk routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"getPredictRisk","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
@agentRouter.delete('/deletePredictRisk')
def deletePredictRisk(id: str):
    request_id_var.set(uuid.uuid4().hex)
    try:
        log.info("DELETE Predict Risk BEFORE")
        result = PredictRisk.deleteOne(id)
        log.info("DELETE Predict Risk AFTER")
        if result:
            return {"status": "Success"}
        else:
            return {"status": "Failed"}
    except PrivacyException as cie:
        log.error(cie.__dict__)
        log.info("exit deletePredictRisk routing method")
        raise HTTPException(**cie.__dict__)
    except Exception as e:
        log.error(str(e))
        ExceptionDb.create({"UUID":request_id_var.get(),"function":"deletePredictRisk","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})