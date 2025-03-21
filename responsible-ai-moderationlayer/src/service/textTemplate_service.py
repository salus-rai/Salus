'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
########################################### IMPORT LIBRARIES ############################################

from langchain.prompts import PromptTemplate
import openai
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from config.prompt_templates import *
from config.logger import CustomLogger, request_id_var
import os
import json
from utilities.utility_methods import *
from utilities.lruCaching import *
import traceback
import re
import threading
from telemetry import telemetry
from dao.AdminDb import Results
import uuid
from datetime import datetime

########################################  Prompt Template  ##########################################
BASELINE_PROMPT = """You are a detail-oriented and highly analytical LLM to detect {detection_type} in the provided prompt.
        {evaluation_criteria}
        {prompting_instructions}
        {few_shot}
        Given the below User Query , generate an output with following fields separated by comma as shown below:
        {output_format}
        {task_data} 
        """


NORMAL_OUTPUT = """
"analysis": "[keep it crisp and to the point, including all necessary details]",
"score": [Assign a decimal score between 0-1]
"""

FAIRNESS_OUTPUT = """
"analysis": "[keep it crisp and to the point, including all necessary details]",
"score": [Assign a decimal score between 0-1],
"bias_type": "[mentions the bias type(s).The value here should be comma separated clear bias type(s), state None in case of no clear bias type(s)]",
"group": "[mentions the group(s) towards which there is a bias.The value here should be comma separated clear group(s), state None in case of no clear group(s)]"
"""

NAVI_OUTPUT = """
"analysis": "[keep it crisp and to the point, including all necessary details]",
"score": [Assign a decimal score between 0-1],
"role":"[role of LLM eg: expert,Advisory,Support]",
"Sentiment":"[this should show emotion state of user prompt eg: Positive - Upbeat]",
"Context":"[this will be coming context]"
"Domain":"[This should show Domain of topic]",
"outputBeforemoderation":"[This should show output before moderation]",
"outputAfterSentimentmoderation":"[This should show output before moderation]"
"""

TOXICITY_OUTPUT= """
"score":[
           {
            "metricName" : "Toxicity",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Severe Toxicity",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Insult",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Threat",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Obscene",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Hate speech",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Identity Attack",
            "metricScore" :[Assign a decimal score between 0-1]
           },
           {
            "metricName" : "Sexual Explicit",
            "metricScore" :[Assign a decimal score between 0-1]
           }
],
"category": "[mention the category of toxicity]",
"analysis": "[keep it crisp and to the point, including all necessary details]"
"""

RESTRICTED_TOPIC_OUTPUT = """
"analysis": "[keep it crisp and to the point, including all necessary details]",
"score": [Assign a decimal score between 0-1],
"category": "[mention the restricted topic being used]"
"""

TASK_DATA_FOR_REQ = """
Task Data.
[User Query]: {question}
[Output]:
"""

TASK_DATA_FOR_RESP = """
Task Data.
[User Query]: {question}
[Response]: {response}
[Output]:
"""
#######################################################################################################


log = CustomLogger()
log_dict={}
cache_ttl = int(os.getenv("CACHE_TTL"))
cache_size = int(os.getenv("CACHE_SIZE"))
cache_flag = os.getenv("CACHE_FLAG")

###############################   Template based Guardrails (LLM Evaluation) #######################

def get_gpt_response(prompt,modelName):
    MODEL_NAME,API_BASE,API_KEY,API_VERSION,API_TYPE = config(modelName)
    client = AzureOpenAI(api_key=API_KEY, 
                         azure_endpoint=API_BASE,
                         api_version=API_VERSION)
    resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages = [{"role": "user", "content": prompt}] ,
                temperature=0,
                max_tokens=500)
    llm_resp = resp.choices[0].message.content if len(resp.choices[0].message.content)!=0 else resp.choices[0].finish_reason
    return llm_resp



def get_output_format(template_name):
    if template_name=="Toxicity Check" or template_name=="Image Toxicity Check":
        return TOXICITY_OUTPUT
    elif template_name == "Restricted Topic Check" or template_name=="Image Restricted Topic Check":
        return RESTRICTED_TOPIC_OUTPUT
    elif template_name == "Fairness and Bias Check":
        return FAIRNESS_OUTPUT
    elif template_name == "Navi Tone Correctness Check":
        return NAVI_OUTPUT
    else:
        return NORMAL_OUTPUT
    


@lru_cache(ttl=cache_ttl,size=cache_size,flag=cache_flag)
def get_response(text,template_name,userId,modelName):
    MODEL_NAME,API_BASE,API_KEY,API_VERSION,API_TYPE = config(modelName)
    try:
        llm_resp = ""
        llm = AzureChatOpenAI(deployment_name=MODEL_NAME,
                                    openai_api_version=API_VERSION,
                                    openai_api_key=API_KEY,
                                    azure_endpoint=API_BASE,
                                    openai_api_type = API_TYPE,
                                    temperature = 0)
        
        final_prompt = PromptTemplate.from_template(BASELINE_PROMPT)
        final_chain = final_prompt | llm
        vars = get_templates(template_name,userId)

        if template_name.startswith("Response"):
             llm_resp = get_gpt_response(text,MODEL_NAME)


        response = final_chain.invoke({f"detection_type":template_name,
                                    "evaluation_criteria":vars["evaluation_criteria"],
                                    "prompting_instructions":vars["prompting_instructions"],
                                    "few_shot":vars["few_shot_examples"],
                                    "output_format":get_output_format(template_name),
                                    "task_data":TASK_DATA_FOR_RESP.format(**{"question":text,"response":llm_resp}) if template_name.startswith("Response") else TASK_DATA_FOR_REQ.replace("{question}",text)})
        
        content = response.dict()['content']
        for pattern in ("[Output]:\n","[Output] :\n","{{","}}","{","}"):
            content = content.replace(pattern,"")
        content=re.sub(r'(?<!")None(?!")','"None"',content)
        content = "{\n" + content + "\n}"

        if(text==""):
            log.info("Prompt is Empty")
            log_dict[request_id_var.get()].append("Prompt is Empty")
            return "Error Occured due to empty prompt" 
        
        print("content : ",content)
        response_dict = json.loads(content)
        
        response_dict['threshold']=0.6
        response_dict['score']=float(response_dict['score'])
        response_dict['result']="FAILED" if response_dict['score'] > response_dict['threshold'] else "PASSED"
       
        if response.dict()['response_metadata']['finish_reason'] == "content_filter":
            response_dict['analysis'] = "The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry. To learn more about our content filtering policies please read our documentation: https://go.microsoft.com/fwlink/?linkid=2198766"
            response_dict['score'] = -1
            response_dict['result'] = "Can't be determined"
        
        return response_dict
                
    except Exception as e:
        line_number = traceback.extract_tb(e.__traceback__)[0].lineno
        log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                   "Error Module":"Failed at Eval LLM model call"})
        log.error(f"Error occured in Chain to generate initial answer: {line_number,e}")




class TextTemplateService:
    def generate_response(self,req,headers,telemetryFlag=False):
        try:
            id = uuid.uuid4().hex
            request_id_var.set(id)
            headers['id']=id
            log_dict[request_id_var.get()]=[]
            AccountName=req.AccountName if "AccountName" in req else "None"
            PortfolioName=req.PortfolioName if "PortfolioName" in req else "None"
            userid = req.userid if "userid" in req else "None"
            lotNumber = str(req.lotNumber) if "lotNumber" in req else "None"
            
            final_response = {}
            if os.getenv("DBTYPE") != "False":# send request payload into DB #
                thread=threading.Thread(target=Results.createRequestPayload,args=("evalLLM",req,id,
                                                                                str(PortfolioName), 
                                                                    str(AccountName),userid,lotNumber))
                thread.start()
            
            try:
                st = time.time()
                response = get_response(req['Prompt'],req['template_name'],userid,req['model_name'])
                final_response = {'uniqueid':id,'userid': req.userid if "userid" in req else "None", 
                              'lotNumber': str(req.lotNumber) if "lotNumber" in req else "None", 
                              'created': str(datetime.now()),
                              'model': req.model_name,
                              'moderationResults':{'analysis':response['analysis'],
                                          'score':response['score'],
                                          'threshold':response['threshold'],
                                          'result':response['result']},
                              'evaluation_check':req['template_name'],
                              'timeTaken':str(round(time.time() - st, 3))+"s"}
        
                if req['template_name'] == "Fairness and Bias Check":
                    final_response['moderationResults'].update({
                        'bias_type':response['bias_type'] if 'bias_type' in response.keys() else "None",
                        'group':response['group'] if 'group' in response.keys() else "None"})
        
        
                if req.userid!="None":
                    for d in prompt_template[req.userid]:
                        if d["templateName"]==req['template_name']:
                            final_response['description'] = d["description"]
                
                starttime = time.time()
                if telemetryFlag==True: # sent response payload to Telemetry #
                    thread1 = threading.Thread(target=telemetry.send_evalLLM_telemetry_request, args=(final_response,id,lotNumber, PortfolioName, AccountName,userid))
                    thread1.start()
                log.debug(f"Time taken in adding to telemetry {time.time()-starttime}")

                if os.getenv("DBTYPE") != "False": # sent response payload to DB #
                    thread2=threading.Thread(target=Results.create,args=(final_response,id,str(PortfolioName), str(AccountName),userid,lotNumber))
                    thread2.start()

            except Exception as e:
                log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                    "Error Module":"Failed at Completion Function"})
                log.error(f"Error starting telemetry or DB thread: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
            
            er=log_dict[request_id_var.get()]
            logobj = {"_id":id,"error":er}
            if len(er)!=0:
                if os.getenv("DBTYPE") != "False":
                    Results.createlog(logobj)
                err_desc = er
                print("error---->>> ",err_desc)
                token_info = {"unique_name":"None","X-Correlation-ID":"None","X-Span-ID":"None"}
                thread_err = threading.Thread(target=telemetry.send_telemetry_error_request, args=(logobj,id,lotNumber,PortfolioName,AccountName,userid,err_desc,headers,token_info))
                thread_err.start()
                del log_dict[id]

            return final_response
        
        except Exception as e:
            line_number = traceback.extract_tb(e.__traceback__)[0].lineno
            log_dict[request_id_var.get()].append({"Line number":str(traceback.extract_tb(e.__traceback__)[0].lineno),"Error":str(e),
                                                    "Error Module":"Failed at Eval LLM model call"})
            log.error(f"Error occured in Chain to generate initial answer: {line_number,e}")


