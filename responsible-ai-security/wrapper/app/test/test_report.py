'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024-2025 Infosys Ltd.
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pytest
from src.config.urls import UrlLinks
from src.service.report import Report
from src.service.utility import Utility   
from test.service.addModelToMockDatabase import AddModel
from test.service.ModelDataAddition import AddModelData,GetBatchPayloadRequest
from src.dao.ModelDb import Model
from src.dao.DataDb import Data
from sklearn.model_selection import train_test_split
from art.attacks.evasion import BasicIterativeMethod
from art.estimators.classification import KerasClassifier
import tensorflow as tf
if tf.executing_eagerly():
    tf.compat.v1.disable_eager_execution()
import os
import json
import numpy as np
import pandas as pd
from art.estimators.classification import SklearnClassifier
from art.attacks.inference.membership_inference import MembershipInferenceBlackBoxRuleBased
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import shutil

class TestReport:
    @classmethod
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModel.SklearnClasifierTabular()
        AddModel.KerasClassifierImage()
        AddModel.SklearnAPIClassifierTabular()
        cls.modelDictSklearnClassifierTabular = Model.findall({'ModelName':'SklearnClassifierTabularModel'})[0]
        cls.modelIdSklearnClassifierTabular = cls.modelDictSklearnClassifierTabular['ModelId']
        cls.dataDictSklearnClassifierTabular = Data.findall({'DataSetName':'SklearnClassifierTabularData'})[0]
        cls.dataIdSklearnClassifierTabular = cls.dataDictSklearnClassifierTabular['DataId']
        cls.modelDictKerasClassifierImage = Model.findall({'ModelName':'KerasClassifierImageModel'})[0]
        cls.modelIdKerasClassifierImage = cls.modelDictKerasClassifierImage['ModelId']
        cls.dataDictKerasClassifierImage = Data.findall({'DataSetName':'KerasClassifierImageData'})[0]
        cls.dataIdKerasClassifierImage = cls.dataDictKerasClassifierImage['DataId']
        cls.modelDictSklearnAPIClassifierTabular = Model.findall({'ModelName':'SklearnAPIClassifierTabularModel'})[0]
        cls.modelIdSklearnAPIClassifierTabular = cls.modelDictSklearnAPIClassifierTabular['ModelId']
        cls.dataDictSklearnAPIClassifierTabular = Data.findall({'DataSetName':'SklearnAPIClassifierTabularData'})[0]
        cls.dataIdSklearnAPIClassifierTabular = cls.dataDictSklearnAPIClassifierTabular['DataId']
        cls.payload_sklearnapiclassifiertabular = {}
        cls.payload_sklearnapiclassifiertabular['modelName'] = 'SklearnAPIClassifierTabularModel' 
        cls.payload_sklearnapiclassifiertabular['attackName'] = 'LabelOnlyGapAttackEndPoint' 
        cls.payload_sklearnapiclassifiertabular['inference_acc'] = 1.0


    def Payload_sklearnclassifiertabular(payload):
        raw_data, data_path = Utility.readDataFile(payload)
        model, model_path, modelName = Utility.readModelFile(payload)
        Payload_path = Utility.readPayloadFile(payload)
        list_of_column_names = list(raw_data.columns)
        payload_folder_path = Utility.getcurrentDirectory() + "/database/payload"
        payload_path = os.path.join(payload_folder_path,modelName + ".txt")
        with open(f'{payload_path}') as f:
            data = f.read()
        data = json.loads(data)
        Output_column = data["groundTruthClassLabel"]
        X = raw_data.drop([Output_column], axis=1).to_numpy()
        Y = raw_data[[Output_column]].to_numpy()
        list_of_column_names.remove(Output_column)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        classifier = SklearnClassifier(model=model)
        attack = MembershipInferenceBlackBoxRuleBased(classifier)
        inferred_train = attack.infer(x_train, y_train)
        inferred_test = attack.infer(x_test, y_test)
        train_acc = np.sum(inferred_train) / len(inferred_train)
        test_acc = 1 - (np.sum(inferred_test) / len(inferred_test))
        acc = (train_acc * len(inferred_train) + test_acc * len(inferred_test)) / (len(inferred_train) + len(inferred_test))
        x,y = Utility.calc_precision_recall(np.concatenate((inferred_train, inferred_test)),
                            np.concatenate((np.ones(len(inferred_train)), np.zeros(len(inferred_test)))))
        attack_data_list,attack_data_status = Utility.combineList({'attack_data':x_train,'target_data':y_train,'prediction_data':inferred_train,'type':'Inference'})
        list_of_column_names.extend([Output_column, 'prediction', 'result'])
        Payload = {
                'modelName':modelName,
                'attackName':"MembershipInferenceRule",
                'dataFileName':os.path.basename(data_path).split('.')[0],
                'adversial_sample':attack_data_list,
                'perturbation':acc,
                'columns':list_of_column_names,
                'attack_data_status':attack_data_status
            }
        return Payload,data_path,model_path,Payload_path

    def pathFinder():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        root_path = new_path + "/database"
        return root_path  

    def databasePath():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestReport.databasePath()
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

    def Payload_kerasclassifierimage(payload):

        img, data_path = Utility.readDataFile(payload)
        model, model_path, modelName = Utility.readModelFile(payload)
        Payload_path = Utility.readPayloadFile(payload)
        x = image.img_to_array(img)
        x = x / 255
        x_art = np.expand_dims(x, axis=0)
        pred = model.predict(x_art)
        actual_prediction = np.argmax(pred, axis=1)[0]
        base_actual_confidence = pred[:,actual_prediction][0]
        Defect_Class = {0: "Pit defect", 1: "Edge crack", 2: "Scratches", 3: "Rolled-in scale"}
        base_prediction_class = Defect_Class[actual_prediction]
        classifier = KerasClassifier(model=model, clip_values=(0, 255))
        attack = BasicIterativeMethod(estimator=classifier,max_iter=10,eps=1.0,eps_step=0.005)
        x_train_adv = attack.generate(x_art)
        pred_adv = classifier.predict(x_train_adv)
        label_adv = np.argmax(pred_adv, axis=1)[0]
        adv_confidence = pred[:,label_adv][0]
        Defect_Class = {0: "Pit defect", 1: "Edge crack", 2: "Scratches", 3: "Rolled-in scale"}
        adv_prediction_class = Defect_Class[label_adv]
        perturbation = np.mean(np.abs((x_train_adv - x_art)))
        Payload = {
                'modelName':modelName,
                'attackName':"BasicIterativeMethod",
                'imageName':f"{os.path.basename(data_path).split('.')[0]}_BasicIterativeMethod",
                'base_sample':x_art,
                'adversial_sample':x_train_adv,
                'basePrediction_class':base_prediction_class,
                'adversialPrediction_class':adv_prediction_class,
                'baseActual_confidence':base_actual_confidence,
                'adversialActual_confidence':adv_confidence,
                'perturbation':perturbation
            }

        return Payload,data_path,model_path,Payload_path 

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


    def test_generatecsvreportart(self):
        TestReport.reportDeletion()
        attackName = 'MembershipInferenceRule'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        response = Report.generatecsvreportart(data_sklearnclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput 

    def test_generatecsvreportart_attack_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,['None'])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        data_sklearnclassifiertabular['attackName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart(data_sklearnclassifiertabular) 

    def test_generatecsvreportart_model_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        attackName = 'MembershipInferenceRule'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        data_sklearnclassifiertabular['modelName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart(data_sklearnclassifiertabular) 


    def test_generatecsvreportartendpoint(self):
        TestReport.reportDeletion()
        attackName = 'MembershipInferenceBlackBox'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId) 
        data_sklearnclassifiertabular['attackName'] = 'MembershipInferenceBlackBox'
        response = Report.generatecsvreportartendpoint(data_sklearnclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput

    def test_generatecsvreportartendpoint_attack_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,['None'])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId) 
        data_sklearnclassifiertabular['attackName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart(data_sklearnclassifiertabular)  

    def test_generatecsvreportartendpoint_model_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        attackName = 'MembershipInferenceRule'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId) 
        data_sklearnclassifiertabular['modelName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart(data_sklearnclassifiertabular)

    def test_generateimagereport(self):
        TestReport.reportDeletion()
        attackName = 'BasicIterativeMethod'
        batchId = TestReport.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        data_kerasclassifierimage,data_path_kerasclassifierimage,model_path_kerasclassifierimage,Payload_path_kerasclassifierimage = TestReport.Payload_kerasclassifierimage(batchId)  
        response = Report.generateimagereport(data_kerasclassifierimage)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput 

    def test_generateimagereport_attack_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        attackName = 'BasicIterativeMethod'
        batchId = TestReport.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        data_kerasclassifierimage,data_path_kerasclassifierimage,model_path_kerasclassifierimage,Payload_path_kerasclassifierimage = TestReport.Payload_kerasclassifierimage(batchId)  
        data_kerasclassifierimage['attackName'] = None
        with pytest.raises(Exception):
            Report.generateimagereport(data_kerasclassifierimage) 

    def test_generateinferencereport_LabelOnlyGapAttackEndPoint(self):
        TestReport.reportDeletion()
        attackName = self.payload_sklearnapiclassifiertabular['attackName']
        batchId = TestReport.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payloadPath = Utility.readPayloadFile(batchId)
        response = Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput

    def test_generateinferencereport_LabelOnlyDecisionBoundaryAttackEndPoint(self):
        TestReport.reportDeletion()
        attackName = 'LabelOnlyDecisionBoundaryAttackEndPoint'
        batchId = TestReport.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payloadPath = Utility.readPayloadFile(batchId)
        self.payload_sklearnapiclassifiertabular['attackName'] = 'LabelOnlyDecisionBoundaryAttackEndPoint'
        response = Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput

    def test_generateinferencereport_MembershipInferenceBlackBoxRuleBasedAttackEndPoint(self):
        TestReport.reportDeletion()
        attackName = 'MembershipInferenceBlackBoxRuleBasedAttackEndPoint'
        batchId = TestReport.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payloadPath = Utility.readPayloadFile(batchId)
        self.payload_sklearnapiclassifiertabular['attackName'] = 'MembershipInferenceBlackBoxRuleBasedAttackEndPoint'
        response = Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput

    def test_generateinferencereport_MembershipInferenceBlackBoxAttackEndPoint(self):
        TestReport.reportDeletion()
        attackName = 'MembershipInferenceBlackBoxAttackEndPoint'
        batchId = TestReport.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payloadPath = Utility.readPayloadFile(batchId)
        self.payload_sklearnapiclassifiertabular['attackName'] = 'MembershipInferenceBlackBoxAttackEndPoint'
        response = Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput

    def test_generateinferencereport_attack_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        self.payload_sklearnapiclassifiertabular['attackName'] = None
        with pytest.raises(Exception):
            Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)

    def test_generateinferencereport_model_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        self.payload_sklearnapiclassifiertabular['modelName'] = None
        with pytest.raises(Exception):
            Report.generateinferencereport(self.payload_sklearnapiclassifiertabular)   

    def test_generatecsvreportart1(self):
        TestReport.reportDeletion()
        attackName = 'MembershipInferenceRule'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        response = Report.generatecsvreportart1(data_sklearnclassifiertabular)
        id = UrlLinks.Current_ID - 1
        expectedOutput = f'{attackName}_{id}'
        assert response == expectedOutput 

    def test_generatecsvreportart1_attack_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,['None'])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        data_sklearnclassifiertabular['attackName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart1(data_sklearnclassifiertabular) 

    def test_generatecsvreportart1_model_None(self):
        TestReport.reportDeletion()
        Utility.updateCurrentID()
        attackName = 'MembershipInferenceRule'
        batchId = TestReport.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        data_sklearnclassifiertabular,data_path_sklearnclassifiertabular,model_path_sklearnclassifiertabular,Payload_path_sklearnclassifiertabular = TestReport.Payload_sklearnclassifiertabular(batchId)  
        data_sklearnclassifiertabular['modelName'] = None
        with pytest.raises(Exception):
            Report.generatecsvreportart1(data_sklearnclassifiertabular)  
