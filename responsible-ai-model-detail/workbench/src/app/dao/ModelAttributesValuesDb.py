"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pymongo
import datetime,time

# from batch_processing.dao.DatabaseConnection import DB
# from batch_processing.dao.DocPageDtl import *
# from batch_processing.dao.DocProcDtlDb import DocProcDtl
from dotenv import load_dotenv
# from batch_processing.config.logger import CustomLogger
from app.config.logger import CustomLogger
from app.dao.DatabaseConnection import DB

load_dotenv()
log = CustomLogger()

mydb = DB.connect()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ModelAttributesValues:

    mycol = mydb["ModelAttributesValues"]


    def findOne(id):

        values = ModelAttributesValues.mycol.find({"_id":id},{})[0]
        values = AttributeDict(values)

        return values
    

    def findall(query):

        value_list = []
        values = ModelAttributesValues.mycol.find(query,{})
        for v in values:
            v = AttributeDict(v)
            value_list.append(v)

        return value_list
    

    def create(values):
         
        value = AttributeDict(values)
        localTime = time.time()
        time.sleep(1/1000)
        mydoc = {
            "_id":localTime,
            "ModelAttributeValuesId":localTime,
            "ModelAttributeId":value.modelAttributeId,
            "ModelId":value.modelId,
            "ModelAttributeValues": value.modelAttributeValues,
            "IsActive": "Y",
            "CreatedDateTime": datetime.datetime.now(),
            "LastUpdatedDateTime": datetime.datetime.now(),
        }
        modelAttributesValuesCreatedData = ModelAttributesValues.mycol.insert_one(mydoc)

        return modelAttributesValuesCreatedData.inserted_id
    
    
    def update(id,value:dict):
      
        newvalues = { "$set": value }
        modelAttributesValuesUpdatedData = ModelAttributesValues.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 

        return modelAttributesValuesUpdatedData.acknowledged
    
    def createForBatchData(values):
         
        value = AttributeDict(values)
        localTime = time.time()
        time.sleep(1/1000)
        # print("values=====",values)
        mydoc = {
            "_id":localTime,
            "ModelAttributeValuesId":localTime,
            "ModelAttributeId":value['ModelAttributeId'],
            "ModelId":value.modelId,
            "ModelAttributeValues": value['ModelAttributevalues'],
            "IsActive": "Y",
            "BatchId": value['BatchId'],
            "CreatedDateTime": datetime.datetime.now(),
            "LastUpdatedDateTime": datetime.datetime.now(),
        }
        modelAttributesValuesCreatedData = ModelAttributesValues.mycol.insert_one(mydoc)
    def delete(query):
        
        ModelAttributesValues.mycol.delete_many(query)
        # DocProcDtl.mycol.delete_many({})
        # Docpagedtl.mycol.delete_many({})