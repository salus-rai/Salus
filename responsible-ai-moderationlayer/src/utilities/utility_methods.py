import os
from dotenv import load_dotenv
from config.logger import CustomLogger

load_dotenv()
prompt_template = {}
log = CustomLogger()

##########################################################################################################

# To get Templates from DB based on Detection Type
def get_templates(detection_type,userId):
    template = {}
    found = False
    data = prompt_template[userId]
    for d in data:
        if d['templateName'] == detection_type:
            found=True
            for s in d['subTemplates']:
                template[s['template']] = s['templateData']
            break 

    if not found:
        log.error(f"Invalid Detection type : {detection_type}")
        raise Exception("Invalid Detection Type")
    return template



# To get GPT Configurations from env file
def config(modelName):
    API_TYPE=os.getenv("OPENAI_API_TYPE")
    if modelName == "gpt3":
        MODEL_NAME = os.getenv("OPENAI_MODEL_GPT3")
        API_BASE = os.getenv("OPENAI_API_BASE_GPT3")
        API_KEY = os.getenv("OPENAI_API_KEY_GPT3")
        API_VERSION = os.getenv("OPENAI_API_VERSION_GPT3")
    elif modelName == "gpt4O":
        MODEL_NAME = os.getenv("OPENAI_MODEL_GPT4_O")
        API_BASE =  os.getenv('OPENAI_API_BASE_GPT4_O') 
        API_KEY = os.getenv('OPENAI_API_KEY_GPT4_O')           
        API_VERSION = os.getenv('OPENAI_API_VERSION_GPT4_O')
    else: # gpt4
        MODEL_NAME = os.getenv("OPENAI_MODEL_GPT4")
        API_BASE = os.getenv("OPENAI_API_BASE_GPT4")
        API_KEY = os.getenv("OPENAI_API_KEY_GPT4")
        API_VERSION = os.getenv("OPENAI_API_VERSION_GPT4")
    return MODEL_NAME,API_BASE,API_KEY,API_VERSION,API_TYPE