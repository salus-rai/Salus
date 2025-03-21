'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pickle
import torch
import os
import time
import logging
from flask import Flask, render_template, request, jsonify
from flask import g
from datetime import datetime
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer,util
from detoxify import Detoxify
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from dao.AdminDb import Results
from werkzeug.exceptions import HTTPException,BadRequest,UnprocessableEntity,InternalServerError
from tqdm.auto import tqdm
from fastapi.encoders import jsonable_encoder


import numpy as np

import traceback
import uuid
from waitress import serve
from mapper.mapper import *
import contextvars

app = Flask(__name__)
print("before loading model")
request_id_var = contextvars.ContextVar("request_id_var")
#pipe = StableDiffusionPipeline.from_pretrained('/model/stablediffusion/fp32/model')
device = "cuda"
registry = RecognizerRegistry()
registry.load_predefined_recognizers()
analyzer_engine = AnalyzerEngine(registry=registry)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
gpu=0 if torch.cuda.is_available() else -1
check_point = 'toxic_debiased-c7548aa0.ckpt'
toxicityModel = Detoxify(checkpoint='../models/detoxify/'+ check_point,
                        device=device,
                        huggingface_config_path='../models/detoxify')

PromptModel_dberta = AutoModelForSequenceClassification.from_pretrained("../models/dbertaInjection").to(device)
Prompttokens_dberta = AutoTokenizer.from_pretrained("../models/dbertaInjection")

topictokenizer_Facebook = AutoTokenizer.from_pretrained("../models/facebook")
topicmodel_Facebook = AutoModelForSequenceClassification.from_pretrained("../models/facebook").to(device)

topictokenizer_dberta = AutoTokenizer.from_pretrained("../models/restricted-dberta-large-zeroshot")
topicmodel_dberta = AutoModelForSequenceClassification.from_pretrained("../models/restricted-dberta-large-zeroshot").to(device)

# classifier = pipeline("zero-shot-classification",model="../models/facebook",device=device)
# classifier2 = pipeline("zero-shot-classification",model="../models/restricted-dberta-large-zeroshot",device=device)
encoder = SentenceTransformer("../models/multi-qa-mpnet-base-dot-v1").to(device)
jailbreakModel = encoder
similarity_model =encoder
request_id_var.set("Startup")
log_dict={}
print("model loaded")

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "details": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(UnprocessableEntity)
def validation_error_handler(exc):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = exc.get_response()
        print(response)
        # replace the body with JSON
        exc_code_desc=exc.description.split("-")
        exc_code=int(exc_code_desc[0])
        exc_desc=exc_code_desc[1]
        response.data = json.dumps({
            "code": exc_code,
            "details":  exc_desc,
        })
        response.content_type = "application/json"
        return response

@app.errorhandler(InternalServerError)
def validation_error_handler(exc):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = exc.get_response()
        print(response)
        # replace the body with JSON
        response.data = json.dumps({
            "code": 500,
            "details": "Some Error Occurred ,Please try Later",
        })
        response.content_type = "application/json"
        return response

@app.route("/rai/v2test/raimoderationmodels/detoxifymodel",methods=[ 'POST'])
def toxic_model():
    st=time.time()
    
    try:
        
        id=uuid.uuid4().hex
        payload=request.get_json()
        request_id_var.set(id)
        logging.info("before invoking toxic_model service ")
        log_dict[request_id_var.get()]=[]
        if payload['text'] is None or (payload['text'] is not None and len(payload['text'])==0):
            raise UnprocessableEntity("1021-Input Text should not be empty ")
        response = toxicity_check(payload,id)
 
        logging.info("after invoking toxic_model service ")
        
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
	

        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        logging.info("exit toxic_model routing method")
        logging.info(f"Time taken by toxicity {time.time()-st}")
        return jsonable_encoder(response)
    except UnprocessableEntity as cie:
        logging.error(cie.__dict__)
        logging.info("exit toxic_model routing method")
        raise UnprocessableEntity(**cie.__dict__)
    except Exception as cie:
        logging.error(cie.__dict__)
        logging.info("exit toxic_model routing method")
        raise HTTPException()
    
@app.route("/rai/v2test/raimoderationmodels/privacy",methods=[ 'POST'])
def pii_check():
    st=time.time()
    logging.info("Entered pii_check routing method")
    try:
        
        id=uuid.uuid4().hex
        payload=request.get_json()
        request_id_var.set(id)
        logging.info("before invoking create usecase service ")
        log_dict[request_id_var.get()]=[]
        if payload['text'] is None or (payload['text'] is not None and len(payload['text'])==0) or payload['entitiesselected'] is None or (payload['entitiesselected'] is not None and len(payload['entitiesselected'])==0):
            raise UnprocessableEntity("1021-invalid input!")
        response = privacy(id,payload['text'],payload['entitiesselected'])
        logging.info("after invoking create usecase service ")
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        # logging.debug("response : " + str(response))
        logging.info("exit pii_check routing method")
        logging.info(f"Time taken by privacy {time.time()-st}")
        return jsonable_encoder(response)
    except Exception as cie:
        logging.error(cie.__dict__)
        logging.info("exit pii_check routing method")
        raise HTTPException()
    
@app.route("/rai/v2test/raimoderationmodels/promptinjectionmodel",methods=[ 'POST'])
def prompt_model():
    st=time.time()
    logging.info("Entered prompt_model routing method")
    try:
        
        id=uuid.uuid4().hex
        payload=request.get_json()
        request_id_var.set(id)
        logging.info("before invoking prompt_model service")
        log_dict[request_id_var.get()]=[]
        if payload['text'] is None or (payload['text'] is not None and len(payload['text'])==0):
            raise UnprocessableEntity("1021-Input Text should not be empty ")
        response = promptInjection_check(payload['text'],id)
        logging.info("after invoking prompt_model service ")
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        # logging.debug("response : " + str(response))
        logging.info("exit prompt_model routing method")
        logging.info(f"Time taken by promptinjection {time.time()-st}")
        return jsonable_encoder(response)
    except Exception as cie:
        logging.error(cie.__dict__)
        logging.info("exit prompt_model routing method")
        raise HTTPException()
    
@app.route("/rai/v2test/raimoderationmodels/restrictedtopicmodel",methods=[ 'POST'])
def restrictedTopic_model():
    st=time.time()
    logging.info("Entered restrictedTopic_model routing method")
    try:
        id=uuid.uuid4().hex
        payload=request.get_json()
        request_id_var.set(id)
        logging.info("before invoking restrictedTopic_model service ")
        log_dict[request_id_var.get()]=[]

        label_cond = payload['labels'] is None or (payload['labels'] is not None and len(payload['labels'])==0)
        model_cond=False
        # print("--")
        if("model" in payload):
            model_cond = payload['model'] is None or (payload['model'] is not None and len(payload['model'])==0)
        # print("==")
        if payload['text'] is None or (payload['text'] is not None and len(payload['text'])==0) or label_cond or model_cond:
            raise UnprocessableEntity("1021-invalid input ")
        response = restricttopic_check(payload,id)
        logging.info("after invoking restrictedTopic_model service ")
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        # logging.debug("response : " + str(response))
        logging.info("exit restrictedTopic_model routing method")
        logging.info(f"Time taken by RestrictedTopic{time.time()-st}")
        # print(type(response))
        # print(type(jsonable_encoder(response)))
        return jsonable_encoder(response)
    except Exception as cie:
        
        logging.error(cie.__dict__)
        logging.info("exit restrictedTopic_model routing method")
        raise HTTPException()
    
@app.route("/rai/v2test/raimoderationmodels/multi_q_net_embedding",methods=[ 'POST'])
def embedding_model():
    st=time.time()
    logging.info("Entered embedding_model routing method")
    try:
        
        id=uuid.uuid4().hex
        payload=request.get_json()
        request_id_var.set(id)
        logging.info("before invoking embedding_model service ")
        log_dict[request_id_var.get()]=[]
        if payload['text'] is None or (payload['text'] is not None and len(payload['text'])==0):
            raise UnprocessableEntity("1021-Input Text should not be empty ")
        response = multi_q_net_embedding(id,payload['text'])
        logging.info("after invoking embedding_model service ")
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        # logging.debug("response : " + str(response))
        logging.info("exit embedding_model routing method")
        logging.info(f"Time taken by Jailbreak {time.time()-st}")
        return jsonable_encoder(response)
    except Exception as cie:
        logging.error(cie.__dict__)
        logging.info("exit embedding_model routing method")
        raise HTTPException()

@app.route("/rai/v2test/raimoderationmodels/multi-qa-mpnet-model_similarity",methods=[ 'POST'])
def similarity_model():
    st=time.time()
    logging.info("Entered similarity_model routing method")
    try:
        
        id=uuid.uuid4().hex
        request_id_var.set(id)
        logging.info("before invoking similarity_model service ")
        payload=request.get_json()
        log_dict[request_id_var.get()]=[]
        text1_cond = payload['text1'] is None or (payload['text1'] is not None and len(payload['text1'])==0)
        text2_cond = payload['text2'] is None or (payload['text2'] is not None and len(payload['text2'])==0)
        emb1_cond = payload['emb1'] is None or (payload['emb1'] is not None and len(payload['emb1'])==0)
        emb2_cond = payload['emb2'] is None or (payload['emb2'] is not None and len(payload['emb2'])==0)
        if text1_cond or text2_cond or emb1_cond or emb2_cond:
            raise UnprocessableEntity("1021-Input Text should not be empty ")
        response = multi_q_net_similarity(id,payload['text1'],payload['text2'],payload['emb1'],payload['emb2'])
        logging.info("after invoking similarity_model service ")
        er=log_dict[request_id_var.get()]
        logobj = {"_id":id,"error":er}
        if len(er)!=0:
            Results.createlog(logobj)
        del log_dict[id]
        logging.debug("response : " + str(response))
        # logging.debug("response : " + str(response))
        logging.info("exit similarity_model routing method")
        logging.info(f"Time taken by similary{time.time()-st}")
        return jsonable_encoder(response)
    except Exception as cie:
        logging.error(cie.__dict__)
        logging.info("exit similarity_model routing method")
        raise HTTPException()
    

def privacy(id,text,PIIenities_selected=None):  
    try:
        analyzer_results = analyzer_engine.analyze(text=text, language="en",entities=PIIenities_selected)
        entityList= []
        anyz_res = jsonable_encoder(analyzer_results)
        for i in anyz_res:
            entityList.append(i['entity_type'])
        return anyz_res,jsonable_encoder(entityList)
    except Exception as e:
             
            logging.error("Error occured in privacy")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at privacy call"})
            raise InternalServerError()
            

def multi_q_net_similarity(id,text1=None,text2=None,emb1=None,emb2=None):
    try:
        if text1:
            with torch.no_grad():
                emb1 = jailbreakModel.encode(text1, convert_to_tensor=True,device=device)
        if text2:
            with torch.no_grad():
                emb2 = jailbreakModel.encode(text2, convert_to_tensor=True,device=device)
        
        emb = util.pytorch_cos_sim(emb1, emb2).to("cpu").numpy().tolist()
        del emb1
        del emb2
        #torch.cuda.empty_cache()
        return emb
    except Exception as e:
             
            logging.error("Error occured in multi_q_net_similarity")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at multi_q_net_similarity call"})
            raise InternalServerError()
            

def multi_q_net_embedding(id,lst):
    try:
        res = []
        for text in lst:
            with torch.no_grad():
                text_embedding = jailbreakModel.encode(text, convert_to_tensor=True,device=device)
            res.append(text_embedding.to("cpu").numpy().tolist())

        del text_embedding
        #torch.cuda.empty_cache()
        return res
        # return text_embedding.numpy().tolist()
    except Exception as e:
             
            logging.error("Error occured in multi_q_net text embedding")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at multi_q_net text embedding call"})
            raise InternalServerError()
            

def restricttopic_check(payload,id): 
    try:
        # topicmodel = topicmodel_Facebook
        # topictokenizer = topictokenizer_Facebook

        # nlp = pipeline('zero-shot-classification', model=classifier, tokenizer=topictokenizer)

        text=payload['text']
        labels=payload['labels']
        
        model =payload['model'] if hasattr(payload, 'model') else "facebook"
        if model==None:
            model="dberta"
        
        if model=="facebook":
            # nlp = classifier
            nlp = pipeline('zero-shot-classification', model=topicmodel_Facebook, tokenizer=topictokenizer_Facebook, device=gpu)
        elif model=="dberta": 
            # nlp = classifier2
            nlp = pipeline('zero-shot-classification', model=topicmodel_dberta, tokenizer=topictokenizer_dberta,device=gpu)
        with torch.no_grad():    
            output=nlp(text, labels,multi_label=True)
        for i in range(len(output["scores"])):
            output["scores"][i] = round(output["scores"][i],4)

        del nlp
        #torch.cuda.empty_cache()
        return output
    
    except Exception as e:
             
            logging.error("Error occured in restricttopic_check")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at restricttopic_check call"})
            raise InternalServerError()

def toxicity_check(payload,id) :
    try:
        text = payload['text']
        with torch.no_grad():
            output = toxicityModel.predict(text)
        List_profanity_score = []
        obj_profanityScore_toxic = profanityScore(metricName='toxicity',
                                        metricScore=output['toxicity'])
        obj_profanityScore_severe_toxic = profanityScore(metricName='severe_toxicity',
                                        metricScore=output['severe_toxicity'])
        obj_profanityScore_obscene = profanityScore(metricName='obscene',
                                        metricScore=output['obscene'])
        obj_profanityScore_threat = profanityScore(metricName='threat',
                                        metricScore=output['threat'])
        obj_profanityScore_insult = profanityScore(metricName='insult',
                                        metricScore=output['insult'])
        obj_profanityScore_identity_attack = profanityScore(metricName='identity_attack',
                                        metricScore=output['identity_attack'])
        obj_profanityScore_sexual_explicit = profanityScore(metricName='sexual_explicit',
                                        metricScore=output['sexual_explicit'])
        
        List_profanity_score.append(obj_profanityScore_toxic)
        List_profanity_score.append(obj_profanityScore_severe_toxic)
        List_profanity_score.append(obj_profanityScore_obscene)
        List_profanity_score.append(obj_profanityScore_threat)
        List_profanity_score.append(obj_profanityScore_insult)
        List_profanity_score.append(obj_profanityScore_identity_attack)
        List_profanity_score.append(obj_profanityScore_sexual_explicit)

        objProfanityAnalyzeResponse = {}
        objProfanityAnalyzeResponse['toxicScore'] = List_profanity_score

        #torch.cuda.empty_cache()
        return objProfanityAnalyzeResponse
    
    except Exception as e:
             
            logging.error("Error occured in toxicity_check")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at toxicity_check call"})
            raise InternalServerError()
            
    
def promptInjection_check(text,id):
    try:

        Prompttokens = Prompttokens_dberta
        PromptModel = PromptModel_dberta

        tokens = Prompttokens.encode_plus(text, truncation=True, padding=True, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = PromptModel(**tokens)

        predicted_label = outputs.logits.argmax().item()
        label_names = PromptModel.config.id2label
        predicted_label_name = label_names[predicted_label]
        predicted_probabilities = outputs.logits.softmax(dim=1)[0, predicted_label].item()

        del tokens
        #torch.cuda.empty_cache()
        # #torch.cuda.empty_cache()
        return predicted_label_name,predicted_probabilities
    except Exception as e:
            
            logging.error("Error occured in promptInjection_check")
            logging.error(f"Exception: {e}")
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at promptInjection_check call"})
            raise InternalServerError()

@app.route("/")
def hello_world():
    return "<h1>Hello, world!</h1>"            

if __name__ == "__main__":
   serve(app, host='0.0.0.0', port=8000, threads=int(os.getenv('THREADS',1)),connection_limit=int(os.getenv('CONNECTION_LIMIT',500)), channel_timeout=int(os.getenv('CHANNEL_TIMEOUT',120)))
   #app.run()
