# Upload-Module
 
## Introduction
This module used for processing large files like video and store the processed video with respect to userid
3 subcatogery under video Processing :
    1.PIIAnonymization
    2.SafetyMasking
    3.NudityMasking
 
## Requirements
1. Python 3.9 - 3.11
2. VSCode
 
## Installation

To run the application, first we need to install Python and the necessary packages:
 
1. Install Python (version >= 3.9) from the [official website](https://www.python.org/downloads/) and ensure it is added to your system PATH.
 
2. Install MongoDB by following the instructions on the [official MongoDB website](https://docs.mongodb.com/manual/installation/).
 
3. Install `pip` if it is not already installed. You can download and install it by following the instructions on the [official pip website](https://pip.pypa.io/en/stable/installation/).

4. Clone the repository:
    ```sh
    git clone <repository-url>
    ```

5. Navigate to the `responsible-ai-upload-doc` directory:
    ```sh
    cd responsible-ai-upload-doc
    ```

6. Create a virtual environment:
    ```sh
    python -m venv myenv
    ```

7. Activate the virtual environment:
    - On Windows:
        ```sh
        .\myenv\Scripts\activate
         ```
 
    - On Linux/Mac:
        ```sh
        source myenv/bin/activate
        ```
8. Now go back to `responsible-ai-upload-doc/` to install the requirements by running the following command : 
   ```sh
     pip install -r .\requirement\requirement.txt
     ```

## Set Configuration Variables
After installing all the required packages, configure the variables necessary to run the APIs.

1. Navigate to the `responsible-ai-upload-doc/src
/docProcess/` directory:
    ```sh
    cd src/docProcess
    ```
2. Locate the `.env` file, which contains keys like the following:
   ```sh
      DB_NAME="${dbname}"                 # [Mandatory] - Any Name : RAI_Admin_DB
      DB_USERNAME="${username}"           # [Optional] 
      DB_PWD="${password}"                # [Optional] 
      DB_IP="${ipaddress}"                # [Optional] 
      DB_PORT="${port}"                   # [Optional] 
      MONGO_PATH="mongodb://${DB_USERNAME}:${DB_PWD}@${DB_IP}:${DB_PORT}/"     # [Mandatory] MONGO_PATH = "mongodb://localhost:27017/"  - if using DB_TYPE = "mongo" locally. Also, use the port according your local
      DB_TYPE ="${dbtype}"                # [Mandatory] DB_TYPE = "mongo"
      COSMOS_PATH ="${cosmos_path}"       # [Optional] - Needed if DB_TYPE = "cosmos"
   PRIVACY_IP="${privacyapi}"
   PRIVACY_PIIVIDEO_IP="${privacy_PII_video_api}" #TO run PII Masking on Video use endpoint form privacy_files 

   SAFETY_NSFW_IP="${nsfw_ip}"  # use safety_video endpoint from safety module
   SAFETY_NUDITY_IP="${nudity_ip}" #use nudity_masking endpoint from safety module

   AZURE_STORE_ADD_API="${azure_store_add_api}" # [Mandatory] -to store processed video 
   AZURE_STORE_GET_API="${azure_store_get_api}" # [Mandatory] - to get stored video 
   ```
   ```sh
    allow_origin = "${allow_origin}"     # allow_origin ="*"         
    To allow access to all sites, use the value *. Alternatively, you can specify a list of sites that should have access.

    allow_method = "${allow_method}"     # allow_method="GET, POST, OPTIONS, HEAD, DELETE, PATCH, UPDATE"
   ```
   NOTE : To store the videos, endpoint is needed from azure blob storage module. 
   
3. Replace the placeholders with your actual values.
## Running the Application

Once we have completed all the aforementioned steps, we can start the service.

1. Navigate to the `src` directory:
    ```sh
    cd ..
    ```

2. Run `main.py` file:
    ```sh
    python main.py
     ```
3. Use the Port No that is mentioned in main.py file. Open the swagger URL in browser once server is running: 
    `http://localhost:<portno>/rai/v1/docProcess/docs#/`

    User can also change the port which is mentioned in main.py file


##### Note: Endpoint /rai/v1/docProcess/getFileContent/{docId} is Deprecated 
