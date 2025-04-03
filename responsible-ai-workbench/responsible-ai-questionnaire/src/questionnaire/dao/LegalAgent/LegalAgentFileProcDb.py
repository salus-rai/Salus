"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from bson import ObjectId
from gridfs import GridFS
import pymongo
from datetime import datetime
import time
from dotenv import load_dotenv
from questionnaire.config.logger import CustomLogger
from questionnaire.dao.DatabaseConnection import DB
load_dotenv()
log = CustomLogger()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


mydb=DB.connect()

class LegalAgentFileProcessing:
    mycol = mydb["LegalAgentFileProcessing"]
    reportFile = GridFS(mydb)

    def findOne(questionNumber):
        result=LegalAgentFileProcessing.mycol.find_one({'questionNumber': questionNumber})
        if result:
            return result
        else:
            return None
        
    def create(data):
        # Check if a document with the same report id already exists
        existing_doc = LegalAgentFileProcessing.mycol.find_one({"_id": data["_id"]})
        if(existing_doc):
            return False
        else:
            created = LegalAgentFileProcessing.mycol.insert_one(data)
        return created.acknowledged
    
    def update(query:dict,value:dict):
        if(query == None):
            return False
        newValues = { "$set": value }
        updatedData = LegalAgentFileProcessing.mycol.update_one(query,newValues)
        return updatedData.acknowledged
    
    def findall(userId):
        try:
            query = {"user_id": userId}
            value_list = []
            values = LegalAgentFileProcessing.mycol.find(query)
            print(values,query)
            for v in values:
            # Convert ObjectId to string if necessary
                if '_id' in v and isinstance(v['_id'], ObjectId):
                    v['_id'] = str(v['_id'])
                print(v)
                value_list.append(v)
            return value_list
        except Exception as e:
            log.error(f"Error finding values: {str(e)}")
            return []
