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

class LegalAgentAnnex:
    mycol = mydb["LegalAgentAnnex"]
    def findOne(annexNumber):
        result=LegalAgentAnnex.mycol.find_one({'annexNumber': annexNumber})
        if result:
            return result
        else:
            return None
        
    def findall(query):
        value_list=[]
        values=LegalAgentAnnex.mycol.find(query,{})
        for v in values:
            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    def create(annexData,annexNumber):
        localTime = time.time()
        mydoc = {
            "_id": localTime,
            "annexNumber": annexNumber,
            "annex": annexData,
            # "telemetryLink": value.telemetryLink,
        }

        # Check if a document with the same annexNumber already exists
        existing_doc = LegalAgentAnnex.mycol.find_one({"annexNumber": annexNumber})
        if existing_doc:
            update_result = LegalAgentAnnex.mycol.update_one(
                {"annexNumber": annexNumber},
                {"$set": {
                    "annex": annexData,
                }}
            )
            return update_result.acknowledged
        else:
            # Insert a new document
            created = LegalAgentAnnex.mycol.insert_one(mydoc)
            return created.acknowledged

