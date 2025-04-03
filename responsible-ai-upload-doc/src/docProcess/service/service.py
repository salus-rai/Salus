"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import json
import threading
import requests

import base64
from io import BytesIO
import shutil
# from docProcess.mapper.mapper import DocList
import os 
from dotenv import load_dotenv
import tempfile


from fastapi.responses import FileResponse, StreamingResponse
from docProcess.dao.DatabaseConnection import DB

from docProcess.dao.DocProccessDb import docDb
from docProcess.dao.fileStoreDb import fileStoreDb as fileDb
load_dotenv()

def customeMask(file_content, maskImage_content,fileName, reqUrl, docid):
    
    """
        Sends a POST request with a video file and a mask image to a specified URL, processes the response, 
        and updates the document status in the database.
        Args:
            file_content (bytes): The content of the video file to be sent.
            maskImage_content (bytes): The content of the mask image file to be sent.
            fileName (str): The name of the video file.
            reqUrl (str): The URL to which the POST request is sent.
            docid (str): The document ID used to update the database.
        Raises:
            requests.HTTPError: If the HTTP request fails.
            Exception: For any other exceptions that occur during processing.
        Notes:
            - The function expects the server to return a JSON response containing a base64-encoded video.
            - The database is updated with the status "Failed" if an error occurs.
            - The commented-out code suggests additional functionality for saving the processed video 
              and updating the database with the result file ID, but it is currently not active.
        """
    
    try:
        filetype = "video/mp4"
        post_files = {
            "payload": (fileName, file_content),
            "maskImage": ("mask.png", maskImage_content)
        }
        response = requests.request("POST", reqUrl, files=post_files)
        response.raise_for_status()
        data = response.json()
        file_content = data.get('video')
        file_content_bytes = base64.b64decode(file_content)
        # print(data)
        # file_content = data.get('video')
        # rf = docDb.fs.new_file(filename=fileName, content_type=filetype)
        # rf.write(file_content_bytes)
        # docDb.update(docid, {"resultFileId": rf._id, "status": "Completed"})
        # rf.close()
    except requests.HTTPError as http_err:
        docDb.update(docid, {"status": "Failed"})
    except Exception as err: 
        docDb.update(docid, {"status": "Failed"})
        
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# localStore="../fileStore/"
class DocProcess:
    def storeFile(file,filetype,fileName,docid):
        
        """
            Uploads a file to an Azure storage container and updates the document database with the file's storage link.
            Args:
                file (file-like object): The file to be uploaded.
                filetype (str): The type of the file, used as the container name in Azure storage.
                fileName (str): The name of the file to be stored.
                docid (str): The document ID to update in the database.
            Returns:
                bytes: The response content from the Azure storage API if the upload is successful.
                bool: False if the upload fails after three attempts.
            Raises:
                Exception: If an error occurs during the file upload process.
            """
        
        surl=os.getenv("AZURE_STORE_ADD_API")
        # file=BytesIO(data)
        
        # with open(fileName, "wb") as f:
        #     f.write(data)
        # file=open(fileName,"rb")
        print(file)
        file={"file":file}
        payload={"container_name":filetype}
        for i in range(3):
            try:
                print("==========================================")
                res=requests.post(url=surl,files=file,data=payload)
                storageDetails=res.json()
                print(storageDetails["blob_name"])
                storelink=os.getenv("AZURE_STORE_GET_API")+"?blob_name="+storageDetails["blob_name"].replace(" ","%20")+"&container_name="+filetype
              
                docDb.update(docid,{"documentLink":storelink,"status":"Completed"})
                return res.content
                # break
            except Exception as e:
                continue
        # res=requests.post(url=surl,files=file,data=payload)
        docDb.update(docid,{"status":"Failed"})
        return False
       
       
    def uploadFile(payload):
        """
        Handles the upload and processing of files based on their type and specified subcategories.
        Args:
            payload (dict): A dictionary containing the following keys:
                - userId (str): The ID of the user uploading the file.
                - file (object): An object containing the file data, including:
                    - file (file-like object): The actual file content.
                    - filename (str): The name of the file.
                    - size (int): The size of the file in bytes.
                    - content_type (str): The MIME type of the file.
                - categories (list): A list of categories associated with the file.
                - subCategoey (list): A list of subcategories for processing the file.
                - maskImage (optional, object): An object containing mask image data for video masking.
        Returns:
            dict: A dictionary containing the following keys:
                - fileName (str): The name of the processed file.
                - type (str): The MIME type of the file.
                - data (bytes): The base64-encoded content of the processed file.
        Raises:
            Exception: If any error occurs during file processing or API requests.
        Processing Details:
            - Supports video, Excel, and other file types.
            - Handles subcategories such as:
                - CustomMask: Applies masking to videos using a provided mask image.
                - PIIAnonymize: Anonymizes Personally Identifiable Information (PII) in videos.
                - FaceAnonymize: Anonymizes faces in videos.
                - SafetyMasking: Applies safety masking (e.g., NSFW content).
                - NudityMasking: Masks nudity in videos.
            - Updates the document database (docDb) with the processing status.
            - Stores processed files in a specified content type (e.g., "rai-videos", "rai-datasets").
            - Handles file cleanup and ensures proper resource management.
        Note:
            - Environment variables are used for API endpoints (e.g., PRIVACY_FaceVIDEO_IP, SAFETY_NSFW_IP).
            - The function assumes the existence of external dependencies like `docDb`, `DocProcess`, and `requests`.
        """
        
        payload=AttributeDict(payload)
        
        userId=payload.userId
        file=payload.file.file
        fileName=payload.file.filename
        print("filename===",fileName)
        print("size",payload.file.size)
        filetype=payload.file.content_type
        categories=payload.categories
        subCat=payload.subCategoey
        # fileStore="docProcess/fileStore/"
        # if(not os.path.exists(fileStore)):
        #     os.makedirs(fileStore)````
        # with open(fileStore+fileName,'wb') as files:
        #     shutil.copyfileobj(file,files)
            
        # print(filetype)
        # f=open(file,"rb")
        # print(f)
        # return docDb.create(``{"userId":userId,"fileName":fileName,"file":fileStore+fileName,"type":filetype})
        # fileid=fileDb.create({"userId":userId,"fileName":fileName,"file":filereq,"type":filetype})
        # docid=docDb.create({"userId":userId,"fileName":fileName,"fileid":fileid,"type":filetype})
        docid=docDb.create({"userId":userId,"fileName":fileName,"type":filetype,"categories":categories,"subCat":subCat,"status":"Uploaded"})
        response:any=""
        file_content:any=""
        contentType=""
        if docid:
            
            if(filetype=="video/mp4"):
                contentType="rai-videos"
            # print(filereq)
                # for stype in subCat:
                docDb.update(docid,{"status":"Processing"})
                if ("CustomMask" in subCat):
                    maskImage = payload.maskImage.file
                    reqUrl = os.getenv("PRIVACY_FaceVIDEO_IP")+"/rai/v1/video/masking"
                    # reqUrl = "http://localhost:30002/v1/privacy/video/masking"
                    post_files = {
                        "payload":file,
                        "maskImage":maskImage
                    }
                    file_content = file.read()
                    maskImage_content = maskImage.read()
                    
                    
                    
                    # threading.Thread(target=process_video, args=(file_content, maskImage_content,fileName, reqUrl, docid)).start()
                    # return {"status": "Video is being processed. Please check back later."}
          
                    # print("Mask image not provided")
                if("PIIAnonymize" in subCat):
                        reqUrl = os.getenv("PRIVACY_PIIVIDEO_IP")
                        post_files = {
                    #   "payload": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test4.mp4", "rb"),
                        "video":file
                        }
                        payload={
                        "magnification":"False",
                        "rotationFlag":"False",
                        "portfolio":None,
                        "account":None,
                        "exclusionList":""
                        }
                        
                        docDb.update(docid,{"status":"PIIAnonymize Processing"})
                        response = requests.request("POST", reqUrl, data=payload, files=post_files)
                        if(file.closed==False):
                            file.close()
                        if(len(response.content)>0 or response.status_code==200):
                                file_content=base64.b64decode(response.content)
                                # file=tempfile.NamedTemporaryFile(suffix='.mp4')
                                # file.write(file_content)
                                # ff=open(file.name,"wb")
                                with open(fileName, "wb") as f:
                                    f.write(file_content)
                                # shutil.copyfileobj(file_content,ff)
                                file=open(fileName,"rb")
                                print(file)
                        docDb.update(docid,{"status":"PIIAnonymize completed"})
                        
                if("FaceAnonymize" in subCat):
                        reqUrl = os.getenv("PRIVACY_FaceVIDEO_IP")+"/rai/v1/video/anonymize"
                        post_files = {
                    #   "payload": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test4.mp4", "rb"),
                        "payload":file
                        }
                     
                        payload = {"name":fileName.split(".")[0]}
                        docDb.update(docid,{"status":"FaceAnonymize Processing"})
                        response = requests.request("POST", reqUrl, data=payload, files=post_files)
                        print(response)
                        print("file",file.closed)
                        if(file.closed==False):
                            file.close()
                        if(len(response.content)>0 or response.status_code==200):
                            print(type(response.content))
                            file_content=base64.b64encode(response.content).decode('utf-8')
    # return False
                            file_content=base64.b64decode(file_content)
                            # file=tempfile.NamedTemporaryFile(suffix='.mp4')
                            # file.write(file_content)
                            with open(fileName, "wb") as f:
                                    f.write(file_content)
                                    
                            file=open(fileName,"rb")
                        docDb.update(docid,{"status":"FaceAnonymize complete"})
                if("SafetyMasking" in subCat):
                        reqUrl = os.getenv("SAFETY_NSFW_IP")
                        post_files = {
                    #   "payload": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test4.mp4", "rb"),
                        "video":file
                        }
                       
                        docDb.update(docid,{"status":"SafetyMasking Processing"})
                        response = requests.request("POST", reqUrl, files=post_files)
                        if(file.closed==False):
                            file.close()
                        print("Response =====",response)
                        if(len(response.content)>0 or response.status_code==200):
                                # file_content=base64.b64encode(response.content).decode('utf-8')
                                file_content=response.json()["BlurredVideo"]
                                # print(file_content)
                                file_content=base64.b64decode(file_content)
                                with open(fileName, "wb") as f:
                                    f.write(file_content)
                                file=open(fileName,"rb")
                        docDb.update(docid,{"status":"SafetyMasking completed"})
                if("NudityMasking" in subCat):
                        reqUrl = os.getenv("SAFETY_NUDITY_IP")
                        post_files = {
                    #   "payload": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test4.mp4", "rb"),
                        "video":file
                        }
                       
                        docDb.update(docid,{"status":"NudityMasking Processing"})
                        response = requests.request("POST", reqUrl, files=post_files)
                        if(file.closed==False):
                            file.close()
                        print("Response =====",response)
                        if(len(response.content)>0 or response.status_code==200):
                                file_content=base64.b64decode(response.json()["BLURRED"])
                                with open(fileName, "wb") as f:
                                    f.write(file_content)
                                file=open(fileName,"rb")
                        docDb.update(docid,{"status":"NudityMasking completed"})
                res=DocProcess.storeFile(file,contentType,fileName,docid)   
                result={"fileName":fileName,"type":filetype}
                result["data"]=base64.b64encode(response.content)
                file.close()
                print(file.closed)
                while(file.closed==False):
                    file.close()
                    print('file closed',file.closed)
                print(fileName)
                # os.remove(fileName)
                return result
                
                 
            elif(filetype=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                    contentType="rai-datasets"
                    reqUrl = os.getenv("PRIVACY_IP")+"/v1/privacy/excel/anonymize"

                    post_files = {
                      "excel": file
                          
                          }

                    payload = ""

                    response = requests.request("POST", reqUrl, data=payload, files=post_files)
                    if(len(response.content)>0 or response.status_code==200):
                        file_content=response.content
                        file_content=base64.b64encode(file_content).decode('utf-8')
                        file_content=base64.b64decode(file_content)
                    # print(response.content)
                    # with open("a.xlsx","wb") as f:
                    #     f.write(response.content)
                    
                    
                
            else:
                contentType="rai-ppt"
                docDb.update(docid,{"status":"Processing"})
                reqUrl = "http://"
                post_files = {
                #   "payload": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test4.mp4", "rb"),
                  "file":file

                      }
                headersList = {

 "Content-Type": "multipart/form-data;" 
}
                payload ={"exclusionList":payload.exclusionList,"fileName":fileName}
                response = requests.request("POST", reqUrl, data=payload, files=post_files)
                if(response.status_code==200):
                    data=response.text
                    # print(type(x))
                    data=json.loads(data)
                    # print(type(x))

                    file_content=base64.b64decode(data.get("res"))
                    print(file_content)
                    # with open("a1.pptx","wb") as f:
                    #     f.write(file_content)
                
                
            print(response)
            if(response.status_code==200):
                # http://100.78.58.216:8000/api/v1/azureBlob/getBlob?blob_name=piivdo%201_de9fe043-9259-4bc4-97dd-b358336a91b5.mp4&container_name=videostore
                # rf=docDb.fs.new_file(filename=fileName,content_type=filetype)
                # rf.write(file_content)
                print(fileName)
                with open(fileName, "wb") as f:
                            f.write(file_content)
                file_content=open(fileName,"rb")
                res=DocProcess.storeFile(file_content,contentType,fileName,docid)
                print(res)
                # print(type(file_content))
                
                # rf.close()
            else:
                docDb.update(docid,{"status":"Failed"})
                
            result={"fileName":fileName,"type":filetype}
            result["data"]=base64.b64encode(response.content)
            file.close()
            os.remove(fileName)
            return result
            
# import requests

# reqUrl = "http://10.86.104.73:30024/docProcessing/process"

# post_files = {
#   "file": open("c:\WORK\GIT\responsible-ai-admin\responsible-ai-admin\src\rai_admin\temp\test.pptx", "rb"),
# }
# headersList = {
#  "Accept": "*/*",
#  "User-Agent": "Thunder Client (https://www.thunderclient.com)",
#  "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A" 
# }

# payload = "--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"exclusionList\"\r\n\r\nhp\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"

# response = requests.request("POST", reqUrl, data=payload, files=post_files, headers=headersList)

# print(response.text)

            
            
    def getFiles(username,categories):
        
        """
            Retrieve files from the database based on the provided username and categories.
            This function connects to the database, retrieves files associated with the 
            specified username and categories, and processes the files to remove certain 
            fields before returning them.
            Args:
                username (str): The username of the user whose files are to be retrieved.
                categories (list): A list of categories to filter the files.
            Returns:
                list: A list of files matching the specified username and categories, 
                      with certain fields removed.
            """
        
        mydb=DB.connect()
        collist = mydb.list_collection_names()
        print(collist)
        print(username)
        files=docDb.findall({"userId":username,"categories":categories})
        # obj=DocList()
        # print (files)
        for i in files:
            if("resultFileId" in i):
                # res=fileDb.findOne(i["resultFileId"])
        #         # print("------------------------------------------------------------------")
        #         # print("------------------------------------------------------------------")
        #         # print("------------------------------------------------------------------")
        #         print("===",res["data"])
        #         res["data"]=base64.b64encode(res["data"])
                del i["resultFileId"]
        #         i.update(res)
        #     print(res)
            
        # obj.r=files
        
        print(files)
        return files
    
    def getFileContent(docId):
        """
        Retrieves the content of files associated with a given document ID.
        This function queries a database to find all files matching the provided
        document ID. For each file, if it contains a "resultFileId", the corresponding
        file data is fetched, encoded in base64, and added to a list of contents.
        Args:
            docId (float): The ID of the document whose associated files are to be retrieved.
        Returns:
            list: A list of dictionaries, where each dictionary represents a file's
                  data with its content encoded in base64.
        Note:
            - The function assumes the existence of `docDb` and `fileDb` as database
              objects with `findall` and `findOne` methods, respectively.
            - The `docId` is expected to be convertible to a float.
        """
        
        print(docId)
        files=docDb.findall({"docId":float(docId)})
        print(files)
        contentList=[]
        for i in files:
            if("resultFileId" in i):
                res=fileDb.findOne(i["resultFileId"])
                # print("bencdoe",res)
                res["data"]=base64.b64encode(res["data"])
                contentList.append(res)
                
        
        print("contentList",contentList)
        return contentList
    
        
        
    
