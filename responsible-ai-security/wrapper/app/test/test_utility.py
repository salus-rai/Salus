'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024-2025 Infosys Ltd.
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from test.service.addModelToMockDatabase import AddModel
from test.service.ModelDataAddition import AddModelData,GetBatchPayloadRequest
from src.dao.ModelDb import Model
from src.dao.DataDb import Data
from src.config.urls import UrlLinks
from sklearn.datasets import load_iris
import datetime,time
from art.estimators.classification import SklearnClassifier
from art.attacks.poisoning.poisoning_attack_svm import PoisoningAttackSVM
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from src.service.defence import Defence
from art.attacks.evasion import ZooAttack
from art.attacks.inference.membership_inference import MembershipInferenceBlackBoxRuleBased
from art.estimators.classification.scikitlearn import SklearnAPIClassifier
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import requests
import json
import pandas as pd
import csv
import pytest
from src.service.utility import Utility
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from src.service.service import Infosys,Bulk,AttributeDict
from src.dao.Security.SecReportDb import SecReport
from src.dao.Batch import Batch
from src.dao.SaveFileDB import FileStoreDb
from src.dao.Batch import Batch
from src.dao.ModelAttributesValuesDb import ModelAttributesValues
from src.dao.ModelAttributesDb import ModelAttributes
from src.config.logger import CustomLogger

log = CustomLogger()

class TestUtility:
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModelData.loadApi()
        AddModel.SklearnClasifierTabular()
        AddModel.ScikitlearnClassifierTabular()
        AddModel.SklearnAPIClassifierTabular()
        cls.modelDictSklearnClassifierTabular = Model.findall({'ModelName':'SklearnClassifierTabularModel'})[0]
        cls.modelIdSklearnClassifierTabular = cls.modelDictSklearnClassifierTabular['ModelId']
        cls.dataDictSklearnClassifierTabular = Data.findall({'DataSetName':'SklearnClassifierTabularData'})[0]
        cls.dataIdSklearnClassifierTabular = cls.dataDictSklearnClassifierTabular['DataId']
        cls.modelDictScikitlearnClassifierTabular = Model.findall({'ModelName':'ScikitlearnClassifierTabularModel'})[0]
        cls.modelIdScikitlearnClassifierTabular = cls.modelDictScikitlearnClassifierTabular['ModelId']
        cls.dataDictScikitlearnClassifierTabular = Data.findall({'DataSetName':'ScikitlearnClassifierTabularData'})[0]
        cls.dataIdScikitlearnClassifierTabular = cls.dataDictScikitlearnClassifierTabular['DataId']
        cls.modelDictSklearnAPIClassifierTabular = Model.findall({'ModelName':'SklearnAPIClassifierTabularModel'})[0]
        cls.modelIdSklearnAPIClassifierTabular = cls.modelDictSklearnAPIClassifierTabular['ModelId']
        cls.dataDictSklearnAPIClassifierTabular = Data.findall({'DataSetName':'SklearnAPIClassifierTabularData'})[0]
        cls.dataIdSklearnAPIClassifierTabular = cls.dataDictSklearnAPIClassifierTabular['DataId']


    def databasePath():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestUtility.databasePath()
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

    def pathFinder():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        root_path = new_path + "/database"
        return root_path  

    def createReportFolder(batchId):
        root_path = os.getcwd()
        root_path = Utility.getcurrentDirectory() + "/database"
        dirList = ["data","model","payload","report"]
        for dir in dirList:
            dirs = root_path + "/" + dir
            if not os.path.exists(dirs):
                os.mkdir(dirs)
        batchList = Batch.findall({'BatchId':batchId})[0]
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
        SAFE_DIR = data_path
        def open_safe_file(filename):
            if '..' in filename or '/' in filename:
                raise ValueError("Invalid filename")
            data_path = os.path.join(SAFE_DIR, filename)
            return open(os.path.join(SAFE_DIR, filename),"wb",newline="")
        data_path = os.path.join(data_path,modelName+'.csv')                                     
        with open_safe_file(modelName+'.csv') as f:
            f.write(dataF)
        Payload_path = Utility.readPayloadFile(batchList['BatchId'])
        payload_folder_path = Utility.getcurrentDirectory() + "/database/payload"
        payload_path = os.path.join(payload_folder_path,modelName + ".txt")
        with open(f'{payload_path}') as f:
            data = f.read()
        payload_data = json.loads(data)
        payload_data["modelEndPoint"] = modelendPoint
        return report_path,payload_data,dataList


    def get_data():
        iris = load_iris()
        X = iris.data
        y = iris.target
        X = X[y != 0, :2]
        y = y[y != 0]
        labels = np.zeros((y.shape[0], 2))
        labels[y == 2] = np.array([1, 0])
        labels[y == 1] = np.array([0, 1])
        y = labels
        n_sample = len(X)
        order = np.random.permutation(n_sample)
        X = X[order]
        y = y[order].astype(np.float32)
        X_train = X[:int(.9 * n_sample)]
        y_train = y[:int(.9 * n_sample)]  
        return X_train,y_train 

    def find_dup(x_train):
        dup = np.zeros(x_train.shape[0])
        for idx, x in enumerate(x_train):
            dup[idx] = np.isin(x_train[:idx], x).all(axis=1).any()  
        return dup 

    def generate_latest_report(self,attack):
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attack])
        Payload = {"batchId":batchId, "modelUrl":attack}
        batchid = Bulk.batchAttack(Payload)
        return batchId

    def generateDefenceModel(self,attack):
        batchId = TestUtility.generate_latest_report(self,attack)
        report_path,payload_data,dataList = TestUtility.createReportFolder(batchId)
        payload = {'batchid':batchId,'modelName':'SklearnClassifierTabularModel','report_path':report_path,'attackList':[attack]}
        Utility.combineReportFile(payload)
        if payload_data['targetDataType'] != 'Image':
            originaldataContent = FileStoreDb.findOne(dataList['SampleData'])
            dataFileType = originaldataContent["fileName"].split('.')[-1]
            original_data_path = os.path.join(report_path,'SklearnClassifierTabularModel'+'.'+dataFileType) 
            if os.path.exists(original_data_path):                          
                os.remove(original_data_path)                                       
            with open(original_data_path, 'wb') as f:
                f.write(originaldataContent["data"])
            Defence.generateCombinedDenfenseModel({'payloadData':payload_data, 'report_path':report_path, 'modelName':'SklearnClassifierTabularModel'})
            Utility.databaseDelete(original_data_path)  
        return report_path,payload_data 

    def getMakeAttackListRow(attack,defence,type,attackName):
        rows = f"""
                <tr>
                    <td>{type}</td>
                    <td>{attackName}</td>
                    <td><span class="selected-attack">✔</span></td>
                    <td>
                        <div class="attack-accuracy">
                            <div class="attack-accuracy-value">{attack:.2f}%</div>
                            <div class="attack-accuracy-bar">
                                <div class="attack-accuracy-bar-fill" style="width: {attack}%;"></div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="detection-accuracy">
                            <div class="detection-accuracy-value">{defence:.2f}%</div>
                            <div class="detection-accuracy-bar">
                                <div class="detection-accuracy-bar-fill" style="width: {defence}%;"></div>
                            </div>
                        </div>
                    </td>
                </tr>
            """
        return rows

    def find_calc_precision_recall(predicted, actual, positive_value=1):
        score = 0  
        num_positive_predicted = 0  
        num_positive_actual = 0 
        for i in range(len(predicted)):
            if predicted[i] == positive_value:
                num_positive_predicted += 1
            if actual[i] == positive_value:
                num_positive_actual += 1
            if predicted[i] == actual[i]:
                if predicted[i] == positive_value:
                    score += 1
        if num_positive_predicted == 0:
            precision = 1
        else:
            precision = score / num_positive_predicted 
        if num_positive_actual == 0:
            recall = 1
        else:
            recall = score / num_positive_actual

        return precision, recall 

    def getEvasionPayloadforGraphForAttack(payload):
        raw_data,model,list_of_column_names,Output_column = TestUtility.getModelDataFromDatabase(payload)
        art_svm_classifier = SklearnClassifier(model=model)
        zoo = ZooAttack(classifier=art_svm_classifier, confidence=0.0, targeted=False, learning_rate=1e-1, max_iter=20,
                        binary_search_steps=10, initial_const=1e-3, abort_early=True, use_resize=False, 
                        use_importance=False, nb_parallel=1, batch_size=1, variable_h=0.2)
        X_train = raw_data.drop([Output_column], axis=1).to_numpy()
        Y_train = raw_data[[Output_column]].to_numpy()
        list_of_column_names.remove(Output_column)
        zoo_x_train_adv = zoo.generate(X_train)
        bscore = model.score(X_train, Y_train)
        bprediction = model.predict([X_train[0]])
        ascore = model.score(zoo_x_train_adv, Y_train)
        aprediction = model.predict([zoo_x_train_adv[0]])
        perturbation = np.mean(np.abs((zoo_x_train_adv - X_train)))
        attack_data_list,attack_data_status = Utility.combineList({'attack_data':zoo_x_train_adv,'target_data':Y_train,'prediction_data':model.predict(zoo_x_train_adv),'adversial_score':ascore,'perturbation':perturbation,'type':'Evasion'})
        list_of_column_names.extend([Output_column, 'prediction', 'result'])
        return list_of_column_names,attack_data_list

    def createFolderForgraphForAttack(list_of_column_names,attack_data_list,attackName):
        root_path = os.getcwd()
        root_path = Utility.getcurrentDirectory() + "/database"
        dirList = ["data","model","payload","report"]
        for dir in dirList:
            dirs = root_path + "/" + dir
            if not os.path.exists(dirs):
                os.mkdir(dirs)
        Current_Report_ID = UrlLinks.Current_ID + 1
        foldername = f'{attackName}_{Current_Report_ID}'
        csvfilename = 'Attack_Samples.csv'
        root_path = root_path + "/report"
        report_path = os.path.join(root_path,foldername)
        if os.path.isdir(report_path):   
            shutil.rmtree(report_path)
        os.mkdir(report_path)
        payload_folder_path = Utility.getcurrentDirectory() + "/database/payload"
        payload_path = os.path.join(payload_folder_path,'SklearnClassifierTabularModel' + ".txt")
        with open(f'{payload_path}') as f:
            data = f.read()
        data = json.loads(data)
        with open(os.path.join(report_path,csvfilename), 'w',newline="") as f:
            write = csv.writer(f)
            write.writerow(list_of_column_names)
            write.writerows(attack_data_list)  
        return report_path,data 

    def getPayloadforcreateArtEstimator(payload):
        raw_data,list_of_column_names,Output_column,data = TestUtility.getModelDataFromDatabase(payload)
        X = raw_data.drop([Output_column], axis=1, inplace=False).to_numpy()
        y = raw_data[[Output_column]].to_numpy()
        list_of_column_names.remove(Output_column)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, train_size=0.80,random_state=32)
        Payload = {
            'modelEndPoint':data['modelEndPoint'],
            'nb_classes':len(data['groundTruthClassNames']),
            'input_shape':(len(list_of_column_names),),
            'api_data_variable':data['data'],
            'api_response_variable':data['prediction']
        }
        return Payload,data,X_train

    def getcreateArtEstimator(payload):
        sklearn_api_estimator = SklearnAPIClassifier(api=payload['modelEndPoint'],
                                nb_classes = payload['nb_classes'],
                                input_shape = payload['input_shape'],
                                api_data_variable = payload['api_data_variable'],
                                api_response_variable = payload['api_response_variable']
                            )
        return sklearn_api_estimator


    def getModelDataFromDatabase(payload):
        raw_data, data_path = Utility.readDataFile(payload)
        modelId = Batch.findall({'BatchId':payload})[0]['ModelId']
        attributeValues = ModelAttributesValues.findall({"ModelId":modelId})
        for value in attributeValues:
            attributes = ModelAttributes.findall({"ModelAttributeId":value.ModelAttributeId})[0]['ModelAttributeName']
            if attributes == 'useModelApi':
                aatributesValue = value.ModelAttributeValues
        if aatributesValue == 'No':
            model, model_path, modelName = Utility.readModelFile(payload)
        else:
            modelName = Utility.readModelFile(payload)    
        Payload_path = Utility.readPayloadFile(payload)
        list_of_column_names = list(raw_data.columns)
        payload_folder_path = TestUtility.pathFinder() + "/payload"
        payload_path = os.path.join(payload_folder_path,modelName + ".txt")
        with open(f'{payload_path}') as f:
            data = f.read()
        data = json.loads(data)
        Output_column = data["groundTruthClassLabel"]
        if aatributesValue == 'No':
            return raw_data,model,list_of_column_names,Output_column 
        else:
            return raw_data,list_of_column_names,Output_column,data 

    def getEvasionPayloadforGraphForAttack(payload):
        raw_data,model,list_of_column_names,Output_column = TestUtility.getModelDataFromDatabase(payload)
        art_svm_classifier = SklearnClassifier(model=model)
        zoo = ZooAttack(classifier=art_svm_classifier, confidence=0.0, targeted=False, learning_rate=1e-1, max_iter=20,
                        binary_search_steps=10, initial_const=1e-3, abort_early=True, use_resize=False, 
                        use_importance=False, nb_parallel=1, batch_size=1, variable_h=0.2)
        X_train = raw_data.drop([Output_column], axis=1).to_numpy()
        Y_train = raw_data[[Output_column]].to_numpy()
        list_of_column_names.remove(Output_column)
        zoo_x_train_adv = zoo.generate(X_train)
        bscore = model.score(X_train, Y_train)
        bprediction = model.predict([X_train[0]])
        ascore = model.score(zoo_x_train_adv, Y_train)
        aprediction = model.predict([zoo_x_train_adv[0]])
        perturbation = np.mean(np.abs((zoo_x_train_adv - X_train)))
        attack_data_list,attack_data_status = Utility.combineList({'attack_data':zoo_x_train_adv,'target_data':Y_train,'prediction_data':model.predict(zoo_x_train_adv),'adversial_score':ascore,'perturbation':perturbation,'type':'Evasion'})
        list_of_column_names.extend([Output_column, 'prediction', 'result'])
        return list_of_column_names,attack_data_list

    def test_find_duplicates(self):
        x_train, y_train = TestUtility.get_data()
        expectedOutput = TestUtility.find_dup(x_train)
        value = Utility.find_duplicates(x_train) 
        assert np.all(value == expectedOutput)

    def test_calc_precision_recall(self):
        element1 = np.ones(100)
        element2 = np.where(np.arange(125) < 100, 1.0, 0.0)
        expectedPrecision,expectedRecall = TestUtility.find_calc_precision_recall(element1,element2)
        precision,recall = Utility.calc_precision_recall(element1,element2)
        assert precision == expectedPrecision
        assert recall == expectedRecall

    def test_get_adversarial_examples(self):
        x_train, y_train = TestUtility.get_data()
        x_val = x_train[-10:]
        y_val = y_train[-10:]
        kernel = 'linear'
        attack_idx = 0
        response1, response2 = Utility.get_adversarial_examples(x_train,y_train,0,x_val,y_val,'linear')
        art_classifier = SklearnClassifier(model=SVC(kernel=kernel), clip_values=(0, 10))
        art_classifier.fit(x_train, y_train)
        init_attack = np.copy(x_train[attack_idx])
        y_attack = np.array([1, 1]) - np.copy(y_train[attack_idx])
        attack = PoisoningAttackSVM(art_classifier, 0.0001, 1.0, x_train, y_train, x_val, y_val, max_iter=50)
        final_attack, _ = attack.poison(np.array([init_attack]), y=np.array([y_attack]))
        assert len(response1) == len(final_attack)
        assert response1.shape == final_attack.shape

    def test_readModelFile(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        model_data:any
        model_data, model_path, modelName = Utility.readModelFile(batchId)
        root_path = TestUtility.pathFinder()
        expected_model_path = root_path + "/model"
        expected_model_path = os.path.join(expected_model_path,'SklearnClassifierTabularModel.pkl')
        assert modelName == 'SklearnClassifierTabularModel'
        assert os.path.exists(model_path)
        assert model_path == expected_model_path
        if os.path.exists(model_path):
            os.remove(model_path)

    def test_readModelFile_None(self):
        with pytest.raises(Exception): 
            Utility.readModelFile(None)

    def test_readDataFile(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        raw_data:any
        raw_data, data_path = Utility.readDataFile(batchId)
        root_path = TestUtility.pathFinder()
        expected_data_path = root_path + "/data"
        expected_data_path = os.path.join(expected_data_path,'SklearnClassifierTabularModel.csv')
        assert os.path.exists(data_path)
        assert data_path == expected_data_path
        if os.path.exists(data_path):
            os.remove(data_path)  

    def test_readDataFile_None(self):  
        with pytest.raises(Exception): 
            Utility.readDataFile(None)  

    def test_readPayloadFile(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload_path = Utility.readPayloadFile(batchId)
        root_path = TestUtility.pathFinder()
        expected_payload_path = root_path + "/payload"
        expected_payload_path = os.path.join(expected_payload_path,'SklearnClassifierTabularModel.txt') 
        assert os.path.exists(payload_path)
        assert payload_path == expected_payload_path
        if os.path.exists(payload_path):
            os.remove(payload_path)  

    def test_readPayloadFile_None(self):  
        with pytest.raises(Exception): 
            Utility.readPayloadFile(None)  

    def test_updateCurrentID(self):
        id = UrlLinks.Current_ID
        Utility.updateCurrentID()
        expected_id = id + 2
        assert UrlLinks.Current_ID ==  expected_id    

    def test_dateTimeFormat(self):
        k = datetime.datetime.now() 
        expected_format_date = k.strftime("%d-%m-%Y %I:%M:%S %p")
        assert Utility.dateTimeFormat(k) == expected_format_date

    def test_sortReportsList(self):
        payload =[
                {
                    "_id": 1716645749.612299,
                    "id": 1716645749.612299,
                    "SecReportCombineId": 1716645749.612299,
                    "SecBatchDtlId": 1711716334.3387322,
                    "ModelId": 1711716334.075861,
                    "ReportName": "Sklearn_Iris_Model.zip",
                    "CreatedDateTime": "2024-05-25T14:02:28.220000",
                    "LastUpdatedDateTime": "2024-05-25T14:02:28.220000"
                },
                {
                    "_id": 1716125007.4068437,
                    "id": 1716125007.4068437,
                    "SecReportCombineId": 1716125007.4068437,
                    "SecBatchDtlId": 1711716334.3387322,
                    "ModelId": 1711716334.075861,
                    "ReportName": "Sklearn_Iris_Model.zip",
                    "CreatedDateTime": "2024-05-19T13:23:16.371000",
                    "LastUpdatedDateTime": "2024-05-19T13:23:16.371000"
        }]
        value = Utility.sortReportsList(payload)
        expectedOutput = sorted(payload, key=lambda x:x['CreatedDateTime'], reverse=True)
        assert value == expectedOutput

    def test_combineList(self):
        x_train, y_train = TestUtility.get_data()
        payload = {'attack_data':x_train,'target_data':y_train,'prediction_data':y_train[-1],'type':'Inference'}
        a = x_train.tolist()
        b = y_train.tolist()
        c = [x + y for x,y in zip(a,b)]
        d = y_train[-1].tolist()
        e = [x + [y] for x,y in zip(c,d)]
        f = []
        for i in range(len(e)):
            if e[i][-1] == e[i][-2]:
                f.append([(i+2),e[i][-2],e[i][-1],'True'])
                e[i].append('True')
            else:
                e[i].append('False')
        result1,result2 = Utility.combineList(payload)
        assert result1 == e
        assert result2 == f

    def test_attackDesc(self):
        value = Utility.attackDesc("MembershipInferenceRule")
        expectedOutput = "\n                        Implementation of a simple, rule-based black-box membership inference attack. \n                        This implementation uses the simple rule: if the model's prediction for a \n                        sample is correct, then it is a member. Otherwise, it is not a member.\n                    "
        assert value == expectedOutput

    def test_attackDesc_None(self):
        value = Utility.attackDesc(None)
        assert len(value) == 0


    def test_updateReportsList(self):
        attack = ['ZerothOrderOptimization']
        batchId = TestUtility.generate_latest_report(self,attack[0])
        reportList = SecReport.findall({"BatchId":batchId})
        payload = {'reportList':reportList, 'modelName':'SklearnClassifierTabularModel','attackList':attack}
        value = Utility.updateReportsList(payload)
        latestDict = {}
        for d in payload['reportList']:
            name = d['ReportName'].split('.')[0]
            if name in payload['attackList']:
                if name in latestDict:
                    if d['CreatedDateTime'] > latestDict[name]['CreatedDateTime']:
                        latestDict[name] = d
                else:
                    latestDict[name] = d
        expectedOutput = list(latestDict.values())
        assert value == expectedOutput


    def test_updateReportsList_None(self):
        payload = {'reportList':None, 'modelName':'SklearnClassifierTabularModel','attackList':['ZerothOrderOptimization']}
        with pytest.raises(Exception): 
            Utility.updateReportsList(payload) 

    def test_combineReportFile(self):
        attack = ['ZerothOrderOptimization']
        batchId = TestUtility.generate_latest_report(self,attack[0])
        report_path,payload_data,dataList = TestUtility.createReportFolder(batchId)
        payload = {'batchid':batchId,'modelName':'SklearnClassifierTabularModel','report_path':report_path,'attackList':attack}
        response = Utility.combineReportFile(payload)
        root_path = TestUtility.pathFinder()
        report_path = root_path + "/report"
        Utility.databaseDelete(report_path)
        assert response == 1

    def test_combineReportFile_None(self):
        attack = ['ZerothOrderOptimization']
        batchId = TestUtility.generate_latest_report(self,attack[0])
        report_path,payload_data,dataList = TestUtility.createReportFolder(batchId)
        payload = {'batchid':None,'modelName':'SklearnClassifierTabularModel','report_path':report_path,'attackList':attack}
        response = Utility.combineReportFile(payload)   
        assert response == 0 

    def test_checkAttackListStatus1(self):
        attack = ['ZerothOrderOptimization']
        report_path,payload_data = TestUtility.generateDefenceModel(self,attack[0])
        expectedstatusList = []
        expecteddefenceList = []
        for filename in os.listdir(report_path):
            if filename.endswith('.csv'):
                csv_path = os.path.join(report_path, filename)
                df = pd.read_csv(csv_path)
                col = df[df[df.columns[-1]] == True][df.columns[-1]].value_counts().tolist()
                if len(col) > 0:
                    value = (col[0] / df.shape[0]) * 100
                    score = Utility.generateDefenceAccuracy1({'modelName':'SklearnClassifierTabularModel', 'csv_path':csv_path, 'folder_path':report_path})
                    expectedstatusList.append({filename.split('.')[0]:value})
                    expecteddefenceList.append({filename.split('.')[0]:(score*100)})
                else:
                    expectedstatusList.append({filename.split('.')[0]:0.0})
                    expecteddefenceList.append({filename.split('.')[0]:0.0})
        statusList,defenceList = Utility.checkAttackListStatus1({'folder_path':report_path,'modelName':'SklearnClassifierTabularModel'}) 
        root_path = TestUtility.pathFinder()
        report_path = root_path + "/report"
        if os.path.isdir(report_path):    
            shutil.rmtree(report_path)      
        assert statusList == expectedstatusList
        assert defenceList == expecteddefenceList

    def test_makeAttackListRow_InferenceAttack(self):
        TestUtility.reportDeletion()
        attack = ['MembershipInferenceRule']
        report_path,payload_data = TestUtility.generateDefenceModel(self,attack[0])
        total_attacks = Infosys.getAttackFuncs({'targetClassifier':'SklearnClassifier','targetDataType':'Tabular'})
        statusList = [{'MembershipInferenceRule': 53.73134}]
        defenceList = [{'MembershipInferenceRule': 33.33333}]
        rows, attack_list = Utility.makeAttackListRow({'total_attacks':total_attacks,'attackList':attack, 'statusList':statusList,'defenceList':defenceList})
        root_path = TestUtility.pathFinder()
        report_path = root_path + "/report"
        if os.path.isdir(report_path):    
            shutil.rmtree(report_path)  
        expectedAttackList = [{'name': 'MembershipInferenceRule', 'type': 'Inference'}]
        assert attack_list == expectedAttackList
        assert rows == TestUtility.getMakeAttackListRow(53.73134,33.33333,'Inference','MembershipInferenceRule')

    def test_makeAttackListRow_EvasionAttack(self):
        attack = ['ZerothOrderOptimization']
        report_path,payload_data = TestUtility.generateDefenceModel(self,attack[0])
        total_attacks = Infosys.getAttackFuncs({'targetClassifier':'SklearnClassifier','targetDataType':'Tabular'})
        statusList = [{'ZerothOrderOptimization': 53.73134}]
        defenceList = [{'ZerothOrderOptimization': 33.33333}]
        rows, attack_list = Utility.makeAttackListRow({'total_attacks':total_attacks,'attackList':attack, 'statusList':statusList,'defenceList':defenceList})
        success_skipped_list = [len(total_attacks), 1, (len(total_attacks)-1)]
        report_datetime = datetime.datetime.now()
        Utility.graphForCombineAttack({'folder_path':report_path, 'modelName':'SklearnClassifierTabularModel', 'model_metaData':payload_data, 'reportTime':report_datetime, 'success_skipped':success_skipped_list, 'target':payload_data['groundTruthClassLabel'], 'rows':rows, 'attack_list':attack_list})
        Utility.htmlToPdfWithWatermark({'folder_path':report_path})
        Utility.createAttackFolder({'report_path':report_path, 'attack_list':attack_list})
        root_path = TestUtility.pathFinder()
        report_path = root_path + "/report"
        if os.path.isdir(report_path):    
            shutil.rmtree(report_path) 
        expectedAttackList = [{'name': 'ZerothOrderOptimization', 'type': 'Evasion'}]  
        assert rows == TestUtility.getMakeAttackListRow(53.73134,33.33333,'Evasion','ZerothOrderOptimization')   
        assert attack_list == expectedAttackList  

    def test_getcurrentDirectory(self):
        expected_path = TestUtility.pathFinder()
        value = Utility.getcurrentDirectory()
        value = value + "/database"
        assert value == expected_path

    def test_graphForAttack_EvasionAttack(self):
        attackName = 'ZerothOrderOptimization'
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        list_of_column_names,attack_data_list = TestUtility.getEvasionPayloadforGraphForAttack(batchId)
        report_path,data = TestUtility.createFolderForgraphForAttack(list_of_column_names,attack_data_list,attackName)
        payload = {'folder_path':report_path, 'target':data['groundTruthClassLabel'], 'attackName':attackName}  
        result = Utility.graphForAttack(payload) 
        assert result.startswith("<div class='graph-container-attack'>")
        assert result.endswith("' alt='Attack Graph' class='graph-image'></div>")

    def test_graphForAttack_InferenceAttack(self):
        TestUtility.reportDeletion()
        attackName = 'MembershipInferenceRule'
        batchId = TestUtility.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        list_of_column_names,attack_data_list = TestUtility.getEvasionPayloadforGraphForAttack(batchId)
        report_path,data = TestUtility.createFolderForgraphForAttack(list_of_column_names,attack_data_list,attackName)
        payload = {'folder_path':report_path, 'target':data['groundTruthClassLabel'], 'attackName':attackName}  
        result = Utility.graphForAttack(payload) 
        assert result.startswith("<div class='graph-container-attack'>")
        assert result.endswith("' alt='Attack Graph' class='graph-image'></div>")


    def test_createArtEstimator(self):
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestUtility.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload,data,X_train = TestUtility.getPayloadforcreateArtEstimator(batchId)
        expectedOutput = TestUtility.getcreateArtEstimator(payload)
        result = Utility.createArtEstimator(payload)
        assert type(result) == type(result)


    def test_getPredictionsFromEndpoint_batchtrue(self):
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestUtility.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload,data,X_train = TestUtility.getPayloadforcreateArtEstimator(batchId)
        payload = {'train_data':X_train, 'batch':True, 'api':data['modelEndPoint'], 'data':data['data'], 'prediction':data['prediction']}
        api_data_variable = payload['data']
        api_response_variable = payload['prediction']
        headers ={'Content-Type': 'application/json'}
        request_data =json.dumps({api_data_variable: payload['train_data'].tolist()})
        response = requests.post(payload['api'], request_data, headers=headers)
        Expectedprediction = json.loads(response.text)[api_response_variable]
        result = Utility.getPredictionsFromEndpoint(payload)
        assert result == Expectedprediction

    def test_getPredictionsFromEndpoint_batchfalse(self):
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestUtility.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload,data,X_train = TestUtility.getPayloadforcreateArtEstimator(batchId)
        payload = {'train_data':X_train[0], 'batch':False, 'api':data['modelEndPoint'], 'data':data['data'], 'prediction':data['prediction']}
        api_data_variable = payload['data']
        api_response_variable = payload['prediction']
        headers ={'Content-Type': 'application/json'}
        request_data =json.dumps({api_data_variable: payload['train_data'].reshape(1, -1).tolist()})
        response = requests.post(payload['api'], request_data, headers=headers)
        Expectedprediction = json.loads(response.text)[api_response_variable]
        result = Utility.getPredictionsFromEndpoint(payload)
        assert result == Expectedprediction

    def test_getPredictionsFromEndpoint_None(self):
        TestUtility.reportDeletion()
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestUtility.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload,data,X_train = TestUtility.getPayloadforcreateArtEstimator(batchId)
        payload = {'train_data':X_train, 'batch':None, 'api':data['modelEndPoint'], 'data':data['data'], 'prediction':data['prediction']}
        with pytest.raises(Exception):
            Utility.getPredictionsFromEndpoint(payload) 

