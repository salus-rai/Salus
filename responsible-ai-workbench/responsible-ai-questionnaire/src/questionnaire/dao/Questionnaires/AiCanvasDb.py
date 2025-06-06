"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import pymongo
import datetime,time
from questionnaire.dao.DatabaseConnection import DB
from questionnaire.config.logger import CustomLogger
from dotenv import load_dotenv
load_dotenv()
log = CustomLogger()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


mydb=DB.connect()

class AICanvasDb:
    mycol = mydb["AICanvas"]
    def findOne(id):
        values=AICanvasDb.mycol.find({"_id":id},{})[0]
        # print(values)
        values=AttributeDict(values)
        return values
    def findall(query):
        value_list=[]
        values=AICanvasDb.mycol.find(query,{})
        for v in values:
            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    def create(values):
        value=AttributeDict(values)
        localTime = time.time()
        mydoc = {
        "_id":localTime,
        "useCaseNameId":value.useCaseNameId,
        "UserId":value.UserId,
        "AICanvasResponse": value.AICanvasResponse.dict(),
        "CreatedDateTime": datetime.datetime.now(),
        "LastUpdatedDateTime": datetime.datetime.now()

        } 
        ResponseCreatedData = AICanvasDb.mycol.insert_one(mydoc)
        return ResponseCreatedData.inserted_id
    def update(id,value:dict):    
        newvalues = { "$set": value }
        ResponseUpdatedData=AICanvasDb.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 
        return ResponseUpdatedData.acknowledged
    def delete(id):
        return AICanvasDb.mycol.delete_many({"_id":id}).acknowledged