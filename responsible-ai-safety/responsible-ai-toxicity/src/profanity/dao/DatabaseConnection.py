'''
© <2023> Infosys Limited, Bangalore, India. All Rights Reserved.
 Version: 
Except for any free or open source software components embedded in this Infosys proprietary software program (“Program”), this Program is protected by copyright laws, international treaties and other pending or existing intellectual property rights in India, the United States and other countries. Except as expressly permitted, any unauthorized reproduction, storage, transmission in any form or by any means (including without limitation electronic, mechanical, printing, photocopying, recording or otherwise), or any distribution of this Program, or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under the law.
'''

import os
import pymongo

from dotenv import load_dotenv
from profanity.config.logger import CustomLogger
import sys
load_dotenv()

log = CustomLogger()


class DB:
    def connect():
        try:
            myclient = pymongo.MongoClient(os.getenv("MONGO_PATH")) 
            mydb = myclient[os.getenv("DB_NAME")]
            # myclient = pymongo.MongoClient("mongodb://localhost:27017")
            # mydb = myclient["rai_profanity"]
            return mydb
        except Exception as e:
            log.info(str(e))
            sys.exit()
            
            