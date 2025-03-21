'''
© <2023> Infosys Limited, Bangalore, India. All Rights Reserved.
 Version: 
Except for any free or open source software components embedded in this Infosys proprietary software program (“Program”), this Program is protected by copyright laws, international treaties and other pending or existing intellectual property rights in India, the United States and other countries. Except as expressly permitted, any unauthorized reproduction, storage, transmission in any form or by any means (including without limitation electronic, mechanical, printing, photocopying, recording or otherwise), or any distribution of this Program, or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under the law.
'''
import pymongo
import datetime,time
from profanity.dao.DatabaseConnection import DB
from dotenv import load_dotenv
from profanity.config.logger import CustomLogger

load_dotenv()
log = CustomLogger()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


mydb=DB.connect()



class TelemetryFlag:
    mycol = mydb["TelemetryFlag"]
    def findOne(id):
        values=TelemetryFlag.mycol.find({"_id":id},{})[0]
        # print(values)
        values=AttributeDict(values)
        return values
    def findall(query):
        value_list=[]
        values=TelemetryFlag.mycol.find(query,{})
        for v in values:

            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    def create(value):
         value=AttributeDict(value)
         localTime = time.time()
         mydoc = {
        "_id":localTime,
        "Module":value.module,
        "TelemetryFlag":False,
        "CreatedDateTime": datetime.datetime.now(),
        "LastUpdatedDateTime": datetime.datetime.now(),
         }
         PtrnRecogCreatedData = TelemetryFlag.mycol.insert_one(mydoc)
         return PtrnRecogCreatedData.inserted_id
    
    def update(id,value:dict):
      
        newvalues = { "$set": value }
        PtrnRecogUpdatedData=TelemetryFlag.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 
        return PtrnRecogUpdatedData.acknowledged
    
    def delete(id):
        TelemetryFlag.mycol.delete_many({"_id":id})
        # DocProcDtl.mycol.delete_many({})
        # Docpagedtl.mycol.delete_many({})
    
    