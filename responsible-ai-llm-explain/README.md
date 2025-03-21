# Responsible-AI-LLM-Explain

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Set Configuration Variables](#set-configuration-variables)
- [Running the Application](#running-the-application)
- [License](#license)
- [Contact](#contact)
- [Issues](#issues)

## Introduction

**LLM Explain APIs** provides explanations for Large Language Models using methods such as Token Importance, Graph of Thoughts, Chain of Thought (CoT), Search Augmentation, Chain of Verification (CoV), and Thread of Thoughts (Thot). It evaluates the responses with metrics including uncertainty, relevancy, and coherence to ensure the reliability and clarity of Generative AI models' outputs.


## Features
- **Sentiment Analysis**
    
    Sentiment analysis analyzes the sentiment of a given prompt, classifies the sentiment, and identifies the key keywords that significantly influenced the model's sentiment assignment. Additionally, it provides a detailed explanation of the decision-making process behind the sentiment classification.
- **Token Importance**

    Token importance in large language models identifies which words or parts of words in a prompt are crucial for shaping the model's response. It helps us understand which tokens significantly influence the output, providing insights into how the model interprets and generates its responses.

- **Graph of Thoughts**

    The Graph of Thoughts reasoning process in large language models is a way to visualize how the model thinks. Imagine the model's ideas as dots, and the connections between them as lines. This method creates a map of these dots and lines to show how the model connects different pieces of information to come up with its answers. It helps us understand the model's logical flow and ensures that its reasoning makes sense, like how a human would think through a problem step-by-step.

- **Search Augmentation**

    Search augmentation in large language models involves using internet searches to validate and enhance the model's responses. This process supplements the model's answers with additional information from online sources, improving accuracy and reliability by cross-checking and complementing the original output.

- **Explanation Metrics**

    LLM Explanation metrics involves assessing how well a large language model's response addresses a query. It focuses on evaluating the quality of the model's answers to ensure they are clear, accurate, and relevant. This process helps in understanding and validating the usefulness of the model's responses.

    - **Uncertainty**: Measures the model’s confidence in its responses, highlighting areas where the model may exhibit lower certainty.

    - **Coherence**: Assesses the logical consistency and organization of the explanation, ensuring a clear and structured line of reasoning.

- **Chain of Thought**

    It refers to a structured problem-solving approach that breaks down complex tasks into a series of logical, step-by-step processes. It allows the model to systematically explore each part of the problem, making the reasoning more transparent and improving the accuracy of the solution by focusing on each individual step before arriving at a final answer.

- **Thread of Thoughts**

    Thread of Thoughts addresses challenges in chaotic or complex contexts where large language models (LLMs) struggle to sift through and prioritize relevant information amidst an overwhelming amount of data. It helps organize and guide the model’s reasoning by maintaining a clear path of thought, ensuring that important details are identified and addressed without getting lost in extraneous information.

- **Chain of Verification**

    Chain of Verification is a mechanism implemented to directly counteract hallucinations, which occur when an LLM generates responses that are logically coherent but factually incorrect. This approach ensures that each piece of information or step in the model's reasoning process is validated or cross-checked, reducing the likelihood of errors or false conclusions by reinforcing the reliability of the generated output.

- **Chain of Thought for RAG**

    Chain of Thought for RAG (Retrieval-Augmented Generation) outlines the reasoning steps an LLM takes to generate a response, combining the input prompt with relevant context retrieved from external sources. The model explains how it integrates both the prompt and the additional information to form a coherent answer. In a RAG-based system, context is retrieved from vector storage and used to enrich the response. This approach ensures the model's response is grounded in relevant, factual data. It also provides transparency into the reasoning behind the response, clarifying which details were prioritized.

**Note:** 
- `Chain of Thought for RAG` `Chain of Verification` `Thread of Thoughts` `Chain of Thought` These features are available under **Moderation Layer** (responsible-ai-moderationLayer) repository.
Please follow the setup instructions in the README file of the moderation layer repository to configure them. Ensure that the service is up and running to execute.

- For generating explanations, use GPT4 or earlier model versions in **llm-explain** (responsible-ai-llm-explain) repository.


## Installation
To run the application, first we need to install Python and the necessary packages:

1. Install Python (version >= 3.9 and <= 3.12) from the [official website](https://www.python.org/downloads/) and ensure it is added to your system PATH.

2. Clone the repository:
    ```sh
    git clone <repository-url>
    ```

3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
         ```

5. Upgrade `pip`:
    ```sh
    python -m pip install --upgrade pip
    ```

6. Navigate to the `responsible-ai-llm-explain` directory:
    ```sh
    cd responsible-ai-llm-explain
    ```
    
7. Go to the `requirements` directory where the `requirement.txt` file is present and install the requirements:
    ```sh
    cd responsible-ai-llm-explain\requirements
    pip install -r requirement.txt
    ```
## Set Configuration Variables

After installing all the required packages, configure the variables necessary to run the APIs.

1. Navigate to the `llm_explain` directory:
    ```sh
    cd ..
    cd src/llm_explain
    ```

2. Locate the `.env` file in the project directory. This file contains several configuration keys. Make sure to fill in the mandatory fields:

    ```sh
    AZURE_OPENAI_API_KEY = "${apikey}"          # [Mandatory]
    AZURE_OPENAI_API_VERSION = "${apiversion}"  # [Mandatory]
    AZURE_OPENAI_ENDPOINT = "${azureendpoint}"  # [Mandatory]
    AZURE_DEPLOYMENT_ENGINE = "${engine}"       # [Mandatory]
    SERPER_KEY = "${serperkey}"                 # [Mandatory]
    ALLOWED_ORIGINS = "${allowedorigins}"       # [Mandatory]
    ERROR_LOG_TELEMETRY_URL = "${errorlogtelemetryurl}" # [Optional]
    TELEMETRY_FLAG = "${telemetryflag}"         # [Optional]
    ```
    ```sh
    ALLOWED_ORIGINS = "${allowed_origins}"     # ALLOWED_ORIGINS ="*"         
    To allow access to all sites, use the value *. Alternatively, you can specify a list of sites that should have access.
    ```
    ```sh
    SERPER_KEY = "${serperkey}"            
    Steps to get serper key:
    1. Signup to "https://serper.dev/" with required details.
    2. Signin into account. go to the "API Keys" section in your account dashboard.
    3. Click on generate button to create new API key.
    3. Copy and assign it to SERPER_KEY variable in configuration.
    ```
    

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

3. Steps to form swagger url:
    1. Use the Port No that is mentioned in `main.py` file. Open the swagger URL in browser once server is running: `http://localhost:Port_No/rai/v1/llm-explainability/docs`

For API calls, please refer to the [API Documnet](responsible-ai-llm-explain/docs/API_Doc.pdf)

## License

The source code for the project is licensed under MIT license, which you can find in the [LICENSE.md](LICENSE.md) file.

## Contact

If you have more questions or need further insights, feel free to Connect with us @ infosysraitoolkit@infosys.com

## Issues

- Graph of Thought currently supports GPT-3.5-Turbo and GPT-4 models, requiring deployment names as `gpt-35-turbo` or `gpt4`; ensure `AZURE_DEPLOYMENT_ENGINE` in the .env file and `modelName` in API payload match. Support for additional models and deployment name issues planned for a future release.
