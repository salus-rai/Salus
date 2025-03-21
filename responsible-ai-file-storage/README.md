# responsible-ai-file-storage

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Features](#features)
- [Installation](#installation)
- [Configurations](#configurations)
- [License](#license)
- [Contact](#contact)

## Introduction
API's to access and consume Azure Blob storage services.

## Requirements
1. Python 3.9 and Python 3.10
2. pip
3. cosmos DB
4. VSCode

## Features

- **Add File - /api/v1/azureBlob/addFile**
The functionality is used to save a file in CosmosDB under a specified container.

- **Get File - /api/v1/azureBlob/getBlob**
The functionality is used to retrieve a file from CosmosDB with in a specified container.

- **Delete File - /api/v1/azureBlob/delete_blob**
The functionality is used to delete a file from a specified container.

- **Update File - /api/v1/azureBlob/updateFile**
The functionality is used to update a file in a container by replacing the existing file with a new version of the file.

- **Add Container - /api/v1/azureBlob/addContainer**
The functionality is used to add a new blob storage container.

- **List Containers - /api/v1/azureBlob/List-Containers**
The functionality is used to list all storage containers, retrieving the names of all containers within a storage account.

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
3.	Install dependencies. 
      1. Go to **responsible-ai-file-storage\requirements** and run 
      ```bash 
         pip install -r requirements.txt.
      ```
      2. if you are on windows, please add **../** in front to .whl file in requirements.txt to install without any errors.
4. Add required configurations provided below in .env file.
5. Run the application using below steps:
      1. Go to responsible-ai-fairness/responsible-ai-fairness/src 
      2. Run 
      ```bash 
         python main_api.py 
      ```
6. Use the Port No that is mentioned in main.py file. Open the swagger URL in browser once server is running: `http://localhost:8000/api/v1/azureBlob/docs#/`


## Configurations
1. Add required environment variables.

| Key         | Placeholder Value | sample Value     | Required |
|-------------|-------------------|------------------|----------|
| AZURE_BLOB_STORAGE_CONNECTION_KEY    | "${azure_connection_key}"     | YOUR_CONNECTION_KEY  |  yes     |

## License

The source code for the project is licensed under MIT license, which you can find in the [LICENSE.md](LICENSE.md) file.


## Contact
If you have more questions or need further insights, feel free to Connect with us @ infosysraitoolkit@infosys.com
