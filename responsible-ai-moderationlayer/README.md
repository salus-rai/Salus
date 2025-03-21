# Responsible-AI-Moderation Layer 

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Set Configuration Variables](#set-configuration-variables)
- [Running the Application](#running-the-application)
- [License](#license)
- [Contact](#contact)
 
## Introduction
The **Moderation Layer** module provides model-based and template-based guardrails to moderate inputs by passing them through various checks like check for toxicity, profanity, prompt injection, jailbreak, privacy etc. The module also provides additional features like chain of thoughts, chain of verifications, token importance and LLM explanation.

This application is built using the Flask web framework.Leveraging the flexibility and scalability of Flask, this application provides some intuitve features as mentioned below.

## Features
1. **Model-based guardrail** : Here we use traditional AI models, libraries to test the input for various checks like prompt injection, jailbreak, toxicity etc.

2. **Template-based guardrail** : Here we  are making use of a Prompt Template for each evaluation check like prompt injection, jailbreak, etc. Prompt templates are a way to define reusable structures for prompting LLMs. It allows us to create a base prompt with placeholders that can be filled with different values to generate specific outputs. 

3. **Translate option** : Given that our model-based guardrails are optimized for English, we offer a translator option. In cases where prompts are in languages other than English, the translator converts them to English before passing them to the guardrails, thus providing extra protection against Multilingual Jailbreak attacks as well.

4. **Multimodal** : We are using multimodal functionality of GPT4o combined with our model based guardrail and template based guardrail to perform moderation checks like prompt injection, jailbreak etc. for text and image uploaded, respectively.

5. **Response comparision** : We are also providing response comparision between just GPT output and output from GPT with our guardrails. 


## Prerequisites

1. Before installing the repo for Moderation Layer, first you need to install the repo for Moderation Models.
Please find the link for **Moderation Model** repo : [moderationmodel](https://github.com/Infosys/Infosys-Responsible-AI-Toolkit/tree/master/responsible-ai-moderationmodel).

2. **Installation of Python** : To run the application, first we need to install Python and the necessary packages. Install Python **(version >= 3.9)** from the [official website](https://www.python.org/downloads/) and ensure it is added to your system PATH.


3. **Installation of pip** :

**Linux:**
1. Check if pip is already installed: Open a terminal and run the following command:
```sh
pip --version
```
2. If pip is not installed, you'll see an error message.
3. Install pip using get-pip.py: Download the `get-pip.py` script as follows
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
4. Make the script executable:
```sh
chmod +x get-pip.py
```
5. Run the script:
```sh
./get-pip.py
```
6. This will install pip and its dependencies.

**Windows:**
1. Download the Python installer: Visit the official [Python website](https://www.python.org/downloads/) and download the latest Python installer for Windows.

2. Install Python: Run the installer and follow the on-screen instructions. Make sure to check the "Add Python to PATH" option during the installation.

3. Verify pip installation: Open a command prompt and run the following command:
```sh
pip --version
```
If pip is installed, you'll see its version.


**macOS:**

**Approach 1**
1. Check if pip is already installed: Open a Terminal window.Type
```sh 
pip --version
```
and press Enter. If pip is installed, you'll see its version.

2. Install pip using Homebrew (recommended): If pip isn't installed or you're unsure, install `Homebrew`, a popular package manager for macOS:
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"   
```
3. Once Homebrew is installed, use it to install pip:
```sh
brew install python
```
4. Verify the installation: Type 
```sh
pip --version
```
again.You should see the installed version of pip.

**Approach 2**

If you encounter issues or prefer a manual installation:

1. Download the get-pip.py script : Use curl to download the script:
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
2. Run the script : Make sure you're using the correct Python interpreter (usually python3):
```sh
python3 get-pip.py
```
3. Enter your password (if prompted) : When you run the script, you might be prompted for your administrator password. This is because the installation process requires elevated privileges. Type your password and press Enter (the characters won't be displayed for security reasons).

4. Verify the installation : Once the script finishes running, you can verify that pip is installed by typing:
```sh
pip --version
```
If pip is installed correctly, you should see the installed version number displayed.



## Installation

### Steps for Installation :
**Step 1**  : You need to install nltk of version 3.9. To do that, go to the path using `cd`   command in command line :
```sh
> cd C:\Users\<your username>
```
Type `python` to open the python terminal.
```sh
> python
```
You will get `>>` like this which signifies python terminal is running. Type the following :
```sh
>> import nltk
>> nltk.download()
```
This will start downloading the latest nltk package (Version : 3.9). You will get a dialog box saying
`Finished downloading collection 'all'` once everything gets downloaded.


**Step 2**  : Clone the repository `responsible-ai-moderationlayer`:
```sh
git clone <repository-url>
```

**Step 3**  : Navigate to the `responsible-ai-moderationlayer` directory:
```sh
cd responsible-ai-moderationLayer
```

**Step 4**  : Use the below link to download `en_core_web_lg` whl file -

[Download Link](https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl)
This will take 30-40 mins. 
Once done, put this inside `lib` folder of the repo `responsible-ai-moderationlayer`.


**Step 5**  : Activate the virtual environment for different OS.

**Windows:**
1. Open Command Prompt or PowerShell: Find and open the appropriate command-line interface
2. Create a virtual environment using the following python command :
```sh
> python -m venv <Name of your Virtual Environment>
```
Let's say your virtual env. name is `myenv` and is located in `C:\Users\your_username`

3. Navigate to the virtual environment directory and activate it using below command :
```sh
> cd C:\Users\your_username\myenv\Scripts
> .\activate
```
4. You should see a prompt that indicates the activated environment, such as (myenv) before your usual prompt like this :
```sh
(myenv) C:\Users\your_username\myenv\Scripts>
```

**Linux:**
1. Open a terminal: Find and open a terminal window.
2. To create a virtual environment, install the relevant version of the `venv` module.Since we are using Python 3.9, install the 3.9 variant of the package, which is named python3.9-venv
```sh
abc@demo:~/$ sudo apt install python3.9-venv
```
3. Create a Virtual env like this.
```sh
abc@demo:~/Projects/MyCoolApp$ python3.9 -m venv <Name of your Virtual Environment>
```
Let's say your virtual env. name is `myenv`

4. Activate the environment: Run the following command
```sh
abc@demo:~/Projects/MyCoolApp$ source myenv/bin/activate
```
5. You should see a prompt that indicates the activated environment, such as (myenv) before your usual prompt like this :
```sh
(myenv) abc@demo:~/Projects/MyCoolApp$
```

**MacOS:**
1. Open Terminal: Find and open the Terminal.
2. Activate the environment: Run the following commands
```sh
python3 -m pip install virtualenv
python3 -m virtualenv <Name of your Virtual environment>
```
Let's say, your virtual env name is `myenv`.
```sh 
source ./myenv/bin/activate 
```


**Step 6** : Go to the `requirements` directory where the `requirement.txt` file is present :

Remember to change `../lib` to `lib`[ **Note :** Needed if you are cloning the repository in your local system ]

For example :
```sh
../lib/better_profanity-2.0.0-py3-none-any.whl
```
change it to
```sh
lib/better_profanity-2.0.0-py3-none-any.whl
```

Now, install the requirements as shown below :
```sh
pip install -r requirement.txt
```

## Set Configuration Variables
After installing all the required packages, configure the environment variables necessary to run the APIs.

We are maintaining an environment file where we are keeping the Moderation Model urls,openai credentials,and many other attributes required for proper functioning of Moderation Layer.

1. Navigate to the `src` directory:
```sh
cd ..
```
2. Locate the file named as `.env`. This file contains key value pairs.There are some mandatory parameters and some are optional.

**Mandatory Parameters**
-------------------------------------------------------------------------------------------------------

1. **Passing Moderation Model URLs** : We have following env variables for passing Moderation Models:
```sh
SIMILARITYMODEL="${similaritymodel}"
RESTRICTEDMODEL="${restrictedmodel}"
DETOXIFYMODEL="${detoxifymodel}"
PROMPTINJECTIONMODEL="${promptinjectionmodel}"
JAILBREAKMODEL="${jailbreakmodel}"
PRIVACY="${privacy}"
```
We need to pass the Model Urls in the same env file, which are nothing but apis for each Model that have been exposed in Moderation Model repo.

```sh
jailbreakmodel=<Put the model url needed for jailbreak>
restrictedmodel=<Put the model url needed for restricted topic>
detoxifymodel=<Put the model url needed for toxicity>
promptinjectionmodel=<Put the model url needed for prompt injection>
jailbreakmodel=<Put the model url needed for jailbreak>
privacy=<Put the model url needed for privacy>
```
For example :
```sh
jailbreakmodel="https://loremipsum.io/generator"
JAILBREAKMODEL="${jailbreakmodel}" 
```

2. **Passing LLM Credentials** : 

**GPT Credentials** :

For this, you need to have Azure OpenaAI service. For more details, you can refer [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) for Pricing Details.


**Note**
1. `apitype` signifies which Cloud Infrastaructure we want to use for Open AI services.
2. We can set any value for apitype like 'azure','aws','google' which ensures that your requests are properly directed to particular cloud infrastructure, allowing you to leverage the powerful capabilities of the platform.

```sh
apitype=<Enter the apitype>
```
Here we are passing openAI creds in the env file as follows.

For gpt4 :
```sh
apibase_gpt4=<Enter the Azure OpenAI endpoint for gpt4, your endpoint should look like the following  https://YOUR_RESOURCE_NAME.openai.azure.com>
apiversion_gpt4=<Enter the Azure OpenAI version for gpt4>
openaimodel_gpt4=<Enter the Model name for gpt4>
apikey_gpt4=<Enter the Azure OpenAI API key for gpt4>
```
For gpt3.5 Turbo :
```sh
apibase_gpt3=<Enter the Azure OpenAI endpoint for gpt3.5 Turbo>
apiversion_gpt3=<Enter the Azure OpenAI version for gpt3.5 Turbo>
openaimodel_gpt3=<Enter the Model name for gpt3.5 Turbo>
apikey_gpt3=<Enter the Azure OpenAI API key for gpt3.5 Turbo>
```
For gpt4O :
```sh
api_base=<Enter the Azure OpenAI endpoint for gpt4O>
api_key=<Enter the Azure OpenAI API key for gpt4O>
api_version=<Enter the Azure OpenAI version for gpt4O>
model=<Enter the Model name for gpt4O>
```

Using the above values here :
```sh
OPENAI_API_BASE_GPT3 = "${apibase_gpt3}"
OPENAI_API_KEY_GPT3 = "${apikey_gpt3}"
OPENAI_API_VERSION_GPT3 = "${apiversion_gpt3}"                
OPENAI_MODEL_GPT3 = "${openaimodel_gpt3}"
OPENAI_API_BASE_GPT4 = "${apibase_gpt4}"
OPENAI_API_KEY_GPT4 = "${apikey_gpt4}"
OPENAI_API_VERSION_GPT4 = "${apiversion_gpt4}"  
OPENAI_MODEL_GPT4 = "${openaimodel_gpt4}"
OPENAI_API_BASE_GPT4_O = "${api_base}"
OPENAI_API_KEY_GPT4_O = "${api_key}"
OPENAI_API_VERSION_GPT4_O = "${api_version}"  
OPENAI_MODEL_GPT4_O = "${model}"
OPENAI_API_TYPE = "${apitype}"
```

3. **Passing DB Related details** : Here we need to pass config details related to DB.
```sh
dbtype=<Mention as 'mongo' for Mongodb or 'psql' for Postgresql>
APP_MONGO_HOST=<Hostname for MongoDB or PostgreSQL>
username=<Enter the username for Database>
password=<Enter the password for Database>
APP_MONGO_DBNAME=<Enter Database name for Mongo/Postgresql>

APP_MONGO_HOST="${APP_MONGO_HOST}"
APP_MONGO_DBNAME="${APP_MONGO_DBNAME}"
DB_USERNAME="${username}"
DB_PWD="${password}"
DBTYPE="${dbtype}"
MONGO_PATH="mongodb://${DB_USERNAME}:${DB_PWD}@${APP_MONGO_HOST}/"
```

4. **Passing Cache details** : Pass the details for caching mechanism.

**Note :**  No. of cache entries depends upon no. of time the cache is invoked.
As per our design, when a single prompt is given , cache is invoked 15 times.
So, if you want to store entries :

for 10 user prompts ----> set cache_size as 150

for 20 user prompts ----> set cache_size as 300
```sh
cache_ttl=<Time for which entries will be stored in cache, mention in seconds>
cache_size=<Total entries in cache>
cache_flag=<cache enablement flag , set it to True if caching to be applied,otherwise False>

CACHE_TTL="${cache_ttl}"
CACHE_SIZE="${cache_size}"
CACHE_FLAG="${cache_flag}"
```

5. **Setting Port No** : This will help to dynamically configure port no. for the Moderation layer Application.

As we know that this app is based on Flask, so you may give port no. as `5000` (Flask's default Port No), or any port no of your choice to make the app run.

Below are the entries for the same :
```sh
ports=< Set your port no. here>
PORT="${ports}"
```

6. **Telemetry Related Details** : If you are setting up this application in your local, then mention as follows :
```sh
TEL_FLAG="${tel_flag}"
tel_flag=<set it as False>
```
otherwise : If you are going to setup elasticsearch, kibana telemetry in your system, use the below configurations.
telemetrypath -> moderation telemetry path URL
coupledtelemetrypath --> coupled moderation telemetry path URL
adminTemplatepath --> admin telemetry path URL
evalllmtelemetrypath --> eval telemetry path URL
```sh
tel_flag=<set it as True>
TELEMETRY_PATH="http://<host:PORT>/path/v1/telemtry/<moderation telemetry api url>" 
COUPLEDTELEMETRYPATH="http://<host:PORT>/path/v1/telemtry/<coupled moderation telemetry api url>"
ADMINTEMPLATEPATH="http://<host:PORT>/path/v1/telemtry/<admin telemetry api url>"
EVALLLMTELEMETRYPATH="http://<host:PORT>/path/v1/telemtry/<eval moderation telemetry api url>"
```

**Optional Parameters**
-------------------------------------------------------------------------------------------------------

1. **Setting Azure AI Tranlator API details** : Below is needed if you want to use Azure translate API for translating the user prompt.For this, you need to have Azure AI Translator service. For more details, you can refer [Azure AI Translator Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/#resources) for Pricing Details.

Set azure translate details as follows :
```sh
AZURE_TRANSLATE_KEY = "${azuretranslatekey}"
AZURE_TRANSLATE_ENDPOINT = "${azuretranslateendpoint}"
AZURE_TRANSLATE_REGION = "${azuretranslateregion}"
azuretranslatekey=<Enter Azure Translate Key>
azuretranslateendpoint=<Enter Azure Translate Endpoint>
azuretranslateregion=<Enter the Region for Azure Translate>
```

2. **BLOOM and LLama Credentials** : Mention the endpoints for Bloom or Llama models.
```sh
BLOOM_ENDPOINT="${bloomendpoint}"
LLAMA_ENDPOINT="${llamaendpoint}"
bloomendpoint=<Mention Bloom endpoint>
llamaendpoint=<Mention Llama endpoint>
```

3. **Setting Details for OAuth2 authentication**: This is required to generate Bearer Token(for OAuth2), which is optional.
```sh
TENANT_ID = "${tenant_id}"
CLIENT_ID = "${client_id}"
CLIENT_SECRET = "${client_secret}"
AUTH_URL = "${auth_url}"
auth_url=<Mention Authenticaion url for token generation>
client_secret=<Client Secret key for token generation>
client_id=<Client Id for token generation>
tenant_id=<Tenant Id for token generation>
```

`SCOPE` is optional, this will be required only if we are using Microsoft or Google's support for token generation.
```sh
SCOPE = "${scope}"
scope=<Set the scope for Service Providers>
```

4. **EXE creation** : This is required for exe creation of application. Set the following variables as follows :
```sh
exe_creation = <Set it to True or False based on user choice>
EXE_CREATION = "${exe_creation}"
```

5. **Setting Vault** : This is required for setting up vault.

For local setup :
```sh
ISVAULT="${isvault}"
isvault=<set it as False>
```
Otherise :
```sh
isvault=<set it as True>
```

6. **Health Check for Application** : This config detail will be required for health check of our application. It's typically used by external monitoring tools or systems to verify if your application is up and running correctly. When a monitoring tool sends a request to `/health` api in `router.py` file, the application responds with a status as `Health check Success` indicating that the application is healthy.

To perform health check , we need to set the following flag :

For local setup :
```sh
log=<set it to false>
```
Otherwise :
```sh
log=<set it to true>
LOGCHECK="${log}"
```

7. Rest all environment variables not mentioned above but are mentioned in `.env` file are completely optional and need not to be set.


## Running the Application

**Note** : Please don't run the api for feedback i.e. `/rai/vi/moderations/feedback` as this endpoint will be deprecated from the next release onwards.

Once we have completed all the above mentioned steps, we can start the service.

1. Navigate to the `src` directory:

2. Run `main.py` file:
    ```sh
    python main.py
     ```

3. PORT_NO : Use the Port No that is configured in `.env` file.

   Open the following URL in your browser:

   `http://localhost:<PORT_NO>/rai/v1/moderations/docs`

4. **For PII Entity Detection and Blocking :**
For `rai/vi/moderations` and `rai/vi/moderations/coupledmoderations` APIs , we have configured parameters to be blocked under `PiientitiesConfiguredToBlock` coming in `ModerationCheckThresholds` in the Request Payload.

These parameters are configurable. For instance, I have provided here some list of entities to block
```sh
"AADHAR_NUMBER" : to block Aadhar Number (Aadhar number should not have spaces in between)
"PAN_Number" : to block PAN Card Number
"IN_AADHAAR" : to block Indian Aadhar number ( this is added due to updated presidio analyzer, which has wide set of entities to detect, make sure Indian Aadhar number should not have spaces in between)
```
```sh
"IN_PAN" : to block Indian PAN Card number ( this is added due to updated presidio analyzer, which has wide set of entities to detect)
```
```sh
"US_PASSPORT" : to block US Passport Number
"US_SSN" : to block US SSN Number
```
which can be added as below :
```sh
"ModerationCheckThresholds": {
    "PiientitiesConfiguredToBlock": [
      "AADHAR_NUMBER",
      "PAN_Number",
      "IN_PAN",
      "IN_AADHAAR",
      "US_PASSPORT",
      "US_SSN"
    ]
}
```

5. **Using Bearer Token for OAuth2 for coupledModeration**
- You need to use the OAuth2 Authentication Token provided Azure or GCP Platform ( Please refer step 3 under **Optional Parameters** in section `Set Configuration Variables` on how to generate OAuth2 token)
- Use that token in 2 places :
  
     a) `Authorize` at the top of the Swagger UI : On clicking on it, you will get an option as **BearerAuth  (http, Bearer)** and then **Value**, in the empty text box , just pass the token and click on `Authorize` and then `Close`.

     b) For Coupled Moderation API : On expanding it, you will get an option as `Parameters`. There, you will find a text box beside `autorization`. Mention the token in below format :
  ```sh
  Bearer <token>
  ```

6. **For the api /rai/v1/moderations/getTemplates/{userid}**
   - For this , first you need to clone the admin repository. Link mentioned :  [Admin Repo](https://github.com/Infosys/Infosys-Responsible-AI-Toolkit/tree/main/responsible-ai-admin)
   - Once done, please do the necessary steps to run the admin repo codebase in your local (as mentioned in admin readme file)
   - Go to the API ```api/v1/rai/admin/createCustomeTemplate``` and provide the necessary details to create custom template. The payload is like this :
  
     For Text Based Templates :
     ```sh
         {
           "userId": "123",
           "mode": "Master_Template/Private_Template", -> Master templates accessible to all, Private templates only to particular user with userid
           "category": "SingleModel",
           "templateName": "Template1",   <------> Name of the Prompt Template
           "description": "Template1",  <-----> Short description on what the template is about
           "subTemplates": [
             {
               "subtemplate": "evaluation_criteria",
               "templateData": ""
             },
             {
               "subtemplate": "prompting_instructions",
               "templateData": ""
             },
             {
               "subtemplate": "few_shot_examples",
               "templateData": ""
             }
           ]
         }
     ```

     For Image based Templates :
     ```sh
         {
           "userId": "123",
           "mode": "Master_Template/Private_Template", -> Master templates accessible to all, Private templates only to particular user with userid
           "category": "MultiModel",
           "templateName": "Template1",   <------> Name of the Prompt Template
           "description": "Template1",  <-----> Short description on what the template is about
           "subTemplates": [
             {
               "subtemplate": "evaluation_criteria",
               "templateData": ""
             },
             {
               "subtemplate": "prompting_instructions",
               "templateData": ""
             },
             {
               "subtemplate": "few_shot_examples",
               "templateData": ""
             }
           ]
         }
     ```

     - Once the above thing is done, in the `.env` file, mention the admin api running in local for the field as shown below :
       ```sh
       adminTemplatepath = "<admin_api_url>" `[ Ex : http://localhost:8019//api/v1/rai/admin/getCustomeTemplate/"]`
       ADMINTEMPLATEPATH="${adminTemplatepath}"
       ```
     - Post this, you can run the api ```api/v1/rai/admin/createCustomeTemplate``` and as success response, you will get response like this :
       ```sh
        Templates Retrieved
       ```

7. **For Template-based Checks**
   - There are 2 APIs exposed that make use of prompt templates to evaluate adversarials from text( text moderation) or image(image moderation).
   - Some Master Templates we are using for the api `/rai/v1/moderations/evalllm` :
     ```sh
     1. Prompt Injection Check : to check for prompt injection
     2. Jailbreak Check : to check for Jailbreak checks
     3. Fairness and Bias Check: to check for biasness
     4. Privacy Check : to check for Privacy
     5. Language Critique Coherence Check : through this check, LLM will evaluate the quality of the provided text, focusing on the coherence aspect.
     6. Language Critique Fluency Check : through this check, LLM will evaluate the quality of the provided text, focusing on the fluency aspect.
     7. Language Critique Grammar Check : through this check, LLM will evaluate the quality of the provided text, focusing on the grammar aspect.
     8. Language Critique Politeness Check : through this check, LLM will evaluate the quality of the provided text, focusing on the politeness aspect.
     9. Response Completness Check : to check if the LLM response is complete w.r.t the user prompt
     10. Response Conciseness Check : to check if the LLM response is concise and brief w.r.t. the user prompt 
     11. Response Language Critique Coherence Check : through this check, LLM will evaluate the quality of the LLM Response, focusing on the coherence aspect.
     12. Response Language Critique Fluency Check : through this check, LLM will evaluate the quality of the LLM Response, focusing on the fluency aspect.
     13. Response Language Critique Grammar Check : through this check, LLM will evaluate the quality of the LLM Response, focusing on the grammar aspect.
     14. Response Language Critique Politeness Check : through this check, LLM will evaluate the quality of the LLM Response, focusing on the politeness aspect.
     ```
         
   - Some Master Templates we are using for the api `/rai/v1/moderations/multimodal` :
     ```sh
     1. Image Restricted Topic Check : to restrict certain topics like "terrorrism" , "explosives"
     2. Image Prompt Injection Check : to check for Prompt Injection
     3. Image Jailbreak Check : to check for Jailbreak attacks
     4. Image Toxicity Check : to check for Toxicity
     5. Image Profanity Check : to check for Profanity
     ```

     We need to use these template names in our request payload as shown below :
     ```sh
     {
      "AccountName": "None",
      "PortfolioName": "None",
      "userid": "None",
      "lotNumber": 1,
      "Prompt": "Which is the biggest country in the world?",
      "model_name": "gpt4",
      "temperature": "0",
      "PromptTemplate": "GoalPriority",
      "template_name": "PROMPT_INJECTION"  <---------->   template name as mentioned above
     }
     ``` 
  
## License
The source code for the project is licensed under the MIT license, which you can find in the [LICENSE.txt](LICENSE.txt) file.

## Contact
If you have more questions or need further insights please feel free to connect with us at
DL : Infosys Responsible AI
Mailid: Infosysraitoolkit@infosys.com
