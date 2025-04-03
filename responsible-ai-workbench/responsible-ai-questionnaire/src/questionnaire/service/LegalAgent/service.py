"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import re
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from questionnaire.constants.local_constants import PROHIBITED_RISK, HIGH_RISK, LIMITED_RISK, MINIMAL_RISK, AGENT_INSTRUCTIONS
from dotenv import load_dotenv

load_dotenv()

class AgentService:
    def __init__(self):
        self.api_key = os.environ.get("APIKEY_GPT3")
        self.api_base = os.environ.get("OPENAI_API_BASE")
        self.api_version = os.environ.get("OPENAI_API_VERSION")
        self.deployment_name = os.environ.get("DEPLOYMENT_NAME")
        
        os.environ["AZURE_OPENAI_API_KEY"] = self.api_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = self.api_base
        self.llm = AzureChatOpenAI(
            azure_deployment=self.deployment_name,
            api_version= self.api_version,
        )

    def predict_risk(self, use_case_data:str):
        @tool
        def prohibited_criteria() -> str:
            """Use this tool to get the creteria for prohibited AI use cases.

            Args:
                None

            Returns:
                str: Returns the criteria for prohibited AI use cases.
            """
            return PROHIBITED_RISK

        @tool
        def highrisk_criteria() -> str:
            """Use this tool to get the criteria for high-risk AI use cases.

            Args:
                None
                
            Returns:
                str: Returns the criteria for high-risk AI use cases.
            """
            return HIGH_RISK

        @tool
        def limitedrisk_criteria() -> str:
            """Use this tool to get the criteria for limited-risk AI use cases.
            
            Args:
                None
                
            Returns:
                str: Returns the criteria for limited-risk AI use cases.
            """
            
            return LIMITED_RISK
            
        @tool 
        def minimalrisk_criteria() -> str:
            """Use this tool to get the criteria for minimal-risk AI use cases.
            
            Args:
                None
                
            Returns:
                str: Returns the criteria for minimal-risk AI use cases.
            """
            
            return MINIMAL_RISK

        @tool
        def get_use_case() -> str:
            """Use this tool to get the use case data.

            Args:
                None
            
            Returns:
                str: Returns the use case data.
            """
            return use_case_data
        
        def print_stream(stream):
            try:
                for s in stream:
                    message = s["messages"][-1]
                    # if isinstance(message, tuple):
                    #     print(message)
                    # else:
                    #     message.pretty_print()
            except Exception as e:
                print("ERROR IN PRINT STREAM", e)
            return message
        
        react_agent=create_react_agent(model=self.llm,tools=[prohibited_criteria, highrisk_criteria,limitedrisk_criteria,minimalrisk_criteria, get_use_case])

        inputs = {"messages": [("user", AGENT_INSTRUCTIONS)]}
        
        message=print_stream(react_agent.stream(inputs, stream_mode="values"))
        ANSWER = None
        REASON = None

        # Regular expression to extract the answer and reason
        pattern = r"### Final answer:\s*(Prohibited|High-Risk|Limited-Risk|Minimal-Risk)\s*Reason:\s*(.*)"

        # Search for the pattern in the response string
        match = re.search(pattern, message.content, re.DOTALL)

        if match:
            ANSWER = match.group(1).strip()
            REASON = match.group(2).strip()

        # Print the extracted values
        print(f"RISK Answer: {ANSWER}")
        return {"risk": ANSWER, "reason": REASON}