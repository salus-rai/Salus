"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


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
from privacy.service.csv_service import *
from privacy.service.json_service import *
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
 # if(len(telFlagData) == 0):
    # telData = TelemetryFlag.create({"module":"Privacy"})
sslv={"False":False,"True":True,"None":True}
 
magMap = {"True": True, "False": False,"true": True, "false": False}
tel_Falg=os.getenv("TELE_FLAG")
tel_Falg=magMap[tel_Falg]
# tel_Falg = os.getenv("TELE_FLAG", "False")  # Default to "False" if TELE_FLAG is not set
# tel_Falg = magMap.get(tel_Falg, False)  # Use .get() to safely access the dictionary and default to False if the key doesn't exist
privacytelemetryurl = os.getenv("PRIVACY_TELEMETRY_URL")
privacyerrorteleurl = os.getenv("PRIVACY_ERROR_URL")

 
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
    """
    Sends a telemetry request.

    Args:
        privacy_telemetry_request (dict): The telemetry request data.

    Raises:
        HTTPException: If an error occurs while sending the telemetry request.

    Returns:
        None
    """
    id = uuid.uuid4().hex
    request_id_var.set("telemetry")

    try:
        log.debug("teleReq=" + json.dumps(privacy_telemetry_request, indent=4))
        
        response = requests.post(privacytelemetryurl, json=privacy_telemetry_request,verify=sslv[os.getenv("VERIFY_SSL","None")])
 
        response.raise_for_status()
        response_data = response.json()
        log.debug("tele data response: "+ str(response))
 
    except Exception as e:
        log.error(str(e))
        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"send_telemetry_requestFunction","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
        raise HTTPException(
            status_code=500,    
            detail="Please check with administration!!",
            headers={"X-Error": "Please check with administration!!"})
        
        
class Telemetry:
    def error_telemetry_request(errobj,id):
        """
        Sends an error telemetry request to a specified URL.

        Args:
            errobj (dict): The error object containing error details.
            id (str): The request ID to be set.

        Returns:
            None

        Raises:
            HTTPException: If an exception occurs during the request process.

        Notes:
            - Logs the error object and the error details.
            - Logs the response from the telemetry server.
            - Logs any exceptions that occur during the request process.
        """
        request_id_var.set(id)

        try:
 
            log.debug("teleReq="+str(errobj))
            log.debug("teleReq="+str(errobj['error']))  # Convert list to string before concatenating
            errorRequest = errobj['error'][0]
 
            if(tel_Falg):
                response = requests.post(privacyerrorteleurl, json=errorRequest,verify=sslv[os.getenv("VERIFY_SSL","None")])
 
                response.raise_for_status()
                response_data = response.json()
                log.debug("tele error response: "+ str(response))
 
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
    """
    Loads a recognizer from the uploaded file.

    Args:
        payload (UploadFile): The uploaded file containing the recognizer data.

    Returns:
        None

    Raises:
        HTTPException: If an error occurs during the file upload or processing.

    Notes:
        - The function expects the file to be in a specific format.
        - Logs any errors that occur during the file upload or processing.
    """
     
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
    """
    Load the recognizer and return the response.

    This function generates a unique ID, sets it in the request_id_var, and then attempts to load the recognizer.
    If loading the recognizer fails, an exception is raised with a 500 status code and an error message.

    Returns:
        The response from loading the recognizer.

    Raises:
        HTTPException: If loading the recognizer fails.
    """
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
    """
    Analyzes the given payload for personally identifiable information (PII).

    Args:
        payload (PIIAnalyzeRequest): The request payload containing the text to be analyzed.
        auth (Depends(auth), optional): The authentication dependency. Defaults to Depends(auth).

    Returns:
        Any: The response from the analysis.

    Raises:
        NoAccountException: If the portfolio/account is incorrect.
        NoAdminConnException: If the accounts and portfolio are not available with the subscription.
        NoMatchingRecognizer: If no matching recognizers were found to serve the request.
        HTTPException: If any other exception occurs during the analysis.
    """
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
 
            # return "Portfolio/Account Is Incorrect"
            raise NoAccountException
 
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
    """
    Anonymizes the given text for personally identifiable information (PII)..

    Args:
        payload (PIIAnonymizeRequest): The payload containing the data to be anonymized.
        auth: The authentication dependency.

    Returns:
        The response from the TextPrivacy.anonymize function.

    Raises:
        NoMatchingRecognizer: If no matching recognizers were found to serve the request.
        NoAccountException: If the portfolio/account is incorrect.
        NoAdminConnException: If accounts and portfolio are not available with the subscription.
        HTTPException: If any other exception occurs.
    """
    id = uuid.uuid4().hex
    request_id_var.set(id)
    
    log.info("Entered create into anonymize routing method")
    try:
        # log.info("Entered create usecase routing method" )
        log.debug("request payload: "+ str(payload))
        startTime = time.time()
        log.debug("Entered into anonymize function")
        response = TextPrivacy.anonymize(payload)
 
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
def encrypt(payload: PIIEncryptRequest, auth=Depends(auth)):
    """
    Encrypts the given text for personally identifiable information (PII) data.

    Args:
        payload (PIIEncryptRequest): The payload to be encrypted.
        auth: The authentication dependency.

    Returns:
        The encrypted response.

    Raises:
        NoAccountException: If the response is None.
        PrivacyException: If an exception occurs during encryption.
        HTTPException: If the account is incorrect or if there is a general exception.

    """
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
    """
    Decrypts the given text for the personally identifiable information (PII)..

    Args:
        payload (PIIDecryptRequest): The payload to be decrypted.
        auth: The authentication dependency.

    Returns:
        The decrypted response.

    Raises:
        PrivacyException: If there is an exception during the decryption process.
        NoAccountException: If the portfolio/account is incorrect.
        HTTPException: If there is a general exception during the decryption process.
    """
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
def image_analyze(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth= Depends(auth)):
    """
    Analyzes the given image for privacy-related information.

    Args:
    - ocr (str): The OCR engine to use for text extraction. Valid options are 'Tesseract', 'EasyOcr', and 'ComputerVision'.
    - magnification (str): The magnification level of the image.
    - rotationFlag (str): The rotation flag of the image.
    - image (UploadFile): The image file to analyze.
    - nlp (str): The NLP model to use for text analysis.
    - portfolio (Optional[str]): The portfolio associated with the image.
    - account (Optional[str]): The account associated with the image.
    - exclusionList (Optional[str]): The list of entities to exclude from analysis.
    - piiEntitiesToBeRedacted (Optional[str]): The list of PII entities to redact from the image.
    - scoreThreshold (Optional[float]): The threshold for the privacy score.
    - auth: The authentication dependency.

    Returns:
    - The response from the image analysis.

    Raises:
    - NoMatchingRecognizer: If no matching recognizers were found to serve the request.
    - NoAccountException: If the portfolio/account is incorrect.
    - NoAdminConnException: If accounts and portfolio are not available with the subscription.
    - HTTPException: If any other exception occurs during the image analysis.
    """
 
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_analyze routing method")
    try:
        
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"nlp":nlp if nlp!="" else None,"portfolio":portfolio,"account":account,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"exclusion":exclusionList,'scoreThreshold':scoreThreshold}
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
def image_anonymize(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),portfolio:Union[str]=Form(None),account:Union[str]=Form(None),exclusionList:Union[str]=Form(None),piiEntitiesToBeRedacted:Union[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth= Depends(auth)):
    """
    Anonymizes an image for personally identifiable information (PII).

    Args:
        ocr (str): The OCR engine to be used for text extraction. Must be one of ['Tesseract', 'EasyOcr', 'ComputerVision'].
        magnification (str): The magnification ratio for the image.
        rotationFlag (str): The rotation flag for the image.
        image (UploadFile): The image file to be anonymized.
        nlp (str): The NLP model to be used for text redaction. Default is None.
        portfolio (Union[str]): The portfolio name. Default is None.
        account (Union[str]): The account name. Default is None.
        exclusionList (Union[str]): The exclusion list. Default is None.
        piiEntitiesToBeRedacted (Union[str]): The PII entities to be redacted. Default is None.
        scoreThreshold (Optional[float]): The score threshold for redaction. Default is 0.4.
        auth (Depends): The authentication dependency.

    Returns:
        The response from the image anonymization process.

    Raises:
        NoMatchingRecognizer: If no matching recognizers were found to serve the request.
        NoAccountException: If the portfolio/account is incorrect.
        NoAdminConnException: If accounts and portfolio are not available with the subscription.
        HTTPException: If any other exception occurs during the image anonymization process.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"nlp":nlp if nlp!="" else None,"portfolio":portfolio if portfolio != "" else None ,"account":account if account !="" else None,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted if piiEntitiesToBeRedacted !="" else None,"exclusion":exclusionList if exclusionList !="" else None,"scoreThreshold":scoreThreshold}
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

@router.post('/privacy/multipleImage/analyze', response_model=List[PIIMultipleImageResponse])
def multipleImage_analyze(
    ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]),
    magnification: str = Form(...),
    rotationFlag: str = Form(...),
    image: List[UploadFile] = File(...),
    nlp: str = Form(default=None, example="basic/good/roberta/ranha"),
    portfolio: Optional[str] = Form(None),
    account: Optional[str] = Form(None),
    exclusionList: Optional[str] = Form(None),
    piiEntitiesToBeRedacted: Optional[str] = Form(None),
    scoreThreshold:Optional[float] = Form(default=float(0.4)),
    auth=Depends(auth)
):
    """
    Analyzes multiple images for privacy-related information.

    Args:
        ocr (str): The OCR engine to use for text extraction. Must be one of ['Tesseract', 'EasyOcr', 'ComputerVision'].
        magnification (str): The magnification ratio for the images.
        rotationFlag (str): The rotation flag for the images.
        image (List[UploadFile]): The list of images to analyze.
        nlp (str, optional): The NLP model to use for entity recognition. Defaults to None.
        portfolio (str, optional): The portfolio name. Defaults to None.
        account (str, optional): The account name. Defaults to None.
        exclusionList (str, optional): The exclusion list. Defaults to None.
        piiEntitiesToBeRedacted (str, optional): The PII entities to be redacted. Defaults to None.
        scoreThreshold (float, optional): The score threshold for entity recognition. Defaults to 0.4.
        auth: The authentication dependency.

    Returns:
        List[PIIMultipleImageResponse]: The list of responses containing the analyzed images and their associated PII entities.

    Raises:
        NoAccountException: If the portfolio or account is incorrect.
        NoAdminConnException: If the accounts and portfolio are not available with the subscription.
        NoMatchingRecognizer: If no matching recognizers were found to serve the request.
        HTTPException: If any other exception occurs during the analysis process.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_analyze routing method")
    try:
        payloads = []
        for i in image:
            payload = {
                "easyocr": ocr,
                "mag_ratio": magMap[magnification],
                "rotationFlag": magMap[rotationFlag],
                "image": i,
                "nlp": nlp if nlp != "" else None,
                "portfolio": portfolio if portfolio != "" else None,
                "account": account if account != "" else None,
                "piiEntitiesToBeRedacted": piiEntitiesToBeRedacted if piiEntitiesToBeRedacted != "" else None,
                "exclusion": exclusionList if exclusionList != "" else None,
                "scoreThreshold": scoreThreshold
            }
            payloads.append(payload)
        
        log.debug("Requested payloads: " + str(payloads))
        startTime = time.time()
        log.debug("Entered into image_analyze function")
        
        responses = []
        for payload in payloads:
            response = ImagePrivacy.image_analyze(payload)
            pii_entities = [PIIEntityImages(
                type=entity.type,
                beginOffset=entity.start,
                endOffset=entity.end,
                score=entity.score
            ) for entity in response.PIIEntities]
            responses.append(PIIMultipleImageResponse(
                filename=payload["image"].filename,
                PIIEntities=pii_entities
            ))
        
        ApiCall.delAdminList()
        log.debug("Returned from image_analyze function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken " + str(totalTime))
    
        for response in responses:
            if response.PIIEntities == 482:
                raise NoMatchingRecognizer
            if response.PIIEntities is None:
                raise NoAccountException
            if response.PIIEntities == 404:
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
        return responses
        
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

@router.post('/privacy/multipleImage/anonymize')
def multipleImage_anonymize(
    ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]),
    magnification: str = Form(...),
    rotationFlag: str = Form(...),
    image: List[UploadFile] = File(...),
    nlp: str = Form(default=None, example="basic/good/roberta/ranha"),
    portfolio: Union[str] = Form(None),
    account: Union[str] = Form(None),
    exclusionList: Union[str] = Form(None),
    piiEntitiesToBeRedacted: Union[str] = Form(None),
    scoreThreshold:Optional[float] = Form(default=float(0.4)),
    auth=Depends(auth)
):
    """
    Anonymizes multiple images.

    Args:
        ocr (str): The OCR engine to use. Valid options are 'Tesseract', 'EasyOcr', and 'ComputerVision'.
        magnification (str): The magnification ratio for the images.
        rotationFlag (str): The rotation flag for the images.
        image (List[UploadFile]): The list of images to be anonymized.
        nlp (str, optional): The NLP model to use. Defaults to None.
        portfolio (Union[str], optional): The portfolio name. Defaults to None.
        account (Union[str], optional): The account name. Defaults to None.
        exclusionList (Union[str], optional): The exclusion list. Defaults to None.
        piiEntitiesToBeRedacted (Union[str], optional): The PII entities to be redacted. Defaults to None.
        scoreThreshold (Optional[float], optional): The score threshold. Defaults to 0.4.
        auth: The authentication dependency.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the filename and the response for each image.

    Raises:
        PrivacyException: If an exception related to privacy occurs.
        NoAccountException: If the portfolio or account is incorrect.
        NoAdminConnException: If the accounts and portfolio are not available with the subscription.
        NoMatchingRecognizer: If no matching recognizers were found to serve the request.
        HTTPException: If any other exception occurs.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method")
    try:
        payloads = []
        for i in image:
            payload = {
                "easyocr": ocr,
                "mag_ratio": magMap[magnification],
                "rotationFlag": magMap[rotationFlag],
                "image": i,
                "nlp": nlp if nlp != "" else None,
                "portfolio": portfolio if portfolio != "" else None,
                "account": account if account != "" else None,
                "piiEntitiesToBeRedacted": piiEntitiesToBeRedacted if piiEntitiesToBeRedacted != "" else None,
                "exclusion": exclusionList if exclusionList != "" else None,
                "scoreThreshold": scoreThreshold
            }
            payloads.append(payload)
        
        log.debug("Payloads: " + str(payloads))
        startTime = time.time()
        log.debug("Entered into image_anonymize function")
        responses = []
        for payload in payloads:
            response = ImagePrivacy.image_anonymize(payload)
            responses.append({
                "filename": payload["image"].filename,
                "response": response
            })
        ApiCall.delAdminList()
        log.debug("Returned from image_anonymize function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken " + str(totalTime))
        for response in responses:
            if response == 482:
                raise NoMatchingRecognizer
            if response is None:
                raise NoAccountException
            if response == 404:
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
        return responses
        
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


# @router.post('/privacy/image/verify')
# def image_verify(image: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),auth= Depends(auth)):
#     id = uuid.uuid4().hex
#     request_id_var.set(id)
#     log.info("Entered create into image_verify routing method" )
#     try:
#         payload={"image":image,"nlp":nlp if nlp!="" else None,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
#         log.debug("request payload: "+str(payload))
#         startTime = time.time()
#         log.debug("Entered into image_verify function")
#         response = ImagePrivacy.image_verify(payload)
#         ApiCall.delAdminList()
#         log.debug("Returned from image_verify function")
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
      
        
#         log.info("exit create from image_verify routing method")
#         # telFlagData = TelemetryFlag.findall({"Module":"Privacy"})[0]
#         # tel_Falg = telFlagData["TelemetryFlag"]
#         log.debug("tel_Flag==="+ str(tel_Falg))
#         # responseList = list(map(lambda obj: obj.__dict__, response.PIIEntities))
#         if(tel_Falg == True):
#             log.debug("Inside Telemetry Flag")
#             # telemetryPayload = {
#             #     "uniqueid": id,
#             #     "tenant": "privacy",
#             #     "apiName": image_verify.__name__,
#             #     # "portfolio": portfolio,
#             #     # "accountName": account,
#             #     # "exclusion_list": exclusionList,
#             #     "request": payload,
#             #     "response": response
#             # }
#             # TelemetryDb.create(telemetryPayload)
            
#             # Trigger the API call asynchronously using a separate thread
#             # with concurrent.futures.ThreadPoolExecutor() as executor:
#             #     executor.submit(send_telemetry_request, privacy_telemetry_request)
#             log.info("******TELEMETRY REQUEST COMPLETED********")
#         return response
        
#     except PrivacyException as cie:
#         log.error("Exception for image_verify")
#         log.error(cie.__dict__)
#         # ExceptionDb.create({"UUID":id,"function":"imageVerifyRouter","msg":cie.__dict__,"description":cie.__dict__})
#         er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
#         er=[{"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":cie.__dict__,"description":cie.__dict__}]
#         er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
#         logobj = {"uniqueid":id,"error":er}
        
#         if len(er)!=0:
#             thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj,id))
#             thread.start()
#             if request_id_var.get() in error_dict:
#                 del error_dict[id] 
#         log.error(cie, exc_info=True)
#         log.info("exit create from image_verify routing method")
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
#         # ExceptionDb.create({"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
#         er=[{"tenetName":"Privacy","errorCode":"imageVerifyRouter","errorMessage":str(e)+"Line No:"+str(e.__traceback__.tb_lineno),"apiEndPoint":"/privacy/image/verify", "errorRequestMethod":"POST"}]
#         # er=[{"UUID":request_id_var.get(),"function":"imageVerifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
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
    
    
@router.post('/privacy/image/hashify')
def image_hashify(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),image: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),piiEntitiesToBeHashified:Union[str]=Form(None),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth= Depends(auth)):
    """
    Hashify an image and perform privacy-related operations.

    Args:
        ocr (str): The OCR engine to be used. Must be one of 'Tesseract', 'EasyOcr', or 'ComputerVision'.
        magnification (str): The magnification ratio for the image.
        rotationFlag (str): The rotation flag for the image.
        image (UploadFile): The image file to be processed.
        nlp (str): The NLP model to be used. Default is None.
        piiEntitiesToBeHashified (Union[str]): The PII entities to be hashified. Default is None.
        portfolio (Optional[str]): The portfolio name. Default is None.
        account (Optional[str]): The account name. Default is None.
        exclusionList (Optional[str]): The exclusion list. Default is None.
        scoreThreshold (Optional[float]): The score threshold. Default is 0.4.
        auth (Depends): The authentication dependency.

    Returns:
        The response from the image encryption operation.

    Raises:
        PrivacyException: If there is an exception during the image encryption operation.
        NoAccountException: If the portfolio or account is incorrect.
        NoAdminConnException: If the accounts and portfolio are not available with the subscription.
        HTTPException: If there is a general exception during the image encryption operation.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into imageEncryption routing method" )
    try:
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"image":image,"nlp":nlp if nlp!="" else None,"piiEntitiesToBeHashified":piiEntitiesToBeHashified if piiEntitiesToBeHashified !="" else None,"portfolio":portfolio,"account":account,"exclusion":exclusionList,"scoreThreshold":scoreThreshold}
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
    
@router.post('/privacy/multipleImage/hashify')
def multipleImage_hashify(
    ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]),
    magnification: str = Form(...),
    rotationFlag: str = Form(...),
    image: List[UploadFile] = File(...),
    nlp: str = Form(default=None, example="basic/good/roberta/ranha"),
    piiEntitiesToBeHashified: Union[str] = Form(None),
    portfolio: Optional[str] = Form(None),
    account: Optional[str] = Form(None),
    exclusionList: Optional[str] = Form(None),
    scoreThreshold:Optional[float] = Form(default=float(0.4)),
    auth=Depends(auth)
):
    """
    Hashify multiple images with privacy settings.

    Args:
        ocr (str): The OCR engine to use. Valid options are 'Tesseract', 'EasyOcr', and 'ComputerVision'.
        magnification (str): The magnification ratio for the images.
        rotationFlag (str): The rotation flag for the images.
        image (List[UploadFile]): The list of images to hashify.
        nlp (str): The NLP model to use. Default is None.
        piiEntitiesToBeHashified (Union[str]): The PII entities to be hashified. Default is None.
        portfolio (Optional[str]): The portfolio name. Default is None.
        account (Optional[str]): The account name. Default is None.
        exclusionList (Optional[str]): The exclusion list. Default is None.
        scoreThreshold (Optional[float]): The score threshold. Default is 0.4.
        auth: The authentication dependency.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the filename and the response for each image.

    Raises:
        PrivacyException: If there is an exception during the image encryption process.
        NoAccountException: If the portfolio/account is incorrect.
        NoAdminConnException: If the accounts and portfolio are not available with the subscription.
        HTTPException: If there is an error during the image encryption process.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into imageEncryption routing method")
    try:
        payloads = []
        for i in image:
            payload = {
                "easyocr": ocr,
                "mag_ratio": magMap[magnification],
                "rotationFlag": magMap[rotationFlag],
                "image": i,
                "nlp": nlp if nlp != "" else None,
                "piiEntitiesToBeHashified": piiEntitiesToBeHashified if piiEntitiesToBeHashified != "" else None,
                "portfolio": portfolio,
                "account": account,
                "exclusion": exclusionList,
                "scoreThreshold":scoreThreshold
            }
            payloads.append(payload)
        
        log.debug("Payloads: " + str(payloads))
        startTime = time.time()
        log.debug("Entered into imageEncryption function")
        
        responses = []
        for payload in payloads:
            response = ImagePrivacy.imageEncryption(payload)
            responses.append({
                "filename": payload["image"].filename,
                "response": response
            })
        
        ApiCall.delAdminList()
        log.debug("Returned from imageEncryption function")
        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken " + str(totalTime))
        
        for response in responses:
            if response["response"] is None:
                raise NoAccountException
            if response["response"] == 404:
                raise NoAdminConnException
        
        log.info("exit create from imageEncryption routing method")
        log.debug("tel_Flag===" + str(tel_Falg))
        if tel_Falg:
            log.debug("Inside Telemetry Flag")
            # telemetryPayload = {
            #     "uniqueid": id,
            #     "tenant": "privacy",
            #     "apiName": image_hashify.__name__,
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
        
        return responses
        
    except PrivacyException as cie:
        log.error("Exception for imageEncryption")
        log.error(cie.__dict__)
        # ExceptionDb.create({"UUID":id,"function":"imageHashifyRouter","msg":cie.__dict__,"description":cie.__dict__})
        er = [{"tenetName": "Privacy", "errorCode": "imageVerifyRouter", "errorMessage": str(cie) + "Line No:" + str(cie.__traceback__.tb_lineno), "apiEndPoint": "/privacy/image/verify", "errorRequestMethod": "POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageHashifyRouter","msg":cie.__dict__,"description":cie.__dict__}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}
        
        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
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
        er = [{"tenetName": "Privacy", "errorCode": "imageVerifyRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/image/verify", "errorRequestMethod": "POST"}]
        # er=[{"UUID":request_id_var.get(),"function":"imageHashifyRouter","msg":str(e),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)}]
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

 
 
   
@router.post('/privacy/dicom/anonymize')
def dicom_anonymize(payload: UploadFile = File(...),auth= Depends(auth)):
    """
    Anonymizes DICOM images.

    Args:
        payload (UploadFile): The DICOM image file to be anonymized.
        auth (Depends): The authentication dependency.

    Returns:
        The anonymized DICOM image.

    Raises:
        NoAccountException: If the account is not found.
        NoAdminConnException: If the admin connection is not established.
        PrivacyException: If there is an exception during the anonymization process.
        HTTPException: If there is an error during the anonymization process.
    """
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

 
## PAYLOAD CHANGED TO ACCEPT TEXT IN A STRUCTURED FORMAT AND GET RESPONSE FOR THE SAME
from starlette.responses import PlainTextResponse
@router.post('/privacy/code/anonymize',response_class=PlainTextResponse)
async def code_redaction(payload_text: str = Body(..., media_type="text/plain", description="The code to be anonymized"),
                        accountName: str = Query("None", description="account name"),
                        portfolioName: str = Query("None", description="portfolio name"),
                         portauth= Depends(auth)):
    """
    Anonymizes the provided code text and sends telemetry request.

    Args:
        payload_text (str): The code to be anonymized.
        accountName (str): The account name.
        portfolioName (str): The portfolio name.
        portauth: The authentication dependency.

    Returns:
        PlainTextResponse: The response as plain text, maintaining the format.

    Raises:
        PrivacyException: If an exception occurs during code anonymization.

    """
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
        log.debug("TelFlag==="+ str(tel_Falg))
        if(tel_Falg == True):
            telemetryPayload = {
                "uniqueid": id,
                "tenant": "privacy",
                "apiname": "CodeText Annonymize",           
                "user": "None",
                "date":now.isoformat(),
                "lotNumber": "None",
                # "exclusionList": payload.exclusionList,
                "request": {
                "portfolio_name": portfolioName,
                "account_name": accountName,
                "exclusion_list": [
                  "None"
                ],
                "inputText": payload_text
              },
                "response": [
                {
                  "type": "None",
                  "beginOffset": 0,
                  "endOffset": 0,
                  "score": 0,
                  "responseText": response
                }
              ]
            }
            # Trigger the API call asynchronously using a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_telemetry_request, telemetryPayload)
            log.info("******TELEMETRY REQUEST COMPLETED********")
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
async def code_anonymize(code_file: UploadFile = File(...),
                         accountName: str = Body("None", description="Enter account name"),
                         portfolioName: str = Body("None", description="Enter portfolio name")):
    """
    Anonymizes the code file by performing code redaction.

    Args:
        code_file (UploadFile): The code file to be anonymized.
        accountName (str): The account name.
        portfolioName (str): The portfolio name.

    Returns:
        StreamingResponse: The redacted code content as a response with the correct filename.

    Raises:
        PrivacyException: If an exception occurs during code redaction.
        HTTPException: If an exception occurs during code redaction and the status code is 500.
    """
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into filener routing method")
    try:
        # Read the file content from the UploadFile object
        code_content = await code_file.read()
        # Perform code redaction
        startTime = time.time()
        log.debug("Entered into filener function")
        redacted_content, output_code_file = codeNer.codeFile(code_content, code_file.filename, model, tokenizer)
        log.debug("Returned from filener function")
        if isinstance(redacted_content, str):
            redacted_content = redacted_content.encode('utf-8')

        endTime = time.time()
        totalTime = endTime - startTime
        log.info("Total Time taken " + str(totalTime))
        headers = {
            "Content-Disposition": f"attachment; filename={output_code_file}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }

        # Delete the uploaded file
        await code_file.close()
        output_code_file = os.path.splitext(code_file.filename)[0] + "_redacted" + os.path.splitext(code_file.filename)[1]
        os.remove(output_code_file)
        log.debug("TelFlag===" + str(tel_Falg))
        if tel_Falg:
            telemetryPayload = {
                "uniqueid": id,
                "tenant": "privacy",
                "apiname": "CodeFile Annonymize",
                "user": "None",
                "date": datetime.now().isoformat(),
                "lotNumber": "None",
                "request": {
                    "portfolio_name": portfolioName,
                    "account_name": accountName,
                    "exclusion_list": ["None"],
                    "inputText": code_content.decode('utf-8') if isinstance(code_content, bytes) else code_content
                },
                "response": [{
                    "type": "None",
                    "beginOffset": 0,
                    "endOffset": 0,
                    "score": 0,
                    "responseText": redacted_content.decode('utf-8') if isinstance(redacted_content, bytes) else redacted_content
                }]
            }
            # Convert telemetryPayload to JSON and print it
            log.debug("telemetryPayload=" + json.dumps(telemetryPayload, indent=4))

            # Trigger the API call asynchronously using a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_telemetry_request, telemetryPayload)
            log.info("******TELEMETRY REQUEST COMPLETED********")

        # Return the redacted code content as a response with the correct filename
        return StreamingResponse(BytesIO(redacted_content), media_type="application/octet-stream", headers=headers)
    except PrivacyException as cie:
        log.error("Exception for filener")
        log.error(cie, exc_info=True)
        er = [{"tenetName": "Privacy", "errorCode": "codeFileAnonimyzeRouter", "errorMessage": str(cie) + "Line No:" + str(cie.__traceback__.tb_lineno), "apiEndPoint": "/privacy/codefile/anonymize", "errorRequestMethod": "POST"}]
        er.extend(error_dict[request_id_var.get()] if request_id_var.get() in error_dict else [])
        logobj = {"uniqueid": id, "error": er}

        if len(er) != 0:
            thread = threading.Thread(target=Telemetry.error_telemetry_request, args=(logobj, id))
            thread.start()
            if request_id_var.get() in error_dict:
                del error_dict[id]
        raise cie
    except Exception as e:
        log.error(str(e))
        er = [{"tenetName": "Privacy", "errorCode": "codeFileAnonimyzeRouter", "errorMessage": str(e) + "Line No:" + str(e.__traceback__.tb_lineno), "apiEndPoint": "/privacy/codefile/anonymize", "errorRequestMethod": "POST"}]
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
            headers={"X-Error": "Please check with administration!!"})




# # from privacy.service.test import Test
# @router.get('/privacy/pii/video/anonymizea')
# async def image_analyze():
#     try:
#         log.info("Entered create usecase routing method" )
#         # payload={"image":image,"portfolio":portfolio,"account":account,"exclusion":exclusionList}
#         # response =VideoAnalyzer.anonymize(payload)
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
    
    """
    Uploads a file for differential privacy processing.

    Args:
        dataset (UploadFile): The file to be uploaded.
        auth: The authentication dependency.

    Returns:
        The response from the differential privacy processing.

    Raises:
        PrivacyException: If there is an exception during the differential privacy processing.
        NoAccountException: If the portfolio/account is incorrect.
        HTTPException: If there is an error during the processing.

    """
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into uploadFIle routing method" )
    try:
        # payload={"excel":excel}
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
        # if(tel_Falg == True):
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
    """
    Anonymizes data using differential privacy.

    Args:
        suppression (Optional[str], optional): The suppression parameter. Defaults to Form("").
        noiselist (Optional[str], optional): The noiselist parameter. Defaults to Form("").
        binarylist (Optional[str], optional): The binarylist parameter. Defaults to Form("").
        rangeList (Optional[str], optional): The rangeList parameter. Defaults to Form("").
        auth: The authentication dependency.

    Returns:
        StreamingResponse: The anonymized data as a streaming response.

    Raises:
        PrivacyException: If there is an exception related to privacy.
        NoAccountException: If the portfolio/account is incorrect.
        HTTPException: If there is any other exception.

    """
   
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into diffPrivacy routing method" )
    try:
        # log.info("Entered create usecase routing method" )
        # payload={"excel":excel}
        payload={"suppression":suppression,"noiselist":noiselist,"binarylist":binarylist,"rangelist":rangeList}
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
        # if(tel_Falg == True):
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
@fileRouter.post('/privacy-files/loadRecognizer')
def loadRecognizer(payload:UploadFile = File(...)):
    """
    Load the recognizer with the given payload.

    Args:
        payload (UploadFile): The file to be used for loading the recognizer.

    Returns:
        dict: The response from the LoadRecognizer.set_recognizer method.

    Raises:
        HTTPException: If an error occurs during the loading process.
    """
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

@fileRouter.get('/privacy-files/getRecognizer')
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
   
@fileRouter.post('/privacy-files/video/anonymize')
async def videoPrivacy(ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),magnification:str=Form(...),rotationFlag:str=Form(...),video: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth= Depends(auth)):
    # payload = {"video": video, "easyocr": ocr}
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        payload={"easyocr":ocr,"mag_ratio":magMap[magnification],"rotationFlag":magMap[rotationFlag],"video":video,"nlp":nlp if nlp!="" else None,"portfolio":portfolio,"account":account,"exclusion":exclusionList,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"scoreThreshold":scoreThreshold}
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
async def PDF(pdf:UploadFile=File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"),ocr: str = Query('Tesseract', enum=['Tesseract',"EasyOcr","ComputerVision"]),portfolio:Optional[str]=Form(None),account:Optional[str]=Form(None),exclusionList:Optional[str]=Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth= Depends(auth)):
    # payload = {"video": video, "easyocr": ocr}
    """
    An asynchronous function that processes a PDF file for privacy masking.

    Parameters:
    - pdf (UploadFile): The PDF file to be processed.
    - nlp (str): The NLP model to be used for text analysis. Default is None.
    - ocr (str): The OCR engine to be used for text extraction. Default is 'Tesseract'.
    - portfolio (Optional[str]): The portfolio associated with the PDF. Default is None.
    - account (Optional[str]): The account associated with the PDF. Default is None.
    - exclusionList (Optional[str]): A list of entities to be excluded from redaction. Default is None.
    - piiEntitiesToBeRedacted (Optional[str]): A list of PII entities to be redacted. Default is None.
    - scoreThreshold (Optional[float]): The threshold for redaction confidence score. Default is 0.4.
    - auth (Depends): The authentication dependency.

    Returns:
    - Response: The processed PDF file as a response with the appropriate headers.

    Raises:
    - PrivacyException: If there is an exception during privacy masking.
    - NoAccountException: If the portfolio or account is incorrect.
    - HTTPException: If there is any other exception during processing.
    """
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method" )
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service ")

        payload={"easyocr":ocr,"mag_ratio":False,"rotationFlag":False,"file": pdf,"nlp":nlp if nlp!="" else None,"portfolio":portfolio,"account":account,"exclusion":exclusionList,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"scoreThreshold":scoreThreshold}
      
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
async def PPT(ppt: UploadFile = File(...),nlp:str=Form(default=None,example="basic/good/roberta/ranha"), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None), scoreThreshold:Optional[float] = Form(default=float(0.4)),auth=Depends(auth)):
    """
    Process a PowerPoint presentation file for privacy protection.

    Args:
        ppt (UploadFile): The PowerPoint presentation file to be processed.
        nlp (str, optional): The NLP model to be used for text analysis. Defaults to None.
        ocr (str, optional): The OCR engine to be used for text extraction. Defaults to 'Tesseract'.
        portfolio (str, optional): The portfolio associated with the presentation. Defaults to None.
        account (str, optional): The account associated with the presentation. Defaults to None.
        exclusionList (str, optional): The list of words to be excluded from redaction. Defaults to None.
        piiEntitiesToBeRedacted (str, optional): The list of PII entities to be redacted. Defaults to None.
        scoreThreshold (float, optional): The threshold for redaction score. Defaults to 0.4.
        auth: The authentication dependency.

    Returns:
        Response: The processed PowerPoint presentation file as a response.

    Raises:
        PrivacyException: If there is an exception during the privacy protection process.
        NoAccountException: If the portfolio or account is incorrect.
        HTTPException: If there is a general exception during the process.
    """
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method")
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service")

        payload = {"easyocr": ocr, "mag_ratio": False, "rotationFlag": False, "file": ppt,"nlp":nlp if nlp!="" else None, "portfolio": portfolio, "account": account, "exclusion": exclusionList,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"scoreThreshold":scoreThreshold}

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
async def DOCX(docx: UploadFile = File(...), nlp:str=Form(default=None,example="basic/good/roberta/ranha"),ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None), piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth=Depends(auth)):
    """
    Process the given DOCX file for privacy redaction.

    Args:
        docx (UploadFile): The DOCX file to be processed.
        nlp (str): The NLP model to be used for redaction. Default is None.
        ocr (str): The OCR engine to be used for text extraction. Default is 'Tesseract'.
        portfolio (str, optional): The portfolio information. Default is None.
        account (str, optional): The account information. Default is None.
        exclusionList (str, optional): The list of entities to be excluded from redaction. Default is None.
        piiEntitiesToBeRedacted (str, optional): The list of PII entities to be redacted. Default is None.
        scoreThreshold (float, optional): The threshold for redaction confidence score. Default is 0.4.
        auth: The authentication dependency.

    Returns:
        Response: The processed DOCX file as a response with appropriate headers.

    Raises:
        PrivacyException: If there is an exception during the privacy redaction process.
        NoAccountException: If the portfolio or account information is incorrect.
        HTTPException: If there is a general exception during the process.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create into image_anonymize routing method")
    try:
        start_time = datetime.now()
        log.info(f"start_time: {start_time}")
        log.info("Before invoking create usecase service")

        payload = {"easyocr": ocr, "mag_ratio": False, "rotationFlag": False, "file": docx,"nlp":nlp if nlp!="" else None, "portfolio": portfolio, "account": account, "exclusion": exclusionList,"piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,"scoreThreshold":scoreThreshold}

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

@fileRouter.post('/privacy-files/csv/anonymize')
def csv_anonymize(file: UploadFile = File(...), keys_to_skip: Union[str, None] = Form(None), nlp: str = Form(default=None, example="basic/good/roberta/ranha"), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),fakeData: Optional[bool] = Form(False),auth=Depends(auth)):
    """
    Anonymizes a CSV file based on the provided parameters.

    Args:
        file (UploadFile): The CSV file to be anonymized.
        keys_to_skip (Union[str, None], optional): Comma-separated list of keys to skip during anonymization. Defaults to None.
        nlp (str, optional): NLP model to use for anonymization. Defaults to None.
        ocr (str, optional): OCR engine to use for text extraction. Defaults to 'Tesseract'.
        portfolio (Optional[str], optional): Portfolio information. Defaults to None.
        account (Optional[str], optional): Account information. Defaults to None.
        exclusionList (Optional[str], optional): List of entities to exclude from anonymization. Defaults to None.
        piiEntitiesToBeRedacted (Optional[str], optional): List of PII entities to be redacted. Defaults to None.
        scoreThreshold (Optional[float], optional): Threshold for PII detection score. Defaults to 0.4.
        fakeData (Optional[bool], optional): Flag to indicate whether to generate fake data. Defaults to False.
        auth (Depends(auth), optional): Authentication dependency. Defaults to None.

    Returns:
        Response: An HTTP response containing the anonymized CSV file as a text/csv attachment.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered csv_anonymize routing method")
    
    try:
        payload = {
            "file": file,
            "keys_to_skip": keys_to_skip.split(',') if keys_to_skip else None,
            "nlp":nlp if nlp!="" else "basic",
            "portfolio": portfolio, 
            "account": account, 
            "exclusion": exclusionList,
            "piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,
            "fakeData": fakeData,
            "scoreThreshold":scoreThreshold

        }
        log.debug("Payload: " + str(payload))
        start_time = time.time()
        output = CSVService.csv_anonymize(payload)
        end_time = time.time()
        total_time = end_time - start_time
        log.info("Total Time taken " + str(total_time))
        log.info("Exiting csv_anonymize routing method")
        print(output)
        return Response(output.getvalue(), media_type='text/csv', headers={'Content-Disposition': 'attachment; filename=anonymized.csv'})
    except Exception as e:
        log.error(str(e))
        raise e


@fileRouter.post('/privacy-files/json/anonymize')
def anonymize_json(file: UploadFile = File(...), keys_to_skip: Union[str, None] = Form(None),  nlp: str = Form(default=None, example="basic/good/roberta/ranha"), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)),auth=Depends(auth)):
    """
    Anonymizes a JSON file based on the provided parameters.

    Args:
        file (UploadFile): The JSON file to be anonymized.
        keys_to_skip (Union[str, None], optional): Comma-separated list of keys to skip during anonymization. Defaults to None.
        nlp (str, optional): NLP model to use for anonymization. Defaults to None.
        ocr (str, optional): OCR engine to use for anonymization. Defaults to 'Tesseract'.
        portfolio (Optional[str], optional): Portfolio information. Defaults to None.
        account (Optional[str], optional): Account information. Defaults to None.
        exclusionList (Optional[str], optional): List of entities to exclude from anonymization. Defaults to None.
        piiEntitiesToBeRedacted (Optional[str], optional): List of PII entities to be redacted. Defaults to None.
        scoreThreshold (Optional[float], optional): Threshold for anonymization score. Defaults to 0.4.
        auth (Depends(auth), optional): Authentication dependency. Defaults to None.

    Returns:
        Response: Anonymized JSON response with the appropriate headers.
    """
   
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered anonymize_json routing method")
    try:
        payload = {
            "file": file,
            "keys_to_skip": keys_to_skip.split(',') if keys_to_skip else None,
            "nlp": nlp if nlp != "" else "basic",
            "easyocr": ocr,
            "portfolio": portfolio,
            "account": account,
            "exclusion": exclusionList,
            "piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,
             "scoreThreshold":scoreThreshold
        }
        print("Payload: " + str(payload))
        start_time = time.time()
        anonymized_json = JSONService.anonymize_json(payload)
        end_time = time.time()
        total_time = end_time - start_time
        log.info("Total Time taken " + str(total_time))
        log.info("Exiting anonymize_json routing method")
        return Response(anonymized_json, media_type='application/json', headers={'Content-Disposition': 'attachment; filename=anonymized.json'})
    except Exception as e:
        log.error(str(e))
        raise e

from privacy.service.files_service import *

def get_file_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

@fileRouter.post('/privacy-files/anonymize')
def anonymize_file(file: UploadFile = File(...), nlp: str = Form(default=None, example="basic/good/roberta/ranha"), ocr: str = Query('Tesseract', enum=['Tesseract', "EasyOcr", "ComputerVision"]), portfolio: Optional[str] = Form(None), account: Optional[str] = Form(None), exclusionList: Optional[str] = Form(None), keys_to_skip: Union[str, None] = Form(None),piiEntitiesToBeRedacted:Optional[str]=Form(None),scoreThreshold:Optional[float] = Form(default=float(0.4)), auth=Depends(auth)):
    """
    Anonymizes the given file based on the provided parameters.

    Args:
        file (UploadFile): The file to be anonymized.
        nlp (str): The NLP model to be used for anonymization. Default is 'basic/good/roberta/ranha'.
        ocr (str): The OCR engine to be used for text extraction. Default is 'Tesseract'.
        portfolio (Optional[str]): The portfolio associated with the file. Default is None.
        account (Optional[str]): The account associated with the file. Default is None.
        exclusionList (Optional[str]): A comma-separated list of words to be excluded from anonymization. Default is None.
        keys_to_skip (Union[str, None]): A comma-separated list of keys to skip during anonymization. Default is None.
        piiEntitiesToBeRedacted (Optional[str]): A comma-separated list of PII entities to be redacted. Default is None.
        scoreThreshold (Optional[float]): The threshold score for anonymization. Default is 0.4.
        auth: The authentication dependency.

    Returns:
        StreamingResponse: The anonymized file as a streaming response.

    Raises:
        HTTPException: If an error occurs during file anonymization.
    """
    
    id = uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered anonymize_file routing method")
    try:
        file_extension = get_file_extension(file.filename)
        payload = {
            "file": file,
            "nlp": nlp if nlp != "" else "basic",
            "easyocr": ocr,
            "portfolio": portfolio,
            "account": account,
            "mag_ratio": False,
            "rotationFlag":False,
            "exclusion": exclusionList,
            "piiEntitiesToBeRedacted":piiEntitiesToBeRedacted,
            "keys_to_skip": keys_to_skip.split(',') if keys_to_skip else None,
            "scoreThreshold":scoreThreshold
        }
        log.debug("Payload: " + str(payload))
        start_time = time.time()
        response_file = FileService.anonymize_file(payload, file_extension)
        end_time = time.time()
        total_time = end_time - start_time
        log.info("Total Time taken " + str(total_time))
        log.info("Exiting anonymize_file routing method")
        
        media_type = 'application/octet-stream'
        if file_extension == 'csv':
            media_type = 'text/csv'
        elif file_extension == 'json':
            media_type = 'application/json'
        elif file_extension == 'pdf':
            media_type = 'application/pdf'
        elif file_extension == 'ppt':
            media_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif file_extension == 'docx':
            media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        return StreamingResponse(response_file, media_type=media_type, headers={"Content-Disposition": f"attachment; filename=anonymized.{file_extension}"})
    except Exception as e:
        log.error(str(e))
        raise HTTPException(status_code=500, detail="An error occurred during file anonymization.")