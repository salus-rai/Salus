"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import shutil
import pymongo
import datetime,time
from docProcess.dao.DatabaseConnection import DB
from dotenv import load_dotenv
from docProcess.config.logger import CustomLogger
from gridfs import GridFS
from bson import objectid

load_dotenv()
log = CustomLogger()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


mydb=DB.connect()


class docDb:
    mycol = mydb["ResponseRegistery"]
    fs=GridFS(mydb)
    def findOne(id):
        """
        Retrieve a single document from the database collection by its unique identifier.
        Args:
            id (str): The unique identifier of the document to retrieve.
        Returns:
            AttributeDict: The document retrieved from the database, converted into an AttributeDict object.
        Raises:
            IndexError: If no document is found with the given identifier.
        """
        
        values=docDb.mycol.find({"_id":id},{})[0]
        # print(values)
        values=AttributeDict(values)
        return values
    def findall(query):
        """
        Retrieve all documents from the database collection that match the given query.
        Args:
            query (dict): A dictionary specifying the query criteria to filter documents.
        Returns:
            list: A list of AttributeDict objects, where each object represents a document 
                  from the database that matches the query.
        """
        
        value_list=[]
        values=docDb.mycol.find(query,{})
        for v in values:

            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    
    def create(value):
         """
        Creates a new document entry in the database.
        Args:
            value (dict): A dictionary containing the following keys:
                - userId (str): The ID of the user creating the document.
                - fileName (str): The name of the file associated with the document.
                - categories (list): A list of categories associated with the document.
                - type (str): The type of the document.
        Returns:
            ObjectId: The ID of the newly inserted document in the database.
        Notes:
            - The `_id` and `docId` fields are generated using the current local time.
            - The `CreatedDateTime` and `LastUpdatedDateTime` fields are set to the current datetime.
            - The `status` field is initialized to "Not Started".
        """
         
         value=AttributeDict(value)
         localTime = time.time()
         mydoc = {
        "_id":localTime,
        "docId":localTime,
        "userId":value.userId,
        "fileName":value.fileName,
        # "inputFileId":value.fileid,
        "categories":value.categories,
        "status":"Not Started",
        "type":value.type,
        "CreatedDateTime": datetime.datetime.now(),
        "LastUpdatedDateTime": datetime.datetime.now(),
         }
         docProccessData = docDb.mycol.insert_one(mydoc)
         return docProccessData.inserted_id
    
    def update(id,value:dict):
        """
        Updates a document in the database with the specified ID and new values.
        Args:
            id (Any): The unique identifier of the document to be updated.
            value (dict): A dictionary containing the fields and their new values to update in the document.
        Returns:
            bool: True if the update operation was acknowledged by the database, False otherwise.
        Logs:
            Logs the new values being set in the document.
        """
        
        newvalues = { "$set": value }
        docProccessData=docDb.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 
        return docProccessData.acknowledged
    
    def delete(id):
        """
        Deletes documents from the database collection based on the provided ID.
        Args:
            id (str or ObjectId): The unique identifier of the document(s) to be deleted.
        Returns:
            None
        """
        
        docDb.mycol.delete_many({"_id":id})
        # DocProcDtl.mycol.delete_many({})
        # Docpagedtl.mycol.delete_many({})
    
    
