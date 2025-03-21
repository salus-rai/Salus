# FAQs  

Below are some frequently asked questions to use `Infosys-Responsible-AI-Toolkit` repositories.  

## How can I avoid issues with long file paths when extracting a ZIP file?  
 
When downloading the entire codebase as a ZIP file, extract it into a folder with a shorter name. This helps avoid issues caused by excessively long file paths when extracting or running the modules.  

## How do I download models from Hugging Face?  

To download models from Hugging Face, sign up on their website. Once registered, you can download the required files.  

## What should I do if the packages in the requirements file are updated?  

If the packages in the `requirements.txt` file are updated, follow these steps:  
1. Verify the issue in the command prompt.  
2. Try upgrading or re-installing the dependencies using the `requirements.txt` file.  
3. If the issue persists, delete and reinstall the dependencies using:  
   ```bash
   pip install -r requirements.txt
   ```  

## How can I resolve connection issues with MongoDB?  

If you face connection issues with MongoDB, follow these steps:  
1. Create an empty folder for your database files.  
2. Open the command prompt and run the following command:  
   ```bash
   mongod --dbpath /path/to/data/directory
   ```  

## How can I check the available features in RAI?  

Refer to the `README.md` file in the respective repositories for general information. For details on specific features and responses, check the endpoint documentation available within the repositories.  

## Which version of Python is required to run the application?  

Refer to the `README.md` file in the respective repository to determine the required Python version.  

## How can I clone a repository?  

Follow these steps to clone a repository:  
1. Copy the repository URL from the **Code** section.  
2. Open the command prompt and navigate to your desired directory.  
3. Run the following command:  
   ```bash
   git clone <repository-url>
   ```  

## How can I create a virtual environment?  

1. Open the command prompt and navigate to the directory where the repository is cloned.  
2. Run the following command to create a virtual environment:  
   ```bash
   python -m venv <name-of-your-environment>
   ```  

## How can I create a database or collection in MongoDB?  
 
1. Open **MongoDB Compass**.  
2. Enter your connection details (hostname, port, authentication) and click **Connect**.  
3. Click the **Create Database** button.  
4. Enter the **Database Name** and **Collection Name**.  
5. Click **Create Database** or **Create Collection**.  

## How can I activate the virtual environment?  

1. Navigate to the directory where your virtual environment is located.  
2. Run the following command to activate it:  
   ```bash
   .\<name-of-your-environment>\Scripts\activate
   ```  

## How do I install the necessary packages?  
 
1. Ensure that your virtual environment is activated.  
2. Navigate to the folder containing the `requirements.txt` file.  
3. Run the following command:  
   ```bash
   pip install -r requirements.txt
   ```  

## How do I run Serper and GoT APIs for Explainability?  

Use GPT-4 or earlier versions to obtain explanations.  

## How do I run the Uncertainty API for Explainability?  

Use GPT-4 or earlier versions to obtain explanations.  

## How do I set up telemetry?  
1. Set `tel_Flag` to `True` in the `.env` file of the respective repository.  
2. Follow the setup instructions in **responsible-ai-telemetry**.  
3. Use the following API endpoint from the Swagger UI setup and assign it to the `telemetry_url` variable in the `.env` file:  
   ```text
   /rai/v1/telemetry/errorloggingtelemetryapi
   ```  