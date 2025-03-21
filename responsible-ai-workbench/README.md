
## Workbench

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Contact](#contact)
  
## Introduction
The workbench repository is used for processing and generating report for Unstructured text and Risk Assessment Report for Questionnaire.

## Requirements
Python 3.9 - 3.11
VSCode

## Installation
To run the application, first we need to install Python and the necessary packages:
 
1. Install Python (version >= 3.9) from the [official website](https://www.python.org/downloads/) and ensure it is added to your system PATH.
 
2. Install MongoDB by following the instructions on the [official MongoDB website](https://docs.mongodb.com/manual/installation/).
 
3. Install `pip` if it is not already installed. You can download and install it by following the instructions on the [official pip website](https://pip.pypa.io/en/stable/installation/).

4. Clone the repository:
    ```sh
    git clone <repository-url>
    ```

5. Navigate to the `responsible-ai-workbench` directory:
    ```sh
    cd responsible-ai-workbench
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
8. Now go back to `responsible-ai-workbench\responsible-ai-questionnaire` to install the requirements by running the following command : 
   ```sh
     pip install -r .\requirement\requirements.txt
     ```

 
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
3. Open the following URL in your browser:
   `http://localhost:<portno>/v1/questionnaire/docs`

    User can also change the port which is mentioned in main.py file

NOTE : To use the following API endpoints:

    /v1/questionnaire/submitResponse
    /v1/questionnaire/Details
    /v1/questionnaire/riskDashboardDetails/{userid}/{useCaseName}
    /v1/questionnaire/ResubmitDetails/{userid}/{useCaseName}
You will need to store questions and their associated options and score in the database based on your project's specific requirements. Additionally, some code modifications may be necessary to align with your database schema and design and for above API's,

    /v1/questionnaire/lotAssign  -- This api is not in use - It will be deperecated in next release
    /v1/questionnaire/workbench/uploadFile -- Internally it's working & the response is null. Will be updated from next release.


## Contact
If you have more questions or need further insights, feel free to Connect with us @Infosysraitoolkit@infosys.com  
