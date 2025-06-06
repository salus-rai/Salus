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


class SubDimensionDb:
    mycol = mydb["SubDimension"]
    def findOne(id):
        values=SubDimensionDb.mycol.find({"_id":id},{})[0]
        # print(values)
        values=AttributeDict(values)
        return values
    def findall(query):
        value_list=[]
        values=SubDimensionDb.mycol.find(query,{})
        for v in values:

            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    def create(values):
         value=AttributeDict(values)
         localTime = time.time()
         mydoc = {
        "_id":localTime,
        "Id":localTime,
        "DimensionId":value.dID,
        "SubDimensionId":value.SDId,
        "SubDimensionName":value.SubDimName,
        "SubDimensionDesc":value.SubDimDesc,
        "isActive":"Y",
        "CreatedDateTime": datetime.datetime.now(),
        "LastUpdatedDateTime": datetime.datetime.now(),
         }
         SubDimensionCreatedData = SubDimensionDb.mycol.insert_one(mydoc)
         return SubDimensionCreatedData.inserted_id
    
    def update(id,value:dict):
      
        newvalues = { "$set": value }
        SubDimensionUpdatedData=SubDimensionDb.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 
        return SubDimensionUpdatedData.acknowledged
    
    def delete(id):
        return SubDimensionDb.mycol.delete_many({"_id":id}).acknowledged
        # DocProcDtl.mycol.delete_many({})
        # Docpagedtl.mycol.delete_many({})
    
    