"""
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from langchain.document_loaders import PyPDFLoader,DirectoryLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import AzureChatOpenAI
import os
import shutil
import time
import uuid
from RAG.config.logger import CustomLogger,request_id_var
import traceback
import requests
import io
import re
from pathlib import Path
from RAG.service.service import cache,MAX_CACHE_SIZE,embedding_function,defaultfs, azureblobnameurl, containername

log=CustomLogger()
request_id_var.set("Startup")

llm = AzureChatOpenAI(deployment_name=os.getenv("OPENAI_MODEL"), temperature=1)

def get_loader(file_path):
    if file_path.endswith('.pdf'):
        return PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        return TextLoader(file_path)
    elif file_path.endswith('.csv'):
        return CSVLoader(file_path)
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

def caching(blobname):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)  

        st = time.time()
        uid = uuid.uuid4().hex
        path = "../data/docs/"+str(uid)+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        for name in blobname:
            # pdf_content=defaultfs.get_last_version(_id=float(i))
            # with open(path+pdf_content.filename, "wb") as buffer:
            #     shutil.copyfileobj(pdf_content, buffer)
            new_blobname = name.replace(" ", "%20")
            blobnameurl= f"{azureblobnameurl}blob_name={name}&container_name={containername}"
            getblob_response = requests.get(url=blobnameurl, data={"blob_name": name,"container_name": containername}, headers=None, verify=False)
            safe_path = Path(path) / name
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
        #log.info("BeforeVector",all_splits)
        vs = FAISS.from_documents(documents=all_splits, embedding=embedding_function)
        vectorindex=0
        if len(cache) == MAX_CACHE_SIZE:
            vectorindex=cache.popitem()[0]
        cache[id(vs)] = vs
        if os.path.exists("../data/docs/"+str(uid)+"/"):
            print("Exists")
            shutil.rmtree("../data/docs/"+str(uid)+"/")
        return id(vs),vectorindex
    
    except Exception as e:
        log.error("Failed at Vectorestore Caching")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")

def removeCache(id):
    try:
        if id in cache:
            cache.__delitem__(id)
            return id
        else:
            return -1
    except Exception as e:
        log.error("Failed at Remove caching")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
