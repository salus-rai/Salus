'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from llm_explain.config.logger import CustomLogger
import openai
import os

log = CustomLogger()

class Azure:
    def __init__(self):
        
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY") # Retrieve Azure OpenAI API key from environment variables
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") # Retrieve Azure OpenAI endpoint from environment variables
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION") # Retrieve Azure OpenAI API version from environment variables
        self.deployment_engine = os.getenv("AZURE_DEPLOYMENT_ENGINE") # Retrieve Azure OpenAI deployment engine (model) from environment variables
        
        # Initialize the AzureOpenAI client with the retrieved API key, API version, and endpoint
        self.client = openai.AzureOpenAI(
                            api_key = self.api_key, 
                            api_version = self.api_version,
                            azure_endpoint = self.azure_endpoint
                        )
        
    def generate(self, prompt):
        try:
            # Generate a chat completion using the AzureOpenAI client
            # The completion is based on a prompt provided by the user and a predefined system message
            completion = self.client.chat.completions.create(
                model=self.deployment_engine, # Specify the model (deployment engine) to use
                messages=[
                    {
                        "role": "system", # System message to set the context for the AI
                        "content": "You are a helpful assistant.",
                    },
                    {
                        "role": "user", # User message that contains the actual prompt
                        "content": prompt
                    }
                ]
            )

            # Return the content of the first message from the generated completion
            return completion.choices[0].message.content
        except openai.APIConnectionError as e:
            log.error(f"Azure OpenAI API connection error: {e}")
            raise Exception("Azure OpenAI API connection error")
    