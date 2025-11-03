'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024-2025 Infosys Ltd.
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pytest
from src.service.defence import Defence
from src.service.utility import Utility   
from src.service.art import Art
from src.config.urls import UrlLinks
import os
import shutil
import json
from test.service.ModelDataAddition import AddModelData,GetBatchPayloadRequest
from test.service.addModelToMockDatabase import AddModel
from src.dao.ModelDb import Model
from src.dao.DataDb import Data
from src.dao.Batch import Batch
from src.dao.SaveFileDB import FileStoreDb
from src.config.logger import CustomLogger

log = CustomLogger()

class TestDefence:
    @classmethod
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModel.SklearnClasifierTabular()
        AddModel.ScikitlearnClassifierTabular()
        cls.modelDictSklearnClassifierTabular = Model.findall({'ModelName':'SklearnClassifierTabularModel'})[0]
        cls.modelIdSklearnClassifierTabular = cls.modelDictSklearnClassifierTabular['ModelId']
        cls.dataDictSklearnClassifierTabular = Data.findall({'DataSetName':'SklearnClassifierTabularData'})[0]
        cls.dataIdSklearnClassifierTabular = cls.dataDictSklearnClassifierTabular['DataId']
        cls.modelDictScikitlearnClassifierTabular = Model.findall({'ModelName':'ScikitlearnClassifierTabularModel'})[0]
        cls.modelIdScikitlearnClassifierTabular = cls.modelDictScikitlearnClassifierTabular['ModelId']
        cls.dataDictScikitlearnClassifierTabular = Data.findall({'DataSetName':'ScikitlearnClassifierTabularData'})[0]
        cls.dataIdScikitlearnClassifierTabular = cls.dataDictScikitlearnClassifierTabular['DataId']



    def databasePath():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestDefence.databasePath()
        report_path = new_path + "/database/report"
        cache_path = new_path + "/database/cacheMemory"
        data_path = new_path + "/database/data"
        model_path = new_path + "/database/model"
        payload_path = new_path + "/database/payload"
        if os.path.exists(report_path):
            shutil.rmtree(report_path) 
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path) 
        if os.path.exists(data_path):
            shutil.rmtree(data_path) 
        if os.path.exists(model_path):
            shutil.rmtree(model_path) 
        if os.path.exists(payload_path):
            shutil.rmtree(payload_path) 


    def getBatchId(modelId,dataId,attackList):
        payload = GetBatchPayloadRequest(
            userId ='admin',
            modelId = modelId,
            dataId = dataId,
            tenetName = ['Security'],
            appAttacks = attackList
        )
        batchdoc = AddModelData.getBatchList(payload)
        batchid = batchdoc[0]['BatchId']
        return batchid


    def getPayload(payload):
        raw_data, data_path = Utility.readDataFile(payload)
        payload_path = Utility.readPayloadFile(payload)
        return data_path,payload_path

    def getDefenseModel(data_path,payload_path,payload):
        Defence.generateDenfenseModel(payload)
        if os.path.exists(data_path):
            os.remove(data_path)
        if os.path.exists(payload_path):
            os.remove(payload_path)


    def getDefenseEndPointModel(data_path,payload_path,payload):
        Defence.generateDenfenseModelendpoint(payload)
        if os.path.exists(data_path):
            os.remove(data_path)
        if os.path.exists(payload_path):
            os.remove(payload_path)


    def pathFinder(payload):
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        root_path = new_path + "/database"
        report_path = os.path.join(root_path+"/report",payload)
        pickle_path = os.path.join(report_path,"DefenseModel.pkl")
        return pickle_path


    def test_generateDenfenseModel_sklearnclassifiertabularattack(self):
        TestDefence.reportDeletion()
        attackName_sklearnclassifiertabular = 'ProjectedGradientDescentTabular'
        batchId = TestDefence.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName_sklearnclassifiertabular])
        Art.ProjectedGradientDescentZoo(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName_sklearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_sklearnclassifiertabular = {'modelName':'SklearnClassifierTabularModel','folderName':k,'dataFileName':os.path.basename(data_path).split('.')[0]}
        TestDefence.getDefenseModel(data_path,payload_path,payload_sklearnclassifiertabular)
        value = TestDefence.pathFinder(k)
        assert os.path.exists(value) 


    def test_generateDenfenseModel_scikitlearnclassifiertabular(self):
        TestDefence.reportDeletion()
        attackName_scikitlearnclassifiertabular = 'MembershipInferenceRule'
        batchId = TestDefence.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName_scikitlearnclassifiertabular])
        Art.MembershipInferenceRule(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName_scikitlearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_scikitlearnclassifiertabular = {'modelName':'ScikitlearnClassifierTabularModel','folderName':k,'dataFileName':os.path.basename(data_path).split('.')[0]}
        TestDefence.getDefenseModel(data_path,payload_path,payload_scikitlearnclassifiertabular)
        value = TestDefence.pathFinder(k)
        assert os.path.exists(value) 


    def test_generateDenfenseModel_sklearnclassifiertabularattack_id_None(self):
        TestDefence.reportDeletion()
        attackName_sklearnclassifiertabular = 'ProjectedGradientDescentTabular'
        batchId = TestDefence.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName_sklearnclassifiertabular])
        Art.ProjectedGradientDescentZoo(batchId)
        id = None
        k = f'{attackName_sklearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_sklearnclassifiertabular = {'modelName':'SklearnClassifierTabularModel','folderName':k,'dataFileName':os.path.basename(data_path).split('.')[0]}
        with pytest.raises(Exception):  
            TestDefence.getDefenseModel(data_path,payload_path,payload_sklearnclassifiertabular)


    def test_generateDenfenseModel_scikitlearnclassifiertabular_id_None(self):
        TestDefence.reportDeletion()
        attackName_scikitlearnclassifiertabular = 'MembershipInferenceRule'
        batchId = TestDefence.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName_scikitlearnclassifiertabular])
        Art.MembershipInferenceRule(batchId)
        id = None
        k = f'{attackName_scikitlearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_scikitlearnclassifiertabular = {'modelName':'ScikitlearnClassifierTabularModel','folderName':k,'dataFileName':os.path.basename(data_path).split('.')[0]}
        with pytest.raises(Exception): 
            TestDefence.getDefenseModel(data_path,payload_path,payload_scikitlearnclassifiertabular)  


    def test_generateDenfenseModelendpoint_sklearnclassifiertabularattack(self):
        TestDefence.reportDeletion()
        attackName_sklearnclassifiertabular = 'ProjectedGradientDescentTabular'
        batchId = TestDefence.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName_sklearnclassifiertabular])
        Art.ProjectedGradientDescentZoo(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName_sklearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_sklearnclassifiertabular = {'modelName':'SklearnClassifierTabularModel','folderName':k}
        TestDefence.getDefenseEndPointModel(data_path,payload_path,payload_sklearnclassifiertabular)
        value = TestDefence.pathFinder(k)
        assert os.path.exists(value)   


    def test_generateDenfenseModelendpoint_sklearnclassifiertabularattack_id_None(self):
        TestDefence.reportDeletion()
        attackName_sklearnclassifiertabular = 'ProjectedGradientDescentTabular'
        batchId = TestDefence.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName_sklearnclassifiertabular])
        Art.ProjectedGradientDescentZoo(batchId)
        id = None
        k = f'{attackName_sklearnclassifiertabular}_{id}'
        data_path,payload_path = TestDefence.getPayload(batchId)
        payload_sklearnclassifiertabular = {'modelName':'SklearnClassifierTabularModel','folderName':k}
        with pytest.raises(Exception):  
            TestDefence.getDefenseEndPointModel(data_path,payload_path,payload_sklearnclassifiertabular)  

    def getPayloadofgenerateCombinedDenfenseModel(payload):
        root_path = Utility.getcurrentDirectory() + "/database"
        dirList = ["data","model","payload","report"]
        for dir in dirList:
            dirs = root_path + "/" + dir
            if not os.path.exists(dirs):
                os.mkdir(dirs)
        batchList = Batch.findall({'BatchId':payload['batchid']})[0]
        modelList = Model.findall({'ModelId':batchList['ModelId']})[0]
        dataList = Data.findall({'DataId':batchList['DataId']})[0]
        modelName = modelList['ModelName']
        modelid = modelList['ModelId']
        modelendPoint = modelList['ModelEndPoint']
        foldername = f'{modelName}'
        report_path = root_path + "/report"
        report_path = os.path.join(report_path,foldername)
        if os.path.isdir(report_path):    
            if os.path.isfile(report_path) or os.path.islink(report_path):
                os.remove(report_path) 
            elif os.path.isdir(report_path):
                shutil.rmtree(report_path) 
        os.mkdir(report_path)
        data_path = Utility.getcurrentDirectory() + "/database/data"
        dataFile = FileStoreDb.fs.get(dataList['SampleData'])
        dataF = dataFile.read()
        # if(Utility.isContentSafe({"Filename" : modelName})):
        #     data_path = os.path.join(data_path,modelName+'.csv')
        # else:
        #     log.info("Suspicious Data Involved in ModelName")
        #     return "Suspicious Data Involved in ModelName"
        
        SAFE_DIR = data_path
        def open_safe_file(filename):
            if '..' in filename or '/' in filename:
                raise ValueError("Invalid filename")
            data_path = os.path.join(SAFE_DIR, filename)
            return open(os.path.join(SAFE_DIR, filename),"w",newline="")
        with open_safe_file(modelName+'.csv') as f:
            f.write(dataF)
        Payload_path = Utility.readPayloadFile(batchList['BatchId'])
        payload_folder_path = Utility.getcurrentDirectory() + "/database/payload"
        payload_path = os.path.join(payload_folder_path,modelName + ".txt")
        with open(f'{payload_path}') as f:
            data = f.read()
        payload_data = json.loads(data)
        payload_data["modelEndPoint"] = modelendPoint
        count = Utility.combineReportFile({'batchid':payload['batchid'],'modelName':modelName,'report_path':report_path,'attackList':payload['attackList']})
        if payload_data['targetDataType'] != 'Image':
            originaldataContent = FileStoreDb.findOne(dataList['SampleData'])
            dataFileType = originaldataContent["fileName"].split('.')[-1]
            original_data_path = os.path.join(report_path,modelName+'.'+dataFileType) 
            if os.path.exists(original_data_path):                          
                os.remove(original_data_path)                                       
            with open(original_data_path, 'wb') as f:
                f.write(originaldataContent["data"])
        return payload_data,report_path,modelName


    def test_generateCombinedDenfenseModel(self):
        attackName_sklearnclassifiertabular = 'ProjectedGradientDescentTabular'
        batchId = TestDefence.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName_sklearnclassifiertabular])
        defencePayload = {'batchid':batchId,'attackList':[attackName_sklearnclassifiertabular]}
        payload_data,report_path,modelName = TestDefence.getPayloadofgenerateCombinedDenfenseModel(defencePayload)
        payload = {'payloadData':payload_data, 'report_path':report_path, 'modelName':modelName}
        Defence.generateCombinedDenfenseModel(payload)
        value = TestDefence.pathFinder(report_path)
        assert os.path.exists(value) 

