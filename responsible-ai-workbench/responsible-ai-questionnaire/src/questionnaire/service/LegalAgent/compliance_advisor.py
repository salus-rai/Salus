"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#Ai compliance advisor to find answers!!
from bson import ObjectId
from langchain_openai import ChatOpenAI
from langchain_core.messages import *
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, Annotated, Sequence
import operator
import json,chardet
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import AzureChatOpenAI
import re
from langchain.pydantic_v1 import BaseModel, Field
import os
#import google.generativeai as genai
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.output_parsers.json import SimpleJsonOutputParser
import pandas as pd
from langgraph.prebuilt import ToolNode,create_react_agent

import glob
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
import logging

import os
from langchain_openai import AzureChatOpenAI

import shutil
import uuid
from datetime import datetime

import requests
import tempfile

from questionnaire.dao.LegalAgent.LegalAgentFileProcDb import LegalAgentFileProcessing
from questionnaire.dao.LegalAgent.legalAgentAnnex import LegalAgentAnnex
from questionnaire.dao.LegalAgent.legalAgentArticlesdb import LegalAgentArticles
from questionnaire.dao.LegalAgent.legalAgentQuestionsdb import LegalAgentQuestions


def storeFile(file,filetype,fileName,processing_id):
        surl=os.getenv("AZURE_STORE_ADD_API")
        # print(file)
        file={"file":file}
        payload={"container_name":filetype}
        for i in range(3):
            try:
                print("==========================================")
                res=requests.post(url=surl,files=file,data=payload)
                storageDetails=res.json()
                print(storageDetails["blob_name"])
                
                storelink=os.getenv("AZURE_STORE_GET_API")+"?blob_name="+storageDetails["blob_name"].replace(" ","%20")+"&container_name="+filetype
              
                print("STORE LINK",storelink)
                # LegalAgentFileProcessing.update({"_id":ObjectId(processing_id)},{"reportLink":storelink,"status":"Completed"})
                LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Completed',"reportLink":storelink, 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})     
                return res.content
                # break
            except Exception as e:
                print(e)
                continue
        # res=requests.post(url=surl,files=file,data=payload)
        # docDb.update(docid,{"status":"Failed"})
        LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Failed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return False


#This function processes the compliance advisor task   
def process_compliance_advisor(processing_id,pdf_content,user_id):
    try:
        # Create a timestamp folder with a unique ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())
        timestamp_folder = os.path.join(".", f"{timestamp}_{unique_id}")

        print(f"Creating timestamp folder: {timestamp_folder}")

        # Create necessary directories
        os.makedirs(os.path.join(timestamp_folder, "Answers"), exist_ok=True)
        os.makedirs(os.path.join(timestamp_folder, "Full_docs"), exist_ok=True)
        # timestamp_folder = f"./{timestamp}_{unique_id}"

        # # Create necessary directories
        # os.makedirs(f"{timestamp_folder}/Answers", exist_ok=True)
        # os.makedirs(f"{timestamp_folder}/Full_docs", exist_ok=True)
        # os.makedirs(f"./assets/images", exist_ok=True)
        # os.makedirs(f"./assets/fonts", exist_ok=True)

        # Save tick, cross, grey images, and fonts into a different folder
        # tick_image = os.path.join(".", "assets", "images", "tick.png")
        # cross_image = os.path.join(".", "assets", "images", "cross.jpg")
        # grey_image = os.path.join(".", "assets", "images", "grey.png")
        # dejavu_sans_bold = os.path.join(".", "assets", "fonts", "dejavu-sans-bold.ttf")
        # dejavu_sans = os.path.join(".", "assets", "fonts", "dejavu-sans.ttf")

        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        tick_image = os.path.join(assets_dir, "images", "tick.png")
        cross_image = os.path.join(assets_dir, "images", "cross.jpg")
        grey_image = os.path.join(assets_dir, "images", "grey.png")
        dejavu_sans_bold = os.path.join(assets_dir, "fonts", "dejavu-sans-bold.ttf")
        dejavu_sans = os.path.join(assets_dir, "fonts", "dejavu-sans.ttf")

        print(f"Assets directory: {assets_dir}")

        # Check if the files exist
        for file_path in [tick_image, cross_image, grey_image, dejavu_sans_bold, dejavu_sans]:
            if os.path.exists(file_path):
                continue
            else:
                print(f"File not found: {file_path}")

        # # Check if the files exist
        # if not os.path.exists(tick_image):
        #     print(f"File not found: {tick_image}")
        # if not os.path.exists(cross_image):
        #     print(f"File not found: {cross_image}")
        # if not os.path.exists(grey_image):
        #     print(f"File not found: {grey_image}")
        # if not os.path.exists(dejavu_sans_bold):
        #     print(f"File not found: {dejavu_sans_bold}")
        # if not os.path.exists(dejavu_sans):
        #     print(f"File not found: {dejavu_sans}")

        # Function to clean up the timestamp folder
        def cleanup_folder(folder_path):
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                logging.error(f"Error deleting folder {folder_path}: {e}")


        deployment_name = os.getenv("DEPLOYMENT_NAME")
        openai_api_base = os.getenv("OPENAI_API_BASE")
        openai_api_version = os.getenv("OPENAI_API_VERSION")
        apikey_gpt3 = os.getenv("APIKEY_GPT3")
       
        
        os.environ["AZURE_OPENAI_API_KEY"] = apikey_gpt3
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai_api_base
        
        
        model = AzureChatOpenAI(
            azure_deployment=deployment_name,
            temperature=0, # or your deployment
            api_version= openai_api_version,
        )


        # Configure logging
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        #This function extracts text between a given part of string to the end of the string
        def extract_text_till_eof(text, word1):
            pattern = f"{word1}(.*)"
            matches = re.findall(pattern, text, re.DOTALL)
            return matches

        #This function extracts text between a given part of string to another part of the string
        def extract_text_between_words(text, word1, word2):
            pattern = f"{word1}(.*?){word2}"
            matches = re.findall(pattern, text, re.DOTALL)
            return matches

        # Define the agent state
        class AgentState(TypedDict):
            #messages will be tracked
            messages: Annotated[Sequence[BaseMessage], operator.add]

        #Defining the retrieve_article args schema
        class article_get(BaseModel):
            article_number: int = Field(description="The number of the article that the user wants to extract")

        #Defining the annex args schema
        class annex_get(BaseModel):
            annex_number: str = Field(description="The roman number in uppercase of the annex that the user wants to extract")

        #This tool is used by the agent to call the relevant article it requires. The doc string in the tool helps give more context to the agent regarding how to call the tool and what it does.
        @tool
        def retrieve_article(article_number:int) -> str:
            
            """ Use this tool to retrieve the relevant article of EU AI Act that is needed.
                Args:
                    article_number (int): The number of the article you want to retrieve.
                Returns:
                    str: The article text. """
            # file_name=".\\Articles\\Article "+str(int(article_number))+".txt"
            # content = open(file_name, 'rb').read()
            # result = chardet.detect(content)
            # encoding = result['encoding']
            # with open(file_name, 'r', encoding=encoding) as f:
            #     content = f.read()    
            # return content
            res = LegalAgentArticles.findOne(article_number)
            if res is None:
                return ""
            # print("----------------------RES----------------------")
            # print(res)
            # print("----------------------RES----------------------")
            return res['article']

        #Tool used to retrieve an annex
        @tool
        def annex_extract_tool(annex_number:str) -> str:    
            """Use this tool to retrieve the relevant annex of EU AI Act that is needed.
                Args:
                    annex_number (str): The roman number in uppercase of the annex you want to retrieve.
                Returns:
                    str: The annex text.  """
            # file_name=".\\Annexes\\ANNEX "+str(annex_number)+".txt"
            # content = open(file_name, 'rb').read()
            # result = chardet.detect(content)
            # encoding = result['encoding']

            # with open(file_name, 'r', encoding=encoding) as f:
            #     content = f.read()
            
            # return content
            res = LegalAgentAnnex.findOne(annex_number)
            if res is None:
                return ""
            # print("----------------------RES----------------------")
            # print(res)
            # print("----------------------RES----------------------")
            return res['annex']


        #Tool used to retrieve history of legal agent by the senior legal agent. Currently we are not passing it directly through messages but as future work we should incorporate seemless transition.
        @tool
        def chat_history_tool(content:str) -> str:    
            """Use this tool to retrieve the previous agent's task, interactions, output and context history
                Args:
                    annex_number (str): The roman number in uppercase of the annex you want to retrieve.
                Returns:
                    str: The context history text.  """
            file_name="./history.txt"
            content = open(file_name, 'rb').read()
            result = chardet.detect(content)
            encoding = result['encoding']

            with open(file_name, 'r', encoding=encoding) as f:
                content = f.read()
            
            return content

        #This function prints all the messages, meaning the input prompts , the output of the model and anything else when the code is running.
        def print_stream(stream):
            for s in stream:
                message = s["messages"][-1]
                # if isinstance(message, tuple):
                    # print(message)
                # else:
                    # message.pretty_print()
            return message

        #This tool is to retrieve details of the client project from the RAI canvas template
        @tool
        def client_info(content:str) -> str:    
            """Use this tool to retrieve the client project documentation
                Args:
                    annex_number (str): put random string
                Returns:
                    str: The client's AI project documentation.  """
            # file_name=".\\use case\\use-case-1.txt"
            # content = open(file_name, 'rb').read()
            # result = chardet.detect(content)
            # encoding = result['encoding']

            # with open(file_name, 'r', encoding=encoding) as f:
            #     content = f.read()
            
            # return content
            return pdf_content


        react_system_message_1=""" You are an AI legal compliance advisor and researcher who is an expert with extensive knowledge of European regulations and 
        standards specifically EU AI Act and has worked with several tech companies to ensure their products meet legal compliance, especially in the realm of AI.
        Lastly, you are passionate about bridging the gap between innovation and regulation. Your goal is to provide guidance and ensuring that your
        client's AI application complies with the EU AI Act regulations."""



        os.environ['TAVILY_API_KEY']="Enter API key here"
        tavily_tool = TavilySearchResults(max_results=4) #increased number of results
        react_agent_1=create_react_agent(model,tools=[retrieve_article,annex_extract_tool,tavily_tool,client_info],state_modifier=react_system_message_1)



        df=pd.DataFrame([["",""]])
        
        for k in range(3,4):
            #For every article i  
            logging.info(f"Processing articles")
            for i in range(1,114):
                    try:
                        question = LegalAgentQuestions.findOne(i)
                        if question is None:
                            logging.error(f"Questions for article {i} not found in database")
                            string1 = ""
                        else:
                            string1 = question['question']  
                            
                        # print('--------------------------STRING1 QUESTION------------------------------------------------')
                        # print(string1)
                        # print('--------------------------STRING1------------------------------------------------')
                        # with open(".\\Questions\\Questions_"+str(k)+"\\Questions_"+str(i)+".txt", "r", encoding='utf8') as file:
                        #     string1=file.read()

                        
                        text=""
                        #For every responsibility j in article i
                        for j in range(1,50):
                            word1="Responsibility "+str(j)
                            word2="Responsibility "+str(j+1)
                            
                            try:
                                responsibility=word1+extract_text_between_words(string1,word1,word2)[0]
                            except:
                                responsibility=word1+extract_text_till_eof(string1,word1)[0]

                            questions=extract_text_till_eof(responsibility,"Questions:")[0].strip().split('\n')
                            responsibility= word1+extract_text_between_words(responsibility,word1,"Questions:")[0]

                            # ADD the logic to check if a responsibility is relevant or not.
                            react_human_message_1="""   

                                According to Article 3 of EU AI Act a provider is defined as: ‘provider’ means a natural or legal person, public authority, agency or other body that develops an AI system or a general-purpose
                                AI model or that has an AI system or a general-purpose AI model developed and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge.

                                Your client classifies as a provider. The following is one of the responsibility for the provider to perform according to the Article """+str(i)+""" of the EU AI Act mentioned in between the delimiters <>:\n <\n"""+responsibility+"""\n>

                                Your task:
                                Your task is to check if the responsibility is applicable to the client or not.                       

                                Steps:
                                In general you should follow these steps:
                                Step 1: Use the client_info tool to extract client project documentation and analyze the project information.
                                Step 2: Write the responsibility as it is. Check if the responsibility is relevant to the client project. Explain the reason why. The responsibility mentioned is mandatory for the client to perform. It should only be considered as not applicable when the responsibility is based on certain project conditions or the project nature itself. For example, if the client project is classified as low risk but the responsibility mentioned is applicable to high risk system then it means that the responsibility would become irrelevant and not applicable for the client to perform. Another example, is if the client project is about automoblie image detection while the responsibilty mentions that AI systems that exploit vulnerabilities of individuals or groups due to age, disability, or specific social or economic situations, causing significant harm should not be placed on the market then in this case too the responsibilty will become irrelevant since automobile detection does not have any relation to human exploitation or social or economic situations.


                                Output format:
                                ### Final answer:
                                Applicable OR Not applicable
                                Reason: [Mention the reason why]

                                Important note:
                                - You should strictly follow the given output format for your answer
                                """ 
                            
                            inputs_1 = {"messages": [("user", react_human_message_1)]}
                            message=print_stream(react_agent_1.stream(inputs_1, stream_mode="values"))
                            # print('--------------------------MESSAGE------------------------------------------------')
                            # print(message.content)
                            # print('--------------------------MESSAGE------------------------------------------------')
                            if "Not applicable" in message.content:
                                for l in range(len(questions)):
                                    questions[l]=questions[l]+"\nAnswer: Not applicable \n\n"

                                text=text+responsibility+"Questions:\n"+''.join(questions)
                                
                            else:
                                question_answer_text=""
                                for question in questions:                            
                                    react_human_message_2="""
                                According to Article 3 of EU AI Act a provider is defined as: ‘provider’ means a natural or legal person, public authority, agency or other body that develops an AI system or a general-purpose
                                AI model or that has an AI system or a general-purpose AI model developed and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge.

                                Your client classifies as a provider. The following is one of the responsibility for the provider to perform according to the Article """+str(i)+""" of the EU AI Act 
                                followed by a question which acts like a checklist to know if the client is in compliance with that responsibility or not,  mentioned in between the delimiters <>:\n <\n"""+responsibility+"""\n"""+question+"""\n>

                                Your task:
                                Find the answer to the question. The answer would not be given in a straightforward manner so you have to search for it. For example, if the question is 'Does the client project classify as high risk AI system?' then you would find description of the project in the document and you would have to evaluate it yourself whether the client's project classifies as high risk AI system according to the EU AI Act. You can use any tools as required.                        

                                Steps:
                                In general you should follow these steps:
                                Step 1: Use the client_info tool to extract client project documentation and analyze the project information.
                                Step 2: Find the answer to the question. If answer is found then write 'Yes' followed by explaination and reference as to where you found the answer. If answer was not found then simply write your answer as 'No'.


                                You should strictly follow the output format mentioned below only when the responsibility is applicable and do not use markdown format :
                                ### Final answer:
                                Question X (where X is the number of the question) : Write the question exactly as it is.
                                Answer: Yes and explaination along with reference OR No if the answer was not found.

                                Important Note:
                                - You should only explain the reference if the answer is 'Yes'. If the answer is No then you should not write any reason or reference and only write the answer as No.

                                """
                                    inputs_2 = {"messages": [("user", react_human_message_2)]}
                                    message=print_stream(react_agent_1.stream(inputs_2, stream_mode="values"))
                                    message.content ="\nAnswer:"+extract_text_till_eof(message.content,"Answer:")[0].strip()
                                    # print("--------------------ANSWER YES OR NO----------------------------")
                                    # print(message.content)
                                    question_answer_text+=question+message.content+"\n\n"
                                    customText = question + '\n(Article ' + str(i) + ' || Responsibility ' + str(j) + ' ) ' + message.content + '\n\n'
                                    # print(customText)
                                    if ('Answer:Yes' in customText):
                                        filePath1 = os.path.join(timestamp_folder, "Answers", "AnswersYES.txt")
                                    else:
                                        filePath1 = os.path.join(timestamp_folder, "Answers", "AnswersNO.txt")
                                    with open(filePath1, "a", encoding='utf8') as output_file:
                                        output_file.write(customText)
                                text=text+responsibility+question_answer_text
                            # print('--------------------------TEXT------------------------------------------------')
                            # print(text)
                            # print('--------------------------TEXT------------------------------------------------')
                            # with open(f"{timestamp_folder}\\Answers\\Answers_"+str(k)+"\\Answers_"+str(i)+".txt", "w", encoding='utf8') as output_file:
                            #         output_file.write(text)
                            with open(f"{timestamp_folder}/Answers/Answers" + str(i) + ".txt", "w", encoding='utf8') as output_file:
                                output_file.write(text)
                    except:
                        pass
                    
                            
        # Post analysis and generate report
        def extract_number(string):
            # Find all numbers in the string
            numbers = re.findall(r'\d+', string)
            # Convert the first found number to an integer (if you expect only one number)
            return int(numbers[0]) if numbers else None

        def analysis(string):
            matplotlib.use('Agg')
            # Data to plot
            labels = 'Not applicable responsibilities', 'QA- Yes', 'QA- No'
            sizes = [string.count("Answer: Not applicable"), string.count("Answer:Yes"), string.count("Answer:No")]
            colors = ['grey', 'yellowgreen', 'red']
            
            

            explode = [0, 0, 0]  # explode 1st slice
            explode[sizes.index(max(sizes))] = 0.1

            # Plot
            plt.pie(sizes, explode=explode ,labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=100)

            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('EU AI compliance pie diagram')

            pie_chart_path = f"{timestamp_folder}/Full_docs/pie_chart.png"
    
            # Delete the existing pie chart file if it exists
            if os.path.exists(pie_chart_path):
                os.remove(pie_chart_path)
            
            # Save the new pie chart
            plt.savefig(pie_chart_path, dpi=200, bbox_inches='tight')
            plt.close()

            if sizes[2] != 0:
                return """\n\n\n\nSummary:
        The client's project is NOT compliant!!!.
        The number of questions that were successfully answered and compliant were: """+str(sizes[1])+"""\nThe number of questions that were not answered: """+str(sizes[2])+"""\nThe number of questions that were not applicable: """+str(sizes[0])
            else:
                return "The client's project is compliant"

        class PDF(FPDF):
            def header(self):
                if self.page_no() == 1:
                    self.set_font("Arial", "B", 18)
                    self.cell(0, 10, "AI generated report for EU AI Act compliance", 0, 1, "C")

            def add_content_with_ticks(self, content):
                self.set_font("Arial", size=11)
                lines = content.split('\n')

                for line in lines:
                    if "Answer:Yes" in line:
                        line = "      " + line
                        self.image(tick_image, x=self.get_x(), y=self.get_y(), w=5, h=5)
                        self.set_text_color(0, 128, 0)
                        self.multi_cell(0, 10, line, border=0)
                        self.set_text_color(0, 0, 0)
                    elif "Answer:No" in line:
                        line = "     " + line
                        self.image(cross_image, x=self.get_x(), y=self.get_y(), w=5, h=5)
                        self.set_text_color(255, 0, 0)
                        self.multi_cell(0, 10, line, border=0)
                        self.set_text_color(0, 0, 0)
                    elif "Not applicable" in line:
                        line = "     " + line
                        self.set_text_color(128, 128, 128)
                        self.image(grey_image, x=self.get_x(), y=self.get_y(), w=5, h=5)
                        self.multi_cell(0, 10, line, border=0)
                        self.set_text_color(0, 0, 0)
                    elif 'Detailed Report with Articles' in line:
                        self.set_font("Arial", "B", size=18)
                        self.multi_cell(0, 10, line, border=0)
                        self.set_font("Arial", size=11)
                    else:
                        self.multi_cell(0, 10, line, border=0)
                    self.ln(1)  # Add some space after each line

        def create_pdf_with_ticks(content, filename, summary):
            try:
                text = content.encode('latin-1', 'replace').decode('latin-1')
                content = text
                pdf = PDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                
                # Ensure content is encoded in utf-8
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                if isinstance(summary, bytes):
                    summary = summary.decode("utf-8")
        
                # Add fonts
                print("Adding fonts")
                # pdf.add_font("DejaVu", "", dejavu_sans, uni=True)
                # pdf.add_font("DejaVu", "B", dejavu_sans_bold, uni=True)
                
                # Add pie chart image
                # Add pie chart image
                print("Adding pie chart")
                pie_chart_path = os.path.join(timestamp_folder, "Full_docs", "pie_chart.png")
                if os.path.exists(pie_chart_path):
                    pdf.image(pie_chart_path, x=10, y=30, w=150)
                    pdf.ln(110)
                    print("Pie chart added successfully")
                else:
                    print(f"Pie chart not found: {pie_chart_path}")

                print("Adding summary and content")
                
                # pdf.image(f"{timestamp_folder}/Full_docs/pie_chart.png", x=10, y=30, w=150)
                # pdf.ln(110)
                
                # Add summary
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 10, summary)
                
                # Add new page and report details
                pdf.add_page()
                pdf.set_font("Arial", "B", size=18)
                pdf.multi_cell(0, 10, "Overview:")
                pdf.set_font("Arial", size=11)
                pdf.ln(10)
                
                pdf.add_content_with_ticks(content)
                pdf.output(filename,'F')
                
                # Add content with ticks
                # pdf.multi_cell(0, 10, content)
                # print(f"Saving PDF to: {filename}")
                # os.makedirs(os.path.dirname(filename), exist_ok=True)
                # pdf.output(filename)
                print(f"PDF created successfully: {filename}")
            except Exception as e:
                print(f"Error creating PDF: {e}")
                logging.error(f"Error creating PDF: {e}")
                raise

        # path2 = ".\\Articles\\Article "
        string = ""

        print("Processing answers")
        yesAnswers = ""
        noAnswers = ""
        if (os.path.exists(os.path.join(timestamp_folder, "Answers", "AnswersYES.txt"))):
            with open(os.path.join(timestamp_folder, "Answers", "AnswersYES.txt"), "r", encoding='utf8') as file:
                yesAnswers = file.read()
        if (os.path.exists(os.path.join(timestamp_folder, "Answers", "AnswersNO.txt"))):
            with open(os.path.join(timestamp_folder, "Answers", "AnswersNO.txt"), "r", encoding='utf8') as file:
                noAnswers = file.read()
        for i in range(1,114):
            try:
                answer_file_path = os.path.join(timestamp_folder, "Answers", f"Answers{i}.txt")
                # print(f"Processing answer file: {answer_file_path}")
                with open(answer_file_path, "r", encoding='utf8') as file:
                    temp1 = file.read()
                # with open(path2 + str(extract_number(os.path.basename(str(file)))) + ".txt", "r", encoding='utf8') as file:
                #     temp2 = file.read()
                article_number = extract_number(os.path.basename(str(file)))
                article_record = LegalAgentArticles.findOne(article_number)
                if article_record is None:
                    logging.error(f"Article {article_number} not found in database")
                    temp2 = ""
                else:
                    temp2 = article_record['article']
                string += temp2 + "\n\n\n" + temp1

            except Exception as e:
                logging.error(f"Error processing answers for article {i}: {e}")

        logging.info("Post analysis and report generation")
        print("Post analysis and report generation")
        try:
            summary = analysis(string)
            print("Analysis completed")
            # filename = f"{timestamp_folder}/Full_docs/report.pdf"
            filename = os.path.join(timestamp_folder, "Full_docs", "report.pdf")
            print(f"Attemping to create PDF: {filename}")
            # filename = ".\\report.pdf"
            string = yesAnswers + "\n\n\n" + noAnswers + "\n\n\n\n" + 'Detailed Report with Articles'+ '\n\n\n' + string
            create_pdf_with_ticks(string, filename, summary)
            logging.info(f"PDF created successfully: {filename}")
            print("PDF created successfully:{filename}")
            with open(filename, "rb") as f:
                print("Storing file...")
                storeFile(f, "rai-pdf-reports", "report.pdf", processing_id)
            LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Completed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            print("Processing completed and status updated")
        except Exception as e:
            print(f"Error in post analysis and report generation: {e}")
            LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Failed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'errorMessage': str(e)})
            logging.error(f"Error in post analysis and report generation: {e}")

    except Exception as e:
        print(f"Error in process_compliance_advisor: {e}")
        LegalAgentFileProcessing.update({'_id': ObjectId(processing_id)}, {'status': 'Failed', 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'errorMessage': str(e)})
        logging.error(f"Error in process_compliance_advisor: {e}")
    finally:
        if os.path.exists(timestamp_folder):
            print(f"Cleaning up timestamp folder: {timestamp_folder}")
        cleanup_folder(timestamp_folder)