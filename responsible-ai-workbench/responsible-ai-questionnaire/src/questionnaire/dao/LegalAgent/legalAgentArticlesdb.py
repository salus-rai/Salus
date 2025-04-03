"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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

class LegalAgentArticles:
    mycol = mydb["LegalAgentArticles"]
    def findOne(articleNumber):
        result=LegalAgentArticles.mycol.find_one({'articleNumber': articleNumber})
        if result:
            return result
        else:
            return None
        
    def findall(query):
        value_list=[]
        values=LegalAgentArticles.mycol.find(query,{})
        for v in values:
            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    def create(articleData,articleNumber):
        localTime = time.time()
        mydoc = {
            "_id": localTime,
            "articleNumber": articleNumber,
            "article": articleData,
            # "telemetryLink": value.telemetryLink,
        }

        # Check if a document with the same articleNumber already exists
        existing_doc = LegalAgentArticles.mycol.find_one({"articleNumber": articleNumber})
        if existing_doc:
            update_result = LegalAgentArticles.mycol.update_one(
                {"articleNumber": articleNumber},
                {"$set": {
                    "article": articleData,
                }}
            )
            return update_result.acknowledged
        else:
            # Insert a new document
            created = LegalAgentArticles.mycol.insert_one(mydoc)
            return created.acknowledged

