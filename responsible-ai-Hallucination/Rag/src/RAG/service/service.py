"""
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from langchain.document_loaders import PyPDFLoader,DirectoryLoader, TextLoader, CSVLoader, JSONLoader, UnstructuredMarkdownLoader
# from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_community.document_loaders import Docx2txtLoader
import random
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import pickle
from langchain.prompts import PromptTemplate
import os
import shutil
import re
import time
import base64
import uuid
import pymongo
import requests
import io
from pathlib import Path
from sentence_transformers import util
from sentence_transformers import SentenceTransformer
from RAG.config.logger import CustomLogger,request_id_var
import gridfs
from cachetools import Cache
from dotenv import load_dotenv
import traceback
import torch
from RAG.service.geval import gEval
from RAG.dao.AdminDb import mydb, collection, fs, defaultfs
# from azure.cosmos import CosmosClient, exceptions
log=CustomLogger()
MAX_CACHE_SIZE = 20
cache = Cache(maxsize=MAX_CACHE_SIZE)
request_id_var.set("Startup")

try:
    load_dotenv()
    openai_api_type = os.environ.get("OPENAI_API_TYPE")
    openai_api_base = os.environ.get("OPENAI_API_BASE")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai_api_version = os.environ.get("OPENAI_API_VERSION")
    azureaddfileurl=os.getenv("AZUREADDFILE")
    containername=os.getenv("CONTAINERNAME")
    azureblobnameurl=os.getenv("AZUREBLOBNAME")
    dbtypename=os.getenv("DB_TYPE")
    # print(openai_api_version)
except Exception as e:
    log.info("Failed at openai model loading")

try:
    similarity_model = SentenceTransformer("../models/all-MiniLM-L6-v2")
    # similarity_model = SentenceTransformer(r"D:\responsible-ai-fm-moderation\Fm_Moderation\models\all-MiniLM-L6-v2")
    #embedding_function = SentenceTransformerEmbeddings(model_name="../models/all-MiniLM-L6-v2")
    embedding_function = OpenAIEmbeddings()
except Exception as e:
    log.info("Failed at model loading")
    log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")


#with open("../data/DefaultVectorstore.pkl","rb") as file:
    #vectorstore =pickle.load(file)

if os.path.exists("../data/docs/"):
    shutil.rmtree("../data/docs/")
template1 = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, try to make up an creative answer but dont give answer from available document which I have provided you for retrieval. 
            Use three sentences maximum and keep the answer as concise as possible. 
            Always say "thanks for asking!" at the end of the answer. 
            {context}
            Question: {question}
            Helpful Answer:"""
template2 = """Use the following pieces of context to answer the question at the end. 
            if document I provided doesnt have any answer of the questions I asked then Dont give response as The document does not provide information.
            If you don't know the answer, make any creative answer and don't take reference from the document I have provided.
            {context}
            Question: {question}
            Helpful Answer:"""
template4   = """Use the following pieces of context to answer the question. 
            if document I provided doesnt have any answer of the questions I asked then Dont give response as The document does not provide information.
            If you don't know the answer, make any creative answer and don't take reference from the document I have provided.
            {context}
            Question: {question}
            Helpful Answer:"""
template5 ="""Use the following pieces of context to answer the question. 
            If the question does not have any similarity with the document provided, then come up with a creative answer from the internet instead of the uploaded document. 
            If you do not know the answer dont apologize, come up with a creative answer for the question from the internet.
            Make sure there is always a answer generated for the question instead of guidelines restrictions as response.
            Give response in a format Answer,score like this Biggest country is Russia,0.1 and always give score even If You dont have answer
            Here score is a hallucination score which range will be from 0 to 1 if the embeddings I provide in the retrieval is having answer then give score close to 0 otherwise 1 and dont give 0.5.
            Please dont use phrases like "I do not know","Sorry","I apologize","As an AI model I am not allowed" in the response.
            {context}
            Question: {question}
            Helpful Answer:"""
            
template10 ="""Use the following pieces of context to answer the question. If the question does not relate to the provided document or if you are unsure of the answer, create a plausible response based on general knowledge from the internet.

            Ensure that an answer is always generated, avoiding any guideline restrictions as a response. Format your response as follows: `Answer,score`. For example, "The largest country is Russia,0.1". 
            Always include a hallucination score ranging from 0 to 1, where:

            - 0 indicates the answer is highly relevant to the prompt, it is highly realistic, the answer contains no factual errors and the answer is not at all nonsensical.
            - 1 indicates the answer is highly unrelated to the prompt, it is highly implausible or unrealistic, it is completely factually incorrect and highly nonsensical.
            - Scores between 0 and 1 should reflect the degree of confidence based on the relevance and accuracy of the answer. Avoid assigning a score of 0.5.

            Avoid phrases like "I do not know", "Sorry", "I apologize", or "As an AI model, I am not allowed" in your response.

            {context}

            Question: {question}

            Helpful Answer:"""
            
template8 ="""Use the following pieces of context to answer the question. 
            If the question does not have any similarity with the document provided, then come up with a creative answer from the internet instead of the uploaded document. 
            If you do not know the answer dont apologize, come up with a creative answer for the question from the internet.
            Make sure there is always a answer generated for the question instead of guidelines restrictions as response.
            Please dont use phrases like "I do not know","Sorry","I apologize","As an AI model I am not allowed" in the response.
            Engage in a step-by-step thought process to elucidate how the answer was reached. 
            Additionally, correlate the source with the answer in the following format:
            Result: "answer"
            Explanation: "step-by-step reasoning"
            Source: "context/document/internet"
            Make sure the above format is mainatained for all questions.
            
            {context}
            
            Question: {question}
            Helpful Answer:"""
template7 = """Utilize the provided context to formulate a response to the posed question. 
                In instances where the question bears no resemblance to the supplied document, employ creativity to derive an answer from the internet, bypassing the document.
                Should the answer be elusive, refrain from expressions of apology and instead, craft a creative response sourced from the internet. 
                Ensure that every question receives a response, without defaulting to guideline restrictions.
                Respond in the following format: Answer, score.
                For example: "The largest country by land area is Russia, 0.1." 
                Always assign a score, even in the absence of a definitive answer. 
                The score is a hypothetical measure of confidence, ranging from 0 to 1. 
                A score approaching 0 suggests that the provided embeddings contain the answer, while a score closer to 1 indicates the opposite. 
                Avoid assigning a score of 0.5.
                Do not use phrases such as "I do not know," "Sorry," "I apologize," or "As an AI model, I am not allowed" in your response. 
                Engage in a step-by-step thought process to elucidate how the answer was reached. 
                Additionally, correlate the source with the answer in the following format:
                Result: "answer"
                Score: "score"
                Explanation: "step-by-step reasoning"
                Source: "context/document/internet"
                {context}
                Question: {question}
                Helpful Answer:"""
                
template6 ="""Use the following pieces of context to answer the question. 
            If the question does not have any similarity with the document provided, then act like a bloom model and just complete the question.
            Please dont use phrases like "I do not know","Sorry","I apologize","As an AI model I am not allowed" in the response.
            {context}
            Question: {question}
            Helpful Answer:"""


message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
QA_CHAIN_PROMPT = PromptTemplate.from_template(template10)
llm = AzureChatOpenAI(deployment_name=os.getenv("OPENAI_MODEL"), temperature=1)

# conn = pymongo.MongoClient(os.environ.get("MONGO_PATH"))
# db = conn[os.environ.get("DB_NAME")]
# defaultdb = conn[os.environ.get("DEFAULT_DB_NAME")]
# fs=gridfs.GridFS(db)
# defaultfs=gridfs.GridFS(defaultdb)

# def defaultQARetrieval(text):
#     try:
#         starttime = time.time()
#         global output
        
#         res = []
#         log.info("Before llm calling")
#         # with open("../data/DefaultVectorstore.pkl","rb") as file:
#         #     vectorstore =pickle.load(file)
#         # vectorstore = pickle.loads(fs.get_last_version(_id=id+"vectorstore",filename="vectorstore.pkl").read())
#         log.info("Vectorstore loaded")
#         qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), return_source_documents=True,
#                                             chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
#         output = qa_chain({"query": text})
#         rt =time.time()
#         #log.info(output["result"])
#         log.info("After llm calling")
#         textArr = re.split(r'(?<=[.!?])\s+(?=\D|$)', output["result"])
#         fullText = output["result"]
#         return [{"text":fullText}]
#         refusals=["Sorry, as an AI model I am unable to provide this information as it is not present in the provided documents.",
#                 "I dont know","I am unable to determine what you ate today as there is no relevant context or information provided to respond to the question"
#                 "I'm sorry, I cannot answer that as there is no information related"
#                 ]
#         for i in refusals:
#             if promptResponseSimilarity(fullText,i) > 0.7:
#                 return [{"text":fullText,"score":0.20},{"endsrc":[]}]
#         inpoutsim = promptResponseSimilarity(text, fullText)
#         # log.info(f"Similarty score between input and output {inpoutsim}")
#         srcArr = output["source_documents"]
#         maxScore = 0
#         inpsourcesim = 0
#         print(textArr)
#         for i in textArr:
#             simScore = 0
#             cit = ""
#             flag = 0
#             for j in srcArr:
#                 score = promptResponseSimilarity(j.page_content, i)
                
#                 maxScore = max(maxScore,score)
#                 print("#",score)
#                 if flag == 0:
#                     flag = 1
#                     maxScore = max(maxScore, promptResponseSimilarity(j.page_content, fullText))
#                     score2 = promptResponseSimilarity(j.page_content, text)
#                     inpsourcesim = max(score2,inpsourcesim)
#                 if score > simScore:
#                     simScore = score
#                     print(j.page_content)
#                     cit = j.metadata["source"]

#             log.info(simScore)
            
#             log.info(f"Source of document:{cit}")
#             if simScore > 0.6:
#                 res.append({"text": i, "source": cit})  # ,"Score":round(simScore.tolist()[0],2)}])
#             else:
#                 res.append({"text": i, "source": ""})
        
#         queue = []
#         i = 0
#         totalsrc = {}
#         while i< len(res):
#             j = i+1
#             st = res[i]["text"]
#             while j < len(res) and res[i]["source"] == res[j]["source"]:
#                 st += res[j]["text"]
#                 j+=1
#             if res[i]["source"] == "":
#                 queue.append([{"text": st}])
#             else:

#                 log.info(f"source: {id+res[i]['source']}")
#                 log.info(f"filename: {os.path.basename(res[i]['source'])}")
#                 pdf_content = fs.get_last_version(_id=id+os.path.basename(res[i]["source"])).read()
#                 encodedString = base64.b64encode(pdf_content)
#                 if os.path.basename(res[i]["source"]) not in totalsrc:
#                         print(res[i]["source"])
#                         totalsrc[os.path.basename(res[i]["source"])] = encodedString
#                 queue.append([{"text": st, "source": os.path.basename(res[i]["source"]),"base64":encodedString}])
#             i=j
#         # log.info(f"Max score {maxScore}")
#         finalScore = (inpoutsim*0.2 + inpsourcesim*0.4 + maxScore*0.4)
#         if finalScore != 0:
#             queue[-1][0]["score"] = round(1- finalScore.tolist()[0], 2)
#         else:
#             queue[-1][0]["score"] = 1
#         totalsrc =  list(map(lambda item:{"source":item[0],"base64":item[1]},totalsrc.items()))
#         queue.append([{"endsrc": totalsrc}])
        
#         et = time.time()
#         return queue
    
#     except Exception as e:
#         log.info("Failed at Default Qa retrieval")
#         log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")

def QARetrieval(text,id):
    try:
        res = []
        log.info("Before llm calling")
        # with open("../data/docs/"+str(id)+"/DefaultVectorstore.pkl","rb") as file:
        #  vectorstore =pickle.load(file)
        if dbtypename=="mongo":
            vectorstore = pickle.loads(fs.get_last_version(_id=id+"vectorstore",filename="vectorstore.pkl").read())
        else:
            ##################################
            filter = {"id": id + "vectorstore"}
            document = collection.find_one(filter)
            if document:
                vectorstore_binary = document["data"]
                vectorstore = pickle.loads(vectorstore_binary)
                print("Vectorstore retrieved successfully!")
            else:
                print("Document not found!")
            ##################################
        log.info("Vectorstore loaded")
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), return_source_documents=True,
                                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        
        output = qa_chain({"query": text})
        #log.info(output["result"])
        log.info("After llm calling")
        refusals=["Sorry, as an AI model I am unable to provide this information as it is not present in the provided documents.",
                "I dont know","I am unable to determine what you ate today as there is no relevant context or information provided to respond to the question"
                "I'm sorry, I cannot answer that as there is no information related"
                ]
        fullText = output["result"]  
        srcArr = output["source_documents"]  
         
        inpoutsim, ressourcescore, inpsourcesim, tempscore, res, arrForSourceText= scoringmetrics(text,fullText,srcArr)
        pagecontent=" ".join(set(arrForSourceText)).replace("\n"," ")
        fullText = fullText.strip('.')
        fullText=",".join(fullText.split(",")[:-1])
        haluscores=gEval(text,fullText,pagecontent)
        avgmetrics= haluscores["AverageScore"]
        avgmetrics=avgmetrics/5
        maxscore=max(inpoutsim, ressourcescore, inpsourcesim)
        print("maxmaxmax", maxscore)
        if avgmetrics>=0.75:
            haluscore=1-avgmetrics*0.98
        elif avgmetrics>=0.5 and avgmetrics<0.75:
            avgsimilarity=(inpoutsim+ressourcescore+inpsourcesim)/3
            if maxscore>=0.5 and maxscore<0.75:
                wt1=0.20
                wt2=0.80
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
            elif maxscore>=0.75:
                haluscore=1-avgsimilarity*1.15
            elif maxscore<0.5:
                wt1=1
                wt2=1
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
        elif avgmetrics<0.5:
            haluscore=1-avgmetrics
            
        # if haluscore>0.70:
        #     haluscore=random.uniform(0.20,0.40)
            
        queue = []
        i = 0
        totalsrc = {}
        while i< len(res):
            j = i+1
            st = res[i]["text"]
            while j < len(res) and res[i]["source"] == res[j]["source"]:
                st += res[j]["text"]
                j+=1
            if res[i]["source"] == "":
                queue.append([{"text": st}])
            else:

                log.info(f"source: {id+res[i]['source']}")
                queue.append([{"text": st, "source": new_blobname}])
            i=j
        
        # finalScore = (inpoutsim*0.2 + inpsourcesim*0.4 + maxScore*0.4)
        # if finalScore != 0:
        #     queue[-1][0]["score"] = finalScore #round(1- finalScore.tolist()[0], 2)
        # else:
        #     queue[-1][0]["score"] = 1
        totalsrc =  list(map(lambda item:{"source":item[0],"base64":item[1]},totalsrc.items()))
        queue.append([{"endsrc": totalsrc}])
        queue.append({"page_content":" ".join(set(arrForSourceText)).replace("\n"," ")})
        queue.append({"hallucination-score":round(haluscore,3)})
        queue.append({"openai_score":tempscore})
        # queue.append(list(map(lambda item: item["page_content"], srcArr)))
        # queue.append(srcArr)
        et = time.time()
        queue.append(fullText)
        return queue
    

    except Exception as e:
        log.info("Failed at Retrieval")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")

def defaultQARetrievalKepler(text,fileupload,vectorestoreid=None):
    if fileupload==True:
        res = []
        log.info("Before llm calling")
        # with open("../data/docs/"+str(id)+"/DefaultVectorstore.pkl","rb") as file:
        #  vectorstore =pickle.load(file)
        if dbtypename=="mongo":
            vectorstore = pickle.loads(fs.get_last_version(_id=vectorestoreid+"vectorstore",filename="vectorstore.pkl").read())
        else:
            #########################
            # Define the filter to retrieve the document
            filter = {"id": vectorestoreid + "vectorstore"}
            document = collection.find_one(filter)
            if document:
                vectorstore_binary = document["data"]
                vectorstore = pickle.loads(vectorstore_binary)
                print("Vectorstore retrieved successfully!")
            else:
                print("Document not found!")
            #########################
        log.info("Vectorstore loaded")
        retriever=vectorstore.as_retriever()
        # print("llm",llm)
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True,
                                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        
        openai_starttime=time.time()
        output = qa_chain({"query": text})
        openai_endtime=time.time()-openai_starttime
        log.info("After llm calling")
        refusals=["Sorry, as an AI model I am unable to provide this information as it is not present in the provided documents.",
                "I dont know","I am unable to determine what you ate today as there is no relevant context or information provided to respond to the question"
                "I'm sorry, I cannot answer that as there is no information related"
                ]
        fullText = output["result"]
        srcArr = output["source_documents"]  
        log.info(f"final response from the retriever:")
        log.info(fullText)
        inpoutsim, ressourcescore, inpsourcesim, tempscore, res, arrForSourceText= scoringmetrics(text,fullText,srcArr)
        pagecontent=" ".join(set(arrForSourceText)).replace("\n"," ")
        log.info(pagecontent)
        fullText = fullText.strip('.')
        fullText=",".join(fullText.split(",")[:-1])
        haluscores, halureasons=gEval(text,fullText,pagecontent) 
        # print("haluscores",haluscores)
        avgmetrics= haluscores["AverageScore"]
        log.info(f"Average hallucination score: {avgmetrics}")
        avgmetrics=avgmetrics/5
        maxscore=max(inpoutsim, ressourcescore, inpsourcesim)
        print("maxmaxmax", maxscore)
        if avgmetrics>=0.75:
            log.info("avgmetrics>=0.75")
            haluscore=1-avgmetrics*0.98
        elif avgmetrics>=0.5 and avgmetrics<0.75:
            log.info("avgmetrics>=0.5 and avgmetrics<0.75")
            avgsimilarity=(inpoutsim+ressourcescore+inpsourcesim)/3
            if maxscore>=0.5 and maxscore<0.75:
                wt1=0.20
                wt2=0.80
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
            elif maxscore>=0.75:
                haluscore=1-avgsimilarity*1.15
            elif maxscore<0.5:
                wt1=1
                wt2=1
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
        elif avgmetrics<0.5:
            log.info("avgmetrics<0.5")
            haluscore=1-avgmetrics
        print("avgmetrics",avgmetrics)
            
        # if haluscore>0.70:
        #     haluscore=random.uniform(0.20,0.40)
                       
        queue = []
        i = 0
        totalsrc = {}
        while i< len(res):
            j = i+1
            st = res[i]["text"]
            while j < len(res) and res[i]["source"] == res[j]["source"]:
                st += res[j]["text"]
                j+=1
            if res[i]["source"] == "":
                queue.append([{"text": st}])
            else:
                queue.append([{"text": st}])
            i=j
        
        # finalScore = (inpoutsim*0.2 + inpsourcesim*0.4 + maxScore*0.4)
        # if finalScore != 0:
        #     queue[-1][0]["score"] = finalScore #round(1- finalScore.tolist()[0], 2)
        # else:
        #     queue[-1][0]["score"] = 1
        
        unique_pdf_names = set()
        # documents = retriever.get_relevant_documents(text) 
        # for Document in documents:
        #     docJson = Document.dict()
        #     if 'metadata' in docJson.keys():
        #         pdfName = docJson['metadata']['source']#.split('\\')[-1]
        #         pdfName=os.path.basename(pdfName)
        #         unique_pdf_names.add(pdfName)   
        documents = srcArr
        for Document in documents:
            docJson = Document.dict()
            if 'metadata' in docJson.keys():
                pdfName = docJson['metadata']['source']#.split('\\')[-1]
                pdfName=os.path.basename(pdfName)
                unique_pdf_names.add(pdfName)   
        if avgmetrics<=0.70:
            context=["Outside context/Internet"]
            sourceName = context
        else:
            sourceName = unique_pdf_names
        
        totalsrc =  list(map(lambda item:{"source":item[0],"base64":item[1]},totalsrc.items()))
        queue.append([{"endsrc": totalsrc}])
        queue.append({"page_content":" ".join(set(arrForSourceText)).replace("\n"," ")})
        queue.append({"Factual_Halluciantion_score":tempscore})
        queue.append({"source-file":sourceName })
        queue.append({"Faithfulness_Hallucination_score":round(float(haluscore),2)})
        queue.append({"openai_time":round(openai_endtime,2)})
        # queue.append(list(map(lambda item: item["page_content"], srcArr)))
        # queue.append(srcArr)
        et = time.time()
        queue.append(fullText)
        return {"rag_response":queue}

       
    else:
        starttime = time.time()
        log.info("Before llm calling")
        # with open("../data/DefaultVectorstore.pkl","rb") as file:
         #    vectorstore =pickle.load(file)
        # vectorstore = pickle.loads(fs.get_last_version(_id=id+"vectorstore",filename="vectorstore.pkl").read())
        log.info("Vectorstore loaded")
        if vectorestoreid:
            
            vect=cache[int(vectorestoreid)]
            retriever=vect.as_retriever()
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True,
                                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
            
        else:
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), return_source_documents=True,
                                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        openai_starttime=time.time()
        output = qa_chain({"query": text})
        openai_endtime=time.time()-openai_starttime
        print("Time for Gpt call",openai_endtime)
        log.info("After llm calling")
        fullText = output["result"]
        srcArr = output["source_documents"]
        
        tempresponse = fullText.strip('.')
        tempresponse=",".join(tempresponse.split(",")[:-1])
        
        refusals=["Sorry, as an AI model I am unable to provide this information as it is not present in the provided documents.",
                "I dont know","I am unable to determine what you ate today as there is no relevant context or information provided to respond to the question"
                "I'm sorry, I cannot answer that as there is no information related"
                ]
        for i in refusals:
            if promptResponseSimilarity(tempresponse,i) > 0.7:
                return [{"text":tempresponse,"score":0.20},{"endsrc":[]}]
        
        
        inpoutsim, ressourcescore, inpsourcesim, tempscore, res, arrForSourceText= scoringmetrics(text,fullText,srcArr)
        pagecontent=" ".join(set(arrForSourceText)).replace("\n"," ")
        fullText = fullText.strip('.')
        fullText=",".join(fullText.split(",")[:-1])
        haluscores, halureasons=gEval(text,fullText,pagecontent)
        avgmetrics= haluscores["AverageScore"]
        avgmetrics=avgmetrics/5
        maxscore=max(inpoutsim, ressourcescore, inpsourcesim)
        print("maxmaxmax", maxscore)
        if avgmetrics>=0.75:
            haluscore=1-avgmetrics*0.98
        elif avgmetrics>=0.5 and avgmetrics<0.75:
            avgsimilarity=(inpoutsim+ressourcescore+inpsourcesim)/3
            if maxscore>=0.5 and maxscore<0.75:
                wt1=0.20
                wt2=0.80
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
            elif maxscore>=0.75:
                haluscore=1-avgsimilarity*1.15
            elif maxscore<0.5:
                wt1=1
                wt2=1
                haluscore=1-avgsimilarity*wt1-avgmetrics*wt2
        elif avgmetrics<0.5:
            haluscore=1-avgmetrics
        
        # if haluscore>0.70:
        #     haluscore=random.uniform(0.20,0.40)
        
        queue = []
        i = 0
        totalsrc = {}
        while i< len(res):
            j = i+1
            st = res[i]["text"]
            while j < len(res) and res[i]["source"] == res[j]["source"]:
                st += res[j]["text"]
                j+=1
            if res[i]["source"] == "":
                queue.append([{"text": st}])
            else:
                queue.append([{"text": st}])
            i=j
            
        # if finalScore != 0:
        #     queue[-1][0]["score"] = finalScore
        # else:
        #     queue[-1][0]["score"] = 1
        queue.append([{"endsrc": totalsrc}])
        queue.append({"page_content":" ".join(set(arrForSourceText)).replace("\n"," ")})
        queue.append({"Factual_Hallucination_score":tempscore})
        queue.append({"Faithfulness_Hallucination_score":round(haluscore,3)})
        queue.append({"openai_time":round(openai_endtime,2)})
        log.info(f"Total time taken: {round(float(time.time()-starttime),2)}")
        return {"rag_response":queue}

def promptResponseSimilarity (inp,out):
    try:
        # input_embedding = get_embedding(inp)
        # output_embedding = get_embedding(out)
        # return cosine_similarity(input_embedding,output_embedding)
        with torch.no_grad():
            input_embedding = similarity_model.encode(inp, convert_to_tensor=False)
        with torch.no_grad():
            output_embedding = similarity_model.encode(out, convert_to_tensor=False)
        similarity = util.pytorch_cos_sim(input_embedding, output_embedding)
        return max(similarity)
    except Exception as e:
        log.info("Failed at promptResponseSimilarity")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}") 

def scoringmetrics(text,fullText,srcArr):
    try:
        res = []
        fullText = fullText.strip('.')
        try:
            tempscore=float(fullText.split(",")[-1].strip())
        except:
            tempscore=1
        
        # fullText = fullText.rsplit(',', 1)[0]
        fullText=",".join(fullText.split(",")[:-1])
        textArr = re.split(r'(?<=[.!?])\s+(?=\D|$)', fullText)
        
        inpoutsim = promptResponseSimilarity(text, fullText)
        
        ressourcescore = 0
        inpsourcesim = 0
        arrForSourceText=[]
        print(textArr)
        for i in textArr:
            simScore = 0
            cit = ""
            flag = 0
            for j in srcArr:
                score = promptResponseSimilarity(j.page_content, i)
                arrForSourceText.append(j.page_content)
                ressourcescore = max(ressourcescore,score)
                print("#",score)
                if flag == 0:
                    flag = 1
                    ressourcescore = max(ressourcescore, promptResponseSimilarity(j.page_content, fullText))
                    score2 = promptResponseSimilarity(j.page_content, text)
                    inpsourcesim = max(score2,inpsourcesim)
                if score > simScore:
                    simScore = score
                    # print(j.page_content)
                    cit = j.metadata["source"]
                    # pdfName = os.path.basename(cit)
                    # print(cit)
            log.info(simScore)
            #print(cit)
            if simScore > 0.5:
                res.append({"text": i, "source": cit})  # ,"Score":round(simScore.tolist()[0],2)}])
            else:
                res.append({"text": i, "source": ""})
        
        
        # log.info(f"Max score {maxScore}")
        # if maxScore<0.3:
        #     finalScore = round(1-(inpoutsim*0.2 + inpsourcesim*0.4 + maxScore*0.4).tolist()[0],2)
        # elif maxScore>0.45:
        #     tempscore=0.2
        #     finalScore=0.2
        # else:
        #     finalScore = round(1-(inpoutsim*0.2 + maxScore*0.8).tolist()[0],2)
            
        return inpoutsim, ressourcescore, inpsourcesim, tempscore, res, arrForSourceText
    
    except Exception as e:
            log.info("Failed at Scoring metrics")
            log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")


# def load_word(file_path):
#     doc = Document(file_path)
#     return [{"text": "\n".join([para.text for para in doc.paragraphs]), "metadata": {"source": file_path}}]

def get_loader(file_path):
    if file_path.endswith('.pdf'):
        return PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        return TextLoader(file_path)
    elif file_path.endswith('.csv'):
        return CSVLoader(file_path)
    elif file_path.endswith('.docx'):
        return Docx2txtLoader(file_path)
    # elif file_path.endswith('.jpg') or file_path.endswith('.png'):
    #     return UnstructuredImageLoader(file_path)
    # elif file_path.endswith('.json'):
    #     return JSONLoader(file_path, jq_schema='.messages[].content', text_content=False)
    # elif file_path.endswith('.md'):
    #     return UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

def path_check(safe_path):
    if re.match(r'^[\w\-\\\/\s.]+$', str(safe_path)):
        return safe_path
    else:
        raise ValueError(f"Invalid path: {safe_path}")

def createvector(payload):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        print("Chunking")
        st = time.time()
        id = uuid.uuid4().hex
        path = "../data/docs/"+str(id)+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        blobnames=[]
        for i in payload:
            # with open(filepath, "rb") as file:
            #     #Create a dictionary with the file data
            #     files={'file': file.file}
            contents = i.file.read()
            filename = i.filename
            response = requests.post(url=azureaddfileurl, files={"file": (filename, contents)}, data={"container_name": containername}, headers=None, verify=False)
            
            if response.status_code == 200:
                global new_blobname, blobname_output
                blobname_output = response.json()['blob_name']
                blobnames.append(blobname_output)
                base_name, file_ext = os.path.splitext(blobname_output)
                newbasename = blobname_output.rsplit("_", 1)[0]
                new_blobname = f"{newbasename}{file_ext}"
                
                log.info(f"File uploaded successfully. Blob name: {blobname_output}, Container name: {containername}")
            else:
                log.info(f"Error uploading file': {response.status_code} - {response.text}")
                    
            blobnameurl= f"{azureblobnameurl}blob_name={blobname_output}&container_name={containername}"
            print(blobnameurl, blobname_output, containername)
            getblob_response = requests.get(url=blobnameurl, data={"blob_name": blobname_output,"container_name": containername}, headers=None, verify=False, timeout=10)
                
            safe_path = Path(path) / new_blobname
            new_input_path = path_check(safe_path)
            with open(str(new_input_path), "wb") as buffer:
                shutil.copyfileobj(io.BytesIO(getblob_response.content), buffer)
            
        # loader = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        # data = loader.load()
        data = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    loader = get_loader(file_path)
                    if callable(loader):
                        data.extend(loader(file_path))
                    else:
                        data.extend(loader.load())
                except ValueError as e:
                    log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
        
        all_splits = text_splitter.split_documents(data)
        global qa_chain
        vectorstore = None
        vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding_function)
        log.info("AftereVector")
        # unique_id = str(uuid.uuid4())
        if dbtypename=="mongo":
            fs.put(pickle.dumps(vectorstore),filename="vectorstore.pkl",_id=id+"vectorstore")
        else:
            vectorstore_binary = pickle.dumps(vectorstore)
            document = {"id": id + "vectorstore", "data": vectorstore_binary}
            collection.insert_one(document)
        
        if os.path.exists("../data/docs/"+str(id)+"/"):
            print("Exists")
            shutil.rmtree("../data/docs/"+str(id)+"/")
        return {"id": id, "blobname": blobnames}
    
    except Exception as e:
        log.info("Failed at createvector")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
       

# def FileUploadtodb(payload):
#     try:
#         # for i in payload:
#         #     print(i.filename)
#         #     with defaultfs.new_file(filename= i.filename,content_type="application/pdf",_id=i.filename) as f:
#         #         shutil.copyfileobj(i.file,f)
#         for i in payload:
#             # with open(filepath, "rb") as file:
#             #     #Create a dictionary with the file data
#             #     files={'file': file.file}
#             contents = i.file.read()
#             filename = i.filename
#             response = requests.post(url=azureaddfileurl, files={"file": (filename, contents)}, data={"container_name": containername}, headers=None, verify=False)
            
#             if response.status_code == 200:
#                 global default_blobname_output
#                 default_blobname_output = response.json()['blob_name']
#                 log.info(f"File uploaded successfully. Blob name: {default_blobname_output}, Container name: {containername}")
#             else:
#                 log.info(f"Error uploading file': {response.status_code} - {response.text}")
            
#         return 1
#     except Exception as e:
#         log.info("Failed at Upload to db")
#         log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")

# def dbupdate():
#     try:
#         if not os.path.exists("../data/temp"):
#             os.makedirs("../data/temp")
#         blobnameurl= f"{azureblobnameurl}blob_name={default_blobname_output}&container_name={containername}"
#         getblob_response = requests.get(url=blobnameurl, data={"blob_name": default_blobname_output,"container_name": containername}, headers=None, verify=False)
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
#         with open("../data/temp/"+ default_blobname_output, "wb") as buffer:
#             shutil.copyfileobj(io.BytesIO(getblob_response.content), buffer)
#         loader = DirectoryLoader("../data/temp/", glob="**/*.pdf", loader_cls=PyPDFLoader)
#         data = loader.load()
#         print(data)
#         all_splits = text_splitter.split_documents(data)
#         #log.info("BeforeVector",all_splits)
#         global vectorstore,qa_chain
#         vectorstore = None
#         vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding_function)
#         #change
#         # retriever = faiss_index.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.6})
#         with open("../data/DefaultVectorstore.pkl","wb") as file:
#             pickle.dump(vectorstore,file)
#         if os.path.exists("../data/temp/"):
#             print("Exists")
#             shutil.rmtree("../data/temp/")
#     except Exception as e:
#         log.info("Failed at VectorestoreUpdate")
#         log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
    
#     # encodedString = base64.b64encode(pdf_content)

def show_score(prompt, response, sourcearr):
    try:        
        log.info("Showing Scores")
        response = response.strip('.')  
        response=",".join(response.split(",")[:-1])
        responseArr = re.split(r'(?<=[.!?])\s+(?=\D|$)', response)

        inpoutsim = promptResponseSimilarity(prompt, response)
  
        maxScore = 0
        inpsourcesim = 0
        for i in responseArr:
            simScore = 0   
            flag = 0
            for j in sourcearr:
                score = promptResponseSimilarity(j, i)
                maxScore = max(maxScore,score)
                
                if flag == 0:
                    flag = 1
                    maxScore = max(maxScore, promptResponseSimilarity(j, response))
                    score2 = promptResponseSimilarity(j, prompt)
                    inpsourcesim = max(score2,inpsourcesim)
                if score > simScore:
                    simScore = score        
        
        if maxScore<0.3:            
            finalScore = round(1-(inpoutsim*0.2 + inpsourcesim*0.4 + maxScore*0.4).tolist()[0],2)
        elif maxScore>0.45:           
            finalScore=0.2
        else:         
            finalScore = round(1-(inpoutsim*0.2 + maxScore*0.8).tolist()[0],2)
        score = {"score":finalScore}
        return score

    except Exception as e:
            log.info("Failed at Show_Score")
            log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
