# responsible-ai-trustllm

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Features](#features)
- [Installation](#installation)
- [Configurations](#configurations)
- [License](#license)
- [Contact](#contact)

## Introduction
 [TrustLLM](https://github.com/HowieHwong/TrustLLM) is a tool used to benchmark text generating LLMs. Privacy, Fairness, Safety, Truthfulness, Ethics of the LLM are evaluated using the dataset provided. We have created a wrapper around this tool to ease the benchmarking process.

## Requirements
1. Python 3.9 and Python 3.10
2. pip
3. Mongo DB
4. VSCode

## Features
- Benchmarking of huggingface models using the dataset provided.
- Adding, deleting, retriving scores from DB.

## Installation
1.	Clone the repository
2.	Create a virtual environment using the command 
```bash
python -m venv .venv
```
and activate it by going to
```bash
.venv\Scripts\activate
```
3.	Setup the DB
      1. Create database in mongodb and add the db name in .env file
4.	Install dependencies. 
      1. Go to **responsible-ai-benchmarking\requirements** and run 
      ```bash 
         pip install -r requirement.txt
      ```
      2. if you are on windows, please add **../** in front to .whl file in requirements.txt to install without any errors.
5. Add required configurations provided below in .env file.
6. Run the application using below steps:
      1. Go to responsible-ai-benchmarking\src 
      2. Run 
      ```bash 
         python main_api.py 
      ```
7. Use the Port No that is mentioned in main.py file. Open the swagger URL in browser once server is running: `http://localhost:<portno>/api/v1/trustllm/docs#/`


## Configurations
 1. Add required environment variables.
 2. Below are the list of env one needs to add, to run the application, add required ones only and for the rest one can keep it as it is. .env template is there in the src folder.

| Key         | Placeholder Value | sample Value     | Required |
|-------------|-------------------|------------------|----------|
| DB_NAME    | "${dbname}"      | "rai_repository"   |  yes     |
| DB_USERNAME  | "${username}"    |  "user"  |  yes   |
| DB_PWD | "${ipaddress}"     |            |  optional|
| DB_PORT      | "${port}"     |                  |  optional|
| MONGO_PATH       | "mongodb://localhost:/"    |   "mongodb://localhost:27017/ "              |  yes |
| COSMOS_PATH    | "${cosmos_path}"         |                  | optional |
| DB_TYPE | "${dbtype}" | "mongo" | yes |
| allow_methods | "${allow_methods}"  | '["GET", "POST"]'  | yes |
| allow_origin     | "${allow_origin}"       | ["*"]         | yes |
| content_security_policy | "${content_security_policy}" | "default-src 'self' img-src data: https:; style-src 'self' 'unsafe-inline'https://cdn.jsdelivr.net;script-src 'self' 'unsafe-inline'https://cdn.jsdelivr.net" | yes |
| cache_control | "${cache_control}" | "private, no-store" | yes |
| XSS_header | "${xss_header}" | "1; mode=block" | yes |
| Vary_header | "${vary_header}" | 'Origin' | yes |
| azure_engine | "${azure_engine}" | Azure Engine Name | yes |
| azure_api_base | "${azure_api_base}" | Azure API Base | yes |
| openai_key | "${openai_key}" | OpenAI Key | yes |
| azure_api_version | "${azure_api_version}" | Azure API Version | yes |


##Note:
Offline Generation and evaluation required GPU to run. To install cuda, execute the following command <br>
``` bash 
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```


## License
The source code for the project is licensed under MIT license, which you can find in the [LICENSE.md](LICENSE.md) file.


## Contact
If you have more questions or need further insights, feel free to Connect with us @ infosysraitoolkit@infosys.com

For more details refer our [User Guide](https://github.com/Infosys-AI-Cloud-MMS/responsible-ai-trustllm/blob/main/trustllm/docs/Steps%20to%20generate%20Benchmark%20scores.pdf) for more details.
