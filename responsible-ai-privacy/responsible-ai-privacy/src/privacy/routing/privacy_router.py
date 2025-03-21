'''
MIT license https://opensource.org/licenses/MIT Copyright 2024 Infosys Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from io import BytesIO
from tempfile import NamedTemporaryFile
import threading
import time
import uuid

import requests
from privacy.util.code_detect.ner.pii_inference.netcustom import code_detect_ner
from privacy.util.code_detect.ner.CodePIINER import codeNer
# from privacy.dao.TelemetryFlagDb import TelemetryFlag
from fastapi import Depends, Query,Request,APIRouter, HTTPException, Response, WebSocket,websockets,FastAPI,Cookie,Body
from typing import List, Union

from privacy.service.privacytelemetryservice import PrivacyTelemetryRequest
from privacy.service.Video_service import *

from fastapi.params import Form
from privacy.mappers.mappers import *
#from privacy.mappers.mappers import PIIEntity, PIIAnalyzeRequest, PIIAnonymizeResponse, PIIAnonymizeRequest,PIIAnalyzeResponse,PIIImageAnonymizeResponse,PIIImageAnalyzeResponse,PIIImageAnalyzeRequest


from privacy.service.Video_service import VideoService
# from privacy.service.logo_service import Logo 
from privacy.service.code_detect_service import *
from privacy.service.excel_service import Excel

from privacy.exception.exception import PrivacyException
from privacy.config.logger import CustomLogger

from fastapi import FastAPI, UploadFile,File
from fastapi.responses import FileResponse
from datetime import date
import concurrent.futures
from fastapi import Request
from fastapi.responses import StreamingResponse
from privacy.util.code_detect.ner.pii_inference.netcustom import *
# from privacy.util.face_detect.mask_detect_video import mask_video
import logging
# from privacy.code_generator.codegeneration import create_new_recognizer_file,modify_recognizer_registry,modify_init_py,run_wheel_creation_commands, copy_wheel_file,test
# from privacy.dao.privacy.PrivacyException import ExceptionDb
# from privacy.dao.privacy.TelemetryDb import TelemetryDb
from privacy.service.api_req import *
from privacy.service.__init__ import *
from privacy.service.textPrivacy import TextPrivacy,Shield
from privacy.service.imagePrivacy import ImagePrivacy
from privacy.service.dicomPrivacy import DICOMPrivacy
from privacy.service.loadRecognizer import LoadRecognizer
import cv2
import numpy as np
router = APIRouter()
# user_id=1234
log=CustomLogger()
app = FastAPI()

fileRouter=APIRouter()
# logger = UserLogger()

import tracemalloc
from transformers import AutoModelForTokenClassification, AutoTokenizer
#@router.post('/privacy/text/analyze', response_model= PIIAnalyzeResponse)
today = date.today()
from datetime import datetime
import asyncio
from dotenv import load_dotenv
load_dotenv()
# import gc
import os
from uuid import UUID, uuid4
# from fastapi_sessions.backends.implementations import InMemoryBackend
# from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
# from request_id_store import request_ids
from privacy.config.logger import request_id_var
import traceback
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from privacy.util.auth.auth_client_id import get_auth_client_id
from privacy.util.auth.auth_jwt import get_auth_jwt
from privacy.util.auth.auth_none import get_auth_none

# from fastapi.se

# from fastapi_session import get_session
# returns current date and time
now = datetime.now()
# from memory_profiler import profile
# telFlagData = TelemetryFlag.findall({})[0]
# tel_Falg = telFlagData["TelemetryFlag"]
# telFlagData = TelemetryFlag.findall({"Module":"Privacy"})
# print("Teldata==",telFlagData)
# if(len(telFlagData) == 0):
    # telData = TelemetryFlag.create({"module":"Privacy"})
    # print("telData===",telData)
magMap = {"True": True, "False": False,"true": True, "false": False}
tel_Falg=os.getenv("TELE_FLAG")
tel_Falg=magMap[tel_Falg]
# tel_Falg = os.getenv("TELE_FLAG", "False")  # Default to "False" if TELE_FLAG is not set
# tel_Falg = magMap.get(tel_Falg, False)  # Use .get() to safely access the dictionary and default to False if the key doesn't exist
# print("===============",tel_Falg,type(tel_Falg))
privacytelemetryurl = os.getenv("PRIVACY_TELEMETRY_URL")
privacyerrorteleurl = os.getenv("PRIVACY_ERROR_URL")

# print("tel_falg===",tel_Falg)
# Load the model and tokenizer for CODEFILE API
local_model_directory = "privacy/util/code_detect/ner/pii_inference/nermodel"
model = AutoModelForTokenClassification.from_pretrained(local_model_directory)
tokenizer = AutoTokenizer.from_pretrained(local_model_directory, model_max_length=10000)



class NoAccountException(Exception):
    pass

class NoAdminConnException(Exception):
    pass

class NoMatchingRecognizer(Exception):
    pass



## FUNCTION FOR FAIL_SAFE TELEMETRY
def send_telemetry_request(privacy_telemetry_request):
    id = uuid.uuid4().hex
    request_id_var.set("telemetry")

    try:
        # print("==",privacy_telemetry_request)
        log.debug("teleReq="+str(privacy_telemetry_request))
        
        response = requests.post(privacytelemetryurl, json=privacy_telemetry_request)
        # print/("===,",response)
        response.raise_for_status()
        response_data = response.json()
        log.debug("tele data response: "+ str(response))
        # print(response_data)
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"send_telemetry_requestFunction","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,    
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
        
class Telemetry:
    def error_telemetry_request(errobj,id):
        request_id_var.set(id)

        try:
            # print("==",privacy_telemetry_request)
            log.debug("teleReq="+str(errobj))
            log.debug("teleReq="+str(errobj['error']))  # Convert list to string before concatenating
            errorRequest = errobj['error'][0]
            print(json.dumps(errorRequest))
            if(tel_Falg):
                response = requests.post(privacyerrorteleurl, json=errorRequest)
                # print("===,",response)
                response.raise_for_status()
                response_data = response.json()
                log.debug("tele error response: "+ str(response))
                # print(response_data)
        except Exception as e:
            log.error(str(e))
            # ExceptionDb.create({"UUID":request_id_var.get(),"function":"send_telemetry_requestFunction","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise HTTPException(
                status_code=500,    
                detail="Please check with administration!!",
                headers={"X-Error": "Please check with administration!!"})
        


# Authentication 

auth_type = os.environ.get("AUTH_TYPE")

if auth_type == "azure":
    auth = get_auth_client_id()
elif auth_type == "jwt":
    auth = get_auth_jwt()

elif auth_type == 'none':
    auth = get_auth_none()
else:
    raise HTTPException(status_code=500, detail="Invalid authentication type configured")
    

router = APIRouter()

# @router.get('/privacy/loadrecog')
# def loadrecog():
    
#     return {"message":"Recognizers loaded successfully"}

@router.post('/privacy/loadRecognizer')
def loadRecognizer(payload:UploadFile = File(...)):
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered into analyze routing method" )

    try:
        log.debug("request payload: "+ str(payload))
        payload = {"file":payload}
        response = LoadRecognizer.set_recognizer(payload)
        return response
    except Exception as e:
        log.error(str(e))
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@router.get('/privacy/getRecognizer')
def loadRecognizer():
    id = uuid.uuid4().hex
    request_id_var.set(id)
    try:
        response = LoadRecognizer.load_recognizer()
        return response
    except Exception as e:
        log.error(str(e))
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@router.post('/privacy/text/analyze', response_model= PIIAnalyzeResponse)
# @profile
def analyze(payload: PIIAnalyzeRequest,auth= Depends(auth)):

    # gc.collect()
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered into analyze routing method" )

    try:
        log.debug("request payload: "+ str(payload))
        # raise Exception("This is a test exception")  # Add this line to raise an exception
        startTime = time.time()
        log.debug("Entered into analyze function")
        tracemalloc.start()
        # raise Exception()
        response = TextPrivacy.analyze(payload)
        ApiCall.delAdminList()
        tracemalloc.stop()
        log.debug("Returned from analyze function")
        endTime = time.time()
        totalTime = endTime - startTime
          
        log.info("Total Time taken "+str(totalTime))
        if(response==482):
            raise NoMatchingRecognizer
        if(response==None):
            # print("Inside Raise Exception")
            # return "Portfolio/Account Is Incorrect"
            raise NoAccountException
        # print("---",response.admin)
        if(response==404):
            raise NoAdminConnException
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},

        # )
    
        log.debug("response : "+ str(response))
        log.info("exit create from analyze routing method")
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        log.debug("TelFlag==="+ str(tel_Falg))
        # TelemetryDb.create({"UUID":id,"tenant":"privacy","apiName":analyze.__name__,"portfolio":payload.portfolio,"accountName":payload.account,"exclusion_list":payload.exclusionList,"entityrecognised":"Text"})
        if(tel_Falg == True):
            responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
            requestList = payload.__dict__
            requestObj = {
                "portfolio_name": payload.portfolio if payload.portfolio is not None else "None",
                "account_name": payload.account if payload.account is not None else "None",
                "inputText": requestList["inputText"],
                "exclusion_list": requestList["exclusionList"].split(',') if requestList["exclusionList"] is not None else [],
            }
            # lotNumber = 0  # Initialize lotNumber with a default value
            # if payload.lotNumber is not None:
            #     lotNumber = payload.lotNumber
            
            telemetryPayload = {
                "uniqueid": id,
                "tenant": "privacy",
                "apiname": analyze.__name__,           
                "user": payload.user if payload.user is not None else "None",
                "date":now.isoformat(),
                "lotNumber": payload.lotNumber if payload.lotNumber is not None else "None",
                # "exclusionList": payload.exclusionList,
                "request": requestObj,
                "response": responseList
            }
            # TelemetryDb.create(telemetryPayload)
            # Trigger the API call asynchronously using a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_telemetry_request, telemetryPayload)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        # responseprivacytelemetry = requests.post(privacytelemetryurl, json=privacy_telemetry_request.__dict__)
        # gc.collect()
        
        return response
    except PrivacyException as cie:
        log.debug("Exception for analyze")
        log.error(cie.__dict__)

        er=[{"tenetName":"Privacy","errorCode":"textAnalyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/analyze", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        # ExceptionDb.create({"UUID":id,"function":"textAnalyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        # print(cie)
        # print(cie.__dict__)
        log.error(cie, exc_info=True)
        log.info("exit create from analyze routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except NoMatchingRecognizer:
        raise HTTPException(
            status_code=482,
            detail=" No matching recognizers were found to serve the request.",
            headers={"X-Error": "Check Recognizer"},
        )
    except Exception as e:
        log.error(str(e))
        # print(error_dict)
        er=[{"tenetName":"Privacy","errorCode":"textAnalyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/analyze", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnalyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
@router.post('/privacy/text/anonymize', response_model= PIIAnonymizeResponse)
def anonymize(payload: PIIAnonymizeRequest,auth= Depends(auth)):
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    
    log.info("Entered create into anonymize routing method")
    try:
        # log.info("Entered create usecase routing method" )
        log.debug("request payload: "+ str(payload))
        startTime = time.time()
        log.debug("Entered into anonymize function")
        response = TextPrivacy.anonymize(payload)
        #print("response339===",response)
        ApiCall.delAdminList()
        log.debug("Returned from anonymize function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        # if(response!=482 or response!=None or response!=404):
        #     log.debug("response : "+ str(response))
        #     pass
        if(response==482):
            raise NoMatchingRecognizer
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException
        log.debug("response : "+ str(response))
        log.info("exit create from anonymize routing method")
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            requestList = payload.__dict__
            requestObj = {
               "portfolio_name": payload.portfolio if payload.portfolio is not None else "None",
                "account_name": payload.account if payload.account is not None else "None",
                "inputText": requestList["inputText"],
                "exclusion_list": requestList["exclusionList"].split(',') if requestList["exclusionList"] is not None else [],
            }
            responseObj = {
                "type": "None",
                "beginOffset": 0,
                "endOffset": 0,
                "score": 0,
                "responseText": response.anonymizedText
            }
            telemetryPayload = {
                "uniqueid": id,
                "tenant": "privacy",
                "apiname": anonymize.__name__,
                "user": payload.user if payload.user is not None else "None",
                "date":now.isoformat(),
                "lotNumber": payload.lotNumber if payload.lotNumber is not None else "None",
                # "exclusionList": payload.exclusionList,
                "request": requestObj,
                "response": [responseObj]
            }
            # Trigger the API call asynchronously using a separate thread
           
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_telemetry_request, telemetryPayload)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
    except PrivacyException as cie:
        log.error("Exception for anonymize")
        log.error(cie.__dict__)
        er=[{"tenetName":"Privacy","errorCode":"textAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/annonymize", "errorRequestMethod":"POST"}]
        # er=[{"UUID":id,"function":"textAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from anonymize routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except NoMatchingRecognizer:
        raise HTTPException(
            status_code=482,
            detail=" No matching recognizers were found to serve the request.",
            headers={"X-Error": "Check Recognizer"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"textAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/annonymize", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
            
@router.post('/privacy/text/encrpyt',response_model=PIIEncryptResponse)
def encrypt(payload: PIIAnonymizeRequest,auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    
    log.info("Entered create into encrypt routing method")
    try:
        log.debug("request payload: "+ str(payload))
        startTime = time.time()
        log.debug("Entered into encrypt function")
        response = TextPrivacy.encrypt(payload)
        log.debug("Returned from encrypt function")
        endTime = time.time()
        totalTime = endTime - startTime
        print("response=======",response)
        log.info("Total Time taken "+str(totalTime))
        
        if(response==None):
            raise NoAccountException
        log.info("exit create from encrypt routing method")
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            requestList = payload.__dict__
            requestObj = {
               "portfolio_name": payload.portfolio if payload.portfolio is not None else "None",
                "account_name": payload.account if payload.account is not None else "None",
                "inputText": requestList["inputText"],
                "exclusion_list": requestList["exclusionList"].split(',') if requestList["exclusionList"] is not None else [],
            }
            responseObj = {
                "type": "None",
                "beginOffset": 0,
                "endOffset": 0,
                "score": 0,
                "responseText": response.text
            }
            telemetryPayload = {
                "uniqueid": id,
                "tenant": "privacy",
                "apiname": anonymize.__name__,
                "user": payload.user if payload.user is not None else "None",
                "date":now.isoformat(),
                "lotNumber": payload.lotNumber if payload.lotNumber is not None else "None",
                # "exclusionList": payload.exclusionList,
                "request": requestObj,
                "response": [responseObj]
            }
            # TelemetryDb.create(telemetryPayload)
            
            
            # Trigger the API call asynchronously using a separate thread
           
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_telemetry_request, telemetryPayload)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
       
    except PrivacyException as cie:
        log.error("Exception for encrypt")
        log.error(cie.__dict__)
        er=[{"tenetName":"Privacy","errorCode":"textEncryptRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/encrpyt", "errorRequestMethod":"POST"}]
        # er=[{"UUID":id,"function":"textEncryptRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from encrypt routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"textEncryptRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/encrpyt", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
@router.post('/privacy/text/decrpyt',response_model= PIIDecryptResponse)  
def decrypt(payload: PIIDecryptRequest,auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into decrypt routing method")
    try:
        log.debug("request payload: "+ str(payload))
        startTime = time.time()
        log.debug("Entered into decrypt function")
        response = TextPrivacy.decryption(payload)
        log.debug("Returned from decrypt function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        return response
    except PrivacyException as cie:
        log.error("Exception for decrypt")
        log.error(cie.__dict__)
        er=[{"tenetName":"Privacy","errorCode":"textDecryptRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/decrpyt", "errorRequestMethod":"POST"}]
        # er=[{"UUID":id,"function":"textDecryptRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from decrypt routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er=[{"tenetName":"Privacy","errorCode":"textDecryptRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/text/decrpyt", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@router.post('/privacy/image/analyze', response_model= PIIImageAnalyzeResponse)
def image_analyze(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_analyze routing method")
    try:
        
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"portfolio":portfolio,"account":account,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"exclusion":exclusionList}
        log.debug("Requested payload" + str(payload))
        startTime = time.time()
        log.debug("Entered into image_analyze function")
        response = ImagePrivacy.image_analyze(payload)
        ApiCall.delAdminList()
        log.debug("Returned from image_analyze function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==482):
            raise NoMatchingRecognizer
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException        
        log.info("exit create from image_analyze routing method")
        log.debug("tel_Flag==="+str(tel_Falg))
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": image_analyze.__name__,
            #     # "portfolio": portfolio,
            #     # "accountName": account,
            #     # "exclusion_list": exclusionList,
            #     "request": requestList,
            #     "response": responseList
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for image_analyze")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"imageAnalyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"imageAnalyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/analyze", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageAnalyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from image_analyze routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except NoMatchingRecognizer:
        raise HTTPException(
            status_code=482,
            detail=" No matching recognizers were found to serve the request.",
            headers={"X-Error": "Check Recognizer"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"imageAnalyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"imageAnalyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/analyze", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageAnalyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@router.post('/privacy/image/anonymize')
def image_anonymize(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"portfolio":portfolio,"account":account,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"exclusion":exclusionList}
        log.debug("Payload:"+str(payload))
        startTime = time.time()
        log.debug("Entered into image_anonymize function")
        response = ImagePrivacy.image_anonymize(payload)
        ApiCall.delAdminList()
        log.debug("Returned from image_anonymize function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==482):
            raise NoMatchingRecognizer
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException 
        log.info("exit create from image_anonymize routing method")
        log.debug("tel_Flag==="+str(tel_Falg))
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": image_anonymize.__name__,
            #     # "portfolio": portfolio,
            #     # "accountName": account,
            #     # "exclusion_list": exclusionList,
            #     "request": requestList,
            #     "response": responseList
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for image_anonymize")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"imageAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"imageAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/anonymize", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except NoMatchingRecognizer:
        raise HTTPException(
            status_code=482,
            detail=" No matching recognizers were found to serve the request.",
            headers={"X-Error": "Check Recognizer"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"imageAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"imageAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/anonymize", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

# @router.post('/privacy/image/masking')
# async def image_mask(media: UploadFile = File(...), template: UploadFile = File(...),auth= Depends(auth)):
#     try:
#         # log.info("before invoking create usecase service ")
#         main_image_content = await media.read()
#         nparr = np.fromstring(main_image_content, np.uint8)
#         main_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         template_image_content = await template.read()
#         nparr = np.fromstring(template_image_content, np.uint8)
#         template_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         if template_image.shape[0] > main_image.shape[0] or template_image.shape[1] > main_image.shape[1]:
#             raise HTTPException(status_code=400, detail ="Mask image must be smaller or equal in size to the main image")
#         response = await ImagePrivacy.image_masking(main_image,template_image)
#         # log.info("after invoking image masking service")
#         is_success, buffer = cv2.imencode(".png", response)

#         # Create a StreamingResponse from the image buffer
#         return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/png")
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)
# @router.post('/privacy/pii/image/anonymize/zip')                                   #########@#@@#@#$@
# def image_anonymize(payload: UploadFile):
#     try:
#         log.info("Entered create usecase routing method" )
#         response = service.zipimage_anonymize(payload)
#         if(response==None):
#             raise HTTPException(
#             status_code=430,
#             detail="Portfolio/Account Is Incorrect",
#             headers={"X-Error": "There goes my error"},
#         )
#         log.info("after invoking create usecase service ")
        
#         log.info("exit create usecase routing method")
#         return response
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)


# @router.post('/privacy/pii/image/anonymize/multiple')
# def image_anonymize(payload: List[UploadFile] = File(...)):
#     try:
#         log.info("Entered create usecase routing method" )
#         response=[]
#         for image in payload:
#             response.append(service.image_anonymize(image))
            
#         log.info("after invoking create usecase service ")
        
#         log.info("exit create usecase routing method")
#         return response
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)

# @router.post('/privacy/pii/image/analyze/multiple')#,response_model=PIIMultipleImageAnalyzeResponse)
# def image_analyze(payload: List[UploadFile] = File(...)):
#     try:
#         log.info("Entered create usecase routing method" )
#         response=[]
#         for image in payload:
#             response.append(service.temp(image))
        
#         log.info("after invoking create usecase service ")
        
#         log.info("exit create usecase routing method")
#         return response
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)


@router.post('/privacy/image/verify')
def image_verify(image: UploadFile = File(...),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_verify routing method" )
    try:
        payload={"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
        log.debug("request payload: "+str(payload))
        startTime = time.time()
        log.debug("Entered into image_verify function")
        response = ImagePrivacy.image_verify(payload)
        ApiCall.delAdminList()
        log.debug("Returned from image_verify function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException        
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
      
        
        log.info("exit create from image_verify routing method")
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        log.debug("tel_Flag==="+ str(tel_Falg))
        # responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": image_verify.__name__,
            #     # "portfolio": portfolio,
            #     # "accountName": account,
            #     # "exclusion_list": exclusionList,
            #     "request": payload,
            #     "response": response
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for image_verify")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"imageVerifyRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
        er=[{"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from image_verify routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
    
@router.post('/privacy/image/hashify')
def image_hashify(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into imageEncryption routing method" )
    try:
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
        log.debug("request payload: "+str(payload))
        startTime = time.time()
        log.debug("Entered into imageEncryption function")
        response = ImagePrivacy.imageEncryption(payload)
        ApiCall.delAdminList()
        log.debug("Returned from imageEncryption function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException        
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
        log.info("exit create from into imageEncryption routing method")
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        log.debug("tel_Flag==="+str(tel_Falg))
        # requestList = payload.__dict__
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": image_verify.__name__,
            #     # "portfolio": portfolio,
            #     # "accountName": account,
            #     # "exclusion_list": exclusionList,
            #     "request": requestList,
            #     "response": response
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for imageEncryption")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"imageHashifyRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageHashifyRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"imageHashifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageHashifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    


# @router.post('/privacy/privacyShield', response_model= PIIPrivacyShieldResponse)
# def privacy_shield(payload: PIIPrivacyShieldRequest,auth= Depends(auth)):
#     id = uuid.uuid4().hex
#     request_id_var.set(id)
#     log.info("Entered create into privacyShield routing method")
#     try:
#         # log.info("Entered create usecase routing method" )
#         log.debug("request payload: "+ str(payload))
#         startTime = time.time()
#         log.debug("Entered into privacyShield function")
#         response = Shield.privacyShield(payload)
#         ApiCall.delAdminList()
#         log.debug("Returned from privacyShield function")
#         endTime = time.time()
#         totalTime = endTime - startTime
#         log.info("Total Time taken "+str(totalTime))
#         if(response==None):
#             raise NoAccountException
#         if(response==404):
#             raise NoAdminConnException        
#         #     raise HTTPException(
#         #     status_code=430,
#         #     detail="Portfolio/Account Is Incorrect",
#         #     headers={"X-Error": "There goes my error"},
#         # )
#         # log.info("after invoking create usecase service ")
#         log.debug("response : "+ str(response))
#         log.info("exit create from privacyShield routing method")
#         # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
#         # tel_Falg = telFlagData["TelemetryFlag"]
#         log.debug("tel_Flag==="+str(tel_Falg))
#         # responseList = response.privacyCheck
#         # requestList = payload.__dict__
#         if(tel_Falg == True):
#             log.debug("Inside Telemetry Flag")
#             # telemetryPayload = {
#             #     "uniqueid": id,
#             #     "tenant": "privacy",
#             #     "apiName": "privacyshield",
#             #     # "portfolio": payload.portfolio,
#             #     # "accountName": payload.account,
#             #     # "exclusion_list": "None",
#             #     "request": requestList,
#             #     "response": responseList
#             # }
#             # TelemetryDb.create(telemetryPayload)
            
#             # Trigger the API call asynchronously using a separate thread
#             # with concurrent.futures.ThreadPoolExecutor() as executor:
#             #     executor.submit(send_telemetry_request, privacy_telemetry_request)
#             log.info("******TELEMETRY REQUEST COMPLETED********")
#         return response
#     except PrivacyException as cie:
#         log.error("Exception for privacyShield")
#         log.error(cie.__dict__)
#         # ExceptionDb.create({"UUID":id,"function":"privacyShield","msg":cie.__dict__,"description":cie.__dict__})
#         er=[{"tenetName":"Privacy","errorCode":"privacyShield","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/privacyShield", "errorRequestMethod":"POST"}]
#         # er=[{"UUID":request_id_var.get(),"function":"privacyShield","msg":cie.__dict__,"description":cie.__dict__}]
#         er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
#         logobj = {"uniqueid":id,"error":er}
        
#         if len(er)!=0:
#             thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
#             thread.start()
#             if request_id_var.get() in error_dict:
#                 del error_dict[id] 
#         log.error(cie, exc_info=True)
#         log.info("exit create from privacyShield routing method")
#         raise HTTPException(**cie.__dict__)
#     except NoAccountException:
#         raise HTTPException(
#             status_code=430,
#             detail="Portfolio/Account Is Incorrect",
#             headers={"X-Error": "There goes my error"},
#         )
#     except NoAdminConnException:
#         raise HTTPException(
#             status_code=435,
#             detail=" Accounts and Portfolio not available with the Subscription!!",
#             headers={"X-Error": "Admin Connection is not established,"},
#         )
#     except Exception as e:
#         log.error(str(e))
#         # ExceptionDb.create({"UUID":request_id_var.get(),"function":"privacyShield","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
#         er=[{"tenetName":"Privacy","errorCode":"privacyShield","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/privacyShield", "errorRequestMethod":"POST"}]
#         # er=[{"UUID":request_id_var.get(),"function":"privacyShield","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
#         er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
#         logobj = {"uniqueid":id,"error":er}
        
#         if len(er)!=0:
#             thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
#             thread.start()
#             if request_id_var.get() in error_dict:
#                 del error_dict[id] 
#         raise HTTPException(
#             status_code=500,
#             detail="Please check with administration!!",
#             headers={"X-Error": "Please check with administration!!"})

# from privacy.service.dicom_service import DICOM
# @router.get('/privacy/pii/dicom/anonymize')
# def image_anonymize():
#     try:
#         log.info("Entered create usecase routing method" )
#         # payload={"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
#         # log.info(str(payload))
#         # response = service.image_anonymize(payload)
#         response=DICOM.dicomReader()
#         # print(response)
        
#         # if(response==None):
#         #     raise HTTPException(
#         #     status_code=430,
#         #     detail="Portfolio/Account Is Incorrect",
#         #     headers={"X-Error": "There goes my error"},
#         # )
#         log.info("after invoking create usecase service ")
        
#         log.info("exit create usecase routing method")
#         return response
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)
 
   
@router.post('/privacy/dicom/anonymize')
def dicom_anonymize(payload: UploadFile = File(...),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into readDicom routing method" )
    try:
        # payload={"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
        startTime = time.time()
        log.debug("Entered into readDicom function")
        response =DICOMPrivacy.readDicom(payload)
        log.debug("Returned from readDicom function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException  
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
     
        
        log.info("exit create from readDicom routing method")
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        log.debug("tel_Flag==="+str(tel_Falg))
        # responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
        # requestList = payload.__dict__
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": "DICOMIMAGE",
            #     # "portfolio": "None",
            #     # "accountName": "None",
            #     # "exclusion_list": "None",
            #     "request": requestList,
            #     "response": responseList
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for readDicom")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"DICOMAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"DICOMAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/dicom/anonymize", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"DICOMAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from readDicom routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"DICOMAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"DICOMAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er=[{"tenetName":"Privacy","errorCode":"DICOMAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/dicom/anonymize", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

@fileRouter.post('/privacy-files/excel/anonymize')
def logo_anonymize(excel: UploadFile = File(...),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into excelanonymize routing method" )
    try:
        payload={"excel":excel}
        print("payload==",payload)
        # print("type==",excel.file.content_type)
        startTime = time.time()
        log.debug("Entered into excelanonymize function")
        response = Excel.excelanonymize(payload)
        log.debug("Returned from excelanonymize function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        if(response==404):
            raise NoAdminConnException  
        
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
       
        log.info("exit create from excelanonymize routing method")
        log.debug("response===="+str(response))
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        log.debug("tel_Flag==="+str(tel_Falg))
        # responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
        # requestList = payload.__dict__
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": "Excel_Anonymize",
            #     # "portfolio": "None",
            #     # "accountName": "None",
            #     # "exclusion_list": "None",
            #     "request": requestList,
            #     "response": responseList
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")
        return FileResponse(response,media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # return response
        
    except PrivacyException as cie:
        log.error("Exception for excelanonymize")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"excelAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        er=[{"tenetName":"Privacy","errorCode":"excelAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy-files/excel/anonymize", "errorRequestMethod":"POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"excelAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except NoAdminConnException:
        raise HTTPException(
            status_code=435,
            detail=" Accounts and Portfolio not available with the Subscription!!",
            headers={"X-Error": "Admin Connection is not established,"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"excelAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"excelAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er=[{"tenetName":"Privacy","errorCode":"excelAnonimyzeRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy-files/excel/anonymize", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

## PAYLOAD CHANGED TO ACCEPT TEXT IN A STRUCTURED FORMAT AND GET RESPONSE FOR THE SAME
from starlette.responses import PlainTextResponse
@router.post('/privacy/code/anonymize',response_class=PlainTextResponse)
async def code_redaction(payload_text: str = Body(..., media_type="text/plain", description="The code to be anonymized"),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into textner routing method")
    try:
        log.debug("payload==" + str(payload_text))
        
        startTime = time.time()
        log.debug("Entered into textner function")
        response = codeNer.codeText(payload_text,model, tokenizer)
        log.debug("Returned from textner function")
        
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken " + str(totalTime))
        log.debug("response" + str(response))
        
        if response is None:
            raise NoAccountException
        
        log.info("exit create from textner routing method")
        # Return the response as plain text, maintaining the format
        return PlainTextResponse(content=response)
    except PrivacyException as cie:
        log.error("Exception for code anonymize")
        log.error(str(cie))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"excelAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"excelAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er=[{"tenetName":"Privacy","errorCode":"CodeAnnonymizeRouter","errorMessage":str(cie)+"Line No:"+str(cie.__traceback__.tb_lineno),"apiEndPoint":"/privacy/code/anonymize", "errorRequestMethod":"POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        raise cie

from io import BytesIO

@router.post('/privacy/codefile/anonymize')
async def code_anonymize(code_file: UploadFile = File(...)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into filener routing method" )
    try:
        # Read the file content from the UploadFile object
        code_content = await code_file.read()
        print("code_content==",code_content)
        # Perform code redaction
        startTime = time.time()
        log.debug("Entered into filener function")
        redacted_content, output_code_file = codeNer.codeFile(code_content, code_file.filename,model, tokenizer)
        log.debug("Returned from filener function")
        if isinstance(redacted_content, str):
            redacted_content = redacted_content.encode('utf-8')
        print(redacted_content,"REDACTED CONTENT")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        headers = {
            "Content-Disposition": f"attachment; filename={output_code_file}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }

        # Delete the uploaded file
        await code_file.close()
        # filepath = os.path.join('', code_file.filename)
        output_code_file = os.path.splitext(code_file.filename)[0] + "_redacted" + os.path.splitext(code_file.filename)[1]
        os.remove(output_code_file)
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        # responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
        # requestList = payload.__dict__
        if(tel_Falg == True):
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": code_anonymize.__name__,
            #     # "portfolio": "None",
            #     # "accountName": "None",
            #     # "exclusion_list": "None",
            #     "request": requestList,
            #     "response": responseList
            # }
            # TelemetryDb.create(telemetryPayload)
            
            # Trigger the API call asynchronously using a separate thread
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     executor.submit(send_telemetry_request, privacy_telemetry_request)
            log.info("******TELEMETRY REQUEST COMPLETED********")

        # Return the redacted code content as a response with the correct filename
        return StreamingResponse(BytesIO(redacted_content), media_type="application/octet-stream", headers=headers)
    except PrivacyException as cie:
        log.error("Exception for filener")
        log.error(cie, exc_info=True)
        # ExceptionDb.create({"UUID":id,"function":"codeFileAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        # er=[{"UUID":request_id_var.get(),"function":"codeFileAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er = [{"tenetName": "Privacy", "errorCode": "codeFileAnonimyzeRouter", "errorMessage": str(cie) + "Line No:" + str(cie.__traceback__.tb_lineno), "apiEndPoint": "/privacy/codefile/anonymize", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise cie
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"codeFileAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"codeFileAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er = [{"tenetName": "Privacy", "errorCode": "codeFileAnonimyzeRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/codefile/anonymize", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})




# # from privacy.service.test import Test
# @router.get('/privacy/pii/video/anonymizea')
# async def image_analyze():
#     try:
#         log.info("Entered create usecase routing method" )
#         # payload={"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
#         # response =VideoAnalyzer.anonymize(payload)
#         # print(response)
#         # if(response==None):
#         #     raise HTTPException(
#         #     status_code=430,
#         #     detail="Portfolio/Account Is Incorrect",
#         #     headers={"X-Error": "There goes my error"},
#         # )
#         # log.info("after invoking create usecase service ")
#         # x=[]
#         x=Test.work()
#         # for i in x:
#         #     print(i)
#         # log.info("exit create usecase routing method")
#         return StreamingResponse(x,media_type="plain/text")
        
        
#     except PrivacyException as cie:
#         log.error(cie.__dict__)
#         log.info("exit create usecase routing method")
#         raise HTTPException(**cie.__dict__)
# app=FastAPI()
# cc=set()
# @app.websocket("/ws")
# async def check(websocket:WebSocket):
#     await websocket.accept()
#     cc.add(websocket)
#     try:
#         while True:
#             m="asdasdasdasdasd"
#             await websocket.send_text(m)
#             await asyncio.sleep(1)
#     except:
#         cc.remove(websocket)



from privacy.service.diffrentialPrivacy import DiffPrivacy
@router.post('/privacy/DifferentialPrivacy/file')
def diff_privacy_file(dataset: UploadFile = File(...),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into uploadFIle routing method" )
    try:
        # payload={"excel":excel}
        # print("payload==",payload)
        # print("type==",excel.file.content_type)
        startTime = time.time()
        log.debug("Entered into uploadFIle function")
        response = DiffPrivacy.uploadFIle(dataset)
        log.debug("Returned from uploadFIle function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
        # log.info("after invoking create usecase service ")
        
        log.info("exit create from uploadFIle routing method")
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        # print("tel_Flag===",tel_Falg)
        # if(tel_Falg == True):
        #     print("Inside Telemetry Flag")
        #     
        #     # Trigger the API call asynchronously using a separate thread
        #     with concurrent.futures.ThreadPoolExecutor() as executor:
            #    executor.submit(send_telemetry_request, privacy_telemetry_request)
        return response
    except PrivacyException as cie:
        log.error("Exception for uploadFIle")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"diffPrivacyFileRouter","msg":cie.__dict__,"description":cie.__dict__})
        # er=[{"UUID":request_id_var.get(),"function":"diffPrivacyFileRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er = [{"tenetName": "Privacy", "errorCode": "diffPrivacyFileRouter", "errorMessage": str(cie) + "Line No:" + str(cie.__traceback__.tb_lineno), "apiEndPoint": "/privacy/DifferentialPrivacy/file", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from uploadFIle routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"diffPrivacyFileRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        # er=[{"UUID":request_id_var.get(),"function":"diffPrivacyFileRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er = [{"tenetName": "Privacy", "errorCode": "diffPrivacyFileRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/DifferentialPrivacy/file", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    
from privacy.service.diffrentialPrivacy import DiffPrivacy
@router.post('/privacy/DifferentialPrivacy/anonymize')
def diff_privacy_anonymize(suppression:Optional[str]=Form(""),noiselist:Optional[str]=Form(""),binarylist:Optional[str]=Form(""),rangeList:Optional[str]=Form(""),auth= Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into diffPrivacy routing method" )
    try:
        # log.info("Entered create usecase routing method" )
        # payload={"excel":excel}
        # print("payload==",payload)
        payload={"suppression":suppression,"noiselist":noiselist,"binarylist":binarylist,"rangelist":rangeList}
        # print("type==",excel.file.content_type)
        startTime = time.time()
        log.debug("Entered into diffPrivacy function")
        response = DiffPrivacy.diffPrivacy(payload)
        log.debug("Returned from diffPrivacy function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        #     raise HTTPException(
        #     status_code=430,
        #     detail="Portfolio/Account Is Incorrect",
        #     headers={"X-Error": "There goes my error"},
        # )
        # log.info("after invoking create usecase service ")
        
        log.info("exit create from diffPrivacy routing method")
        log.debug("res===="+str(response))
        # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
        # tel_Falg = telFlagData["TelemetryFlag"]
        # print("tel_Flag===",tel_Falg)
        # if(tel_Falg == True):
        #     print("Inside Telemetry Flag")
        #     
        #     # Trigger the API call asynchronously using a separate thread
        #     with concurrent.futures.ThreadPoolExecutor() as executor:
            #    executor.submit(send_telemetry_request, privacy_telemetry_request)
        # return response
        headers = {"Content-Disposition": f"attachment; filename=x.csv"}
        return StreamingResponse(response, media_type="text/csv", headers=headers)
    except PrivacyException as cie:
        log.error("Exception for diffPrivacy")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"diffPrivacyAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__})
        # er=[{"UUID":request_id_var.get(),"function":"diffPrivacyAnonimyzeRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er = [{"tenetName": "Privacy", "errorCode": "diffPrivacyAnonimyzeRouter", "errorMessage": str(cie) + "Line No:" + str(cie.__traceback__.tb_lineno), "apiEndPoint": "/privacy/DifferentialPrivacy/anonymize", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        # er={"UUID":request_id_var.get(),"function":"diffPrivacyAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        # er=[{"UUID":request_id_var.get(),"function":"diffPrivacyAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er = [{"tenetName": "Privacy", "errorCode": "diffPrivacyAnonimyzeRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/DifferentialPrivacy/anonymize", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
   
@fileRouter.post('/privacy-files/video/anonymize')
async def videoPrivacy(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),video: UploadFile = File(...),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),auth= Depends(auth)):
    # payload = {"video": video, "easyocr": ocr}
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"video":video,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
        startTime = time.time()
        response = await VideoService.videoPrivacy(payload)
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken "+str(totalTime))
        if(response==None):
            raise NoAccountException
        
        
        log.info("exit create from image_anonymize routing method")
        return response
        
    except PrivacyException as cie:
        log.error("Exception for video_privacy")
        log.error(cie.__dict__)
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # ExceptionDb.create({"UUID":id,"function":"videoPrivacyRouter","msg":cie.__dict__,"description":cie.__dict__})
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            
            if request_id_var.get() in error_dict:
                del error_dict[id]
        log.error(cie, exc_info=True)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        er = [{"tenetName": "Privacy", "errorCode": "diffPrivacyAnonimyzeRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/DifferentialPrivacy/anonymize", "errorRequestMethod": "POST"}]
        
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"videoPrivacyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})

from privacy.service.pdf_service import PDFService
@fileRouter.post('/privacy-files/PDF/anonymize')
async def PDF(pdf:UploadFile=File(...),ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),auth= Depends(auth)):
    # payload = {"video": video, "easyocr": ocr}
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service ")

        payload={"easyocr":ocr,"mag_ratio":False,"rotationFlag":False,"file": pdf,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
      
        log.debug("Request payload: "+ str(payload))
        response = PDFService.mask_pdf(AttributeDict(payload))
        if(response==None):
            raise NoAccountException
        log.info("After invoking create usecase service ")
        log.debug("Response : "+ str(response))
        log.info("Exit create usecase routing method")
        end_time = datetime.now()
        log.info(f"end_time: {end_time}")
        total_time = end_time - start_time
        log.info(f"total_time: {total_time}")
        response = Response(content=response.read(), media_type="application/pdf")
        response.headers["Content-Disposition"] = "attachment; filename="+pdf.filename

        return response
        
    except PrivacyException as cie:
        log.error("Exception for encrypt")
        log.error(cie.__dict__)
        er=[{"UUID":id,"function":"textEncryptRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        # 
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        log.error(cie, exc_info=True)
        log.info("exit create from encrypt routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        er=[{"UUID":request_id_var.get(),"function":"textAnonimyzeRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid":id,"error":er}
        if len(er)!=0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id] 
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
    

from privacy.service.ppt_service import PPTService  
@fileRouter.post('/privacy-files/PPT/anonymize')
async def PPT(ppt: UploadFile = File(...), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None), auth=Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method")
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service")

        payload = {"easyocr": ocr, "mag_ratio": False, "rotationFlag": False, "file": ppt, "portfolio": portfolio, "account": account, "exclusion": exclusionList}

        log.debug("Request payload: " + str(payload))
        response = PPTService.mask_ppt(AttributeDict(payload))
        if response is None:
            raise NoAccountException
        log.info("After invoking create usecase service")
        log.debug("Response : " + str(response))
        log.info("Exit create usecase routing method")
        end_time = datetime.now()
        log.info(f"end_time: {end_time}")
        total_time = end_time - start_time
        log.info(f"total_time: {total_time}")
        response = Response(content=response.read(), media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        response.headers["Content-Disposition"] = "attachment; filename=" + ppt.filename

        return response

    except PrivacyException as cie:
        log.error("Exception for encrypt")
        log.error(cie.__dict__)
        er = [{"UUID": id, "function": "textEncryptRouter", "msg": cie.__dict__, "description": cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}
        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        log.error(cie, exc_info=True)
        log.info("exit create from encrypt routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        er = [{"UUID": request_id_var.get(), "function": "textAnonimyzeRouter", "msg": str(e), "description": str(e) + "Line No:" + str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}
        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"}
        )

from privacy.service.docs_service import DOCService
@fileRouter.post('/privacy-files/DOCX/anonymize')
async def DOCX(docx: UploadFile = File(...), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None), auth=Depends(auth)):
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method")
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service")

        payload = {"easyocr": ocr, "mag_ratio": False, "rotationFlag": False, "file": docx, "portfolio": portfolio, "account": account, "exclusion": exclusionList}

        log.debug("Request payload: " + str(payload))
        response = DOCService.mask_doc(AttributeDict(payload))
        if response is None:
            raise NoAccountException
        log.info("After invoking create usecase service")
        log.debug("Response : " + str(response))
        log.info("Exit create usecase routing method")
        end_time = datetime.now()
        log.info(f"end_time: {end_time}")
        total_time = end_time - start_time
        log.info(f"total_time: {total_time}")
        response = Response(content=response.read(), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response.headers["Content-Disposition"] = "attachment; filename=" + docx.filename

        return response

    except PrivacyException as cie:
        log.error("Exception for encrypt")
        log.error(cie.__dict__)
        er = [{"UUID": id, "function": "textEncryptRouter", "msg": cie.__dict__, "description": cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}
        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        log.error(cie, exc_info=True)
        log.info("exit create from encrypt routing method")
        raise HTTPException(**cie.__dict__)
    except NoAccountException:
        raise HTTPException(
            status_code=430,
            detail="Portfolio/Account Is Incorrect",
            headers={"X-Error": "There goes my error"},
        )
    except Exception as e:
        log.error(str(e))
        er = [{"UUID": request_id_var.get(), "function": "textAnonimyzeRouter", "msg": str(e), "description": str(e) + "Line No:" + str(e.__traceback__.tb_lineno)}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}
        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        raise HTTPException(
            status_code=500,
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"}
        )