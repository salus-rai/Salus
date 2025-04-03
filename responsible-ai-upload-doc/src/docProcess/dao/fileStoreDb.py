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


class fileStoreDb:
    # mycol = mydb["ResponseRegistery"]
    fs=GridFS(mydb)
    def findOne(id):
        """
        Retrieves a file or document from the database based on the provided ID.
        Args:
            id (str): The unique identifier of the file or document to retrieve.
        Returns:
            dict: A dictionary containing the following keys if the file is found:
                - "fileName" (str): The name of the file.
                - "contentType" (str): The MIME type of the file.
                - "data" (bytes): The content of the file.
            If the file is not found, returns an AttributeDict object with the retrieved values.
        """
        
        file=fileStoreDb.fs.find_one({"_id":id})
        if file:
            content=file.read()
            return {"fileName":file.filename,"contentType":file.contentType, "data":content}
        # values=fileStoreDb.mycol.find({"_id":id},{})[0]
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
                  from the database collection that matches the query.
        """
        
        value_list=[]
        values=fileStoreDb.mycol.find(query,{})
        for v in values:

            v=AttributeDict(v)
            value_list.append(v)
        return value_list
    
    def create(value):
         """
        Creates a new file in the file storage database.
        Args:
            value (dict): A dictionary containing the file details. It should have the following keys:
                - fileName (str): The name of the file.
                - type (str): The content type of the file (e.g., MIME type).
                - file (file-like object): The file object to be stored.
        Returns:
            any: The unique identifier (_id) of the newly created file in the database.
        Raises:
            Exception: If there is an error during the file creation process.
        """
        
         value=AttributeDict(value)
         fileid:any
         with fileStoreDb.fs.new_file(_id=time.time(),filename=value.fileName,content_type=value.type) as f:
             shutil.copyfileobj(value.file,f)
             fileid=f._id
           
         return fileid
    
    def update(id,value:dict):
        """
        Updates a document in the database collection with the specified ID.
        Args:
            id: The unique identifier (_id) of the document to be updated.
            value (dict): A dictionary containing the fields and values to update in the document.
        Returns:
            bool: True if the update operation was acknowledged by the database, False otherwise.
        Logs:
            Logs the updated values being set in the document.
        """
        
        newvalues = { "$set": value }
        docProccessData=fileStoreDb.mycol.update_one({"_id":id},newvalues)
        log.debug(str(newvalues)) 
        return docProccessData.acknowledged
    
    def delete(id):
        """
        Deletes documents from the fileStoreDb collection based on the provided ID.
        Args:
            id (Any): The unique identifier of the documents to be deleted.
        Returns:
            None
        """
        
        fileStoreDb.mycol.delete_many({"_id":id})
        # DocProcDtl.mycol.delete_many({})
        # Docpagedtl.mycol.delete_many({})
    
    