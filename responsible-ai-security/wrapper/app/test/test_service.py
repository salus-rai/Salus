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
import pytest
from src.config.urls import UrlLinks
from src.service.utility import Utility
import os
import io
import unittest.mock as mock
import shutil
from src.service.service import Infosys,Bulk,AttributeDict
from src.dao.Html import Html
import datetime,time

class TestService:
    @classmethod
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModelData.loadApi()
        AddModel.SklearnClasifierTabular()
        AddModel.ScikitlearnClassifierTabular()
        AddModel.KerasClassifierImage()
        AddModel.SklearnAPIClassifierTabular()
        cls.modelDictSklearnClassifierTabular = Model.findall({'ModelName':'SklearnClassifierTabularModel'})[0]
        cls.modelIdSklearnClassifierTabular = cls.modelDictSklearnClassifierTabular['ModelId']
        cls.dataDictSklearnClassifierTabular = Data.findall({'DataSetName':'SklearnClassifierTabularData'})[0]
        cls.dataIdSklearnClassifierTabular = cls.dataDictSklearnClassifierTabular['DataId']
        cls.modelDictScikitlearnClassifierTabular = Model.findall({'ModelName':'ScikitlearnClassifierTabularModel'})[0]
        cls.modelIdScikitlearnClassifierTabular = cls.modelDictScikitlearnClassifierTabular['ModelId']
        cls.dataDictScikitlearnClassifierTabular = Data.findall({'DataSetName':'ScikitlearnClassifierTabularData'})[0]
        cls.dataIdScikitlearnClassifierTabular = cls.dataDictScikitlearnClassifierTabular['DataId']
        cls.modelDictKerasClassifierImage = Model.findall({'ModelName':'KerasClassifierImageModel'})[0]
        cls.modelIdKerasClassifierImage = cls.modelDictKerasClassifierImage['ModelId']
        cls.dataDictKerasClassifierImage = Data.findall({'DataSetName':'KerasClassifierImageData'})[0]
        cls.dataIdKerasClassifierImage = cls.dataDictKerasClassifierImage['DataId']
        cls.modelDictSklearnAPIClassifierTabular = Model.findall({'ModelName':'SklearnAPIClassifierTabularModel'})[0]
        cls.modelIdSklearnAPIClassifierTabular = cls.modelDictSklearnAPIClassifierTabular['ModelId']
        cls.dataDictSklearnAPIClassifierTabular = Data.findall({'DataSetName':'SklearnAPIClassifierTabularData'})[0]
        cls.dataIdSklearnAPIClassifierTabular = cls.dataDictSklearnAPIClassifierTabular['DataId']
        cls.targetClassifier = 'SklearnClassifier'
        cls.targetDataType = 'Tabular' 


    def databasePath():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestService.databasePath()
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

# # #----------------------------getAttackFuncs---------------------------

    def test_getAttackFuncs(self):
        payload = {'targetClassifier': self.targetClassifier, 'targetDataType': self.targetDataType}
        value = Infosys.getAttackFuncs(payload)
        k = 'ZerothOrderOptimization'
        assert k in value

    def test_getAttackFuncs_Classifier_None(self):
        payload = {'targetClassifier': None, 'targetDataType': self.targetDataType} 
        value = Infosys.getAttackFuncs(payload)
        assert len(value) == 0 

    def test_getAttackFuncs_DataType_None(self):
        payload = {'targetClassifier': self.targetClassifier, 'targetDataType': None} 
        value = Infosys.getAttackFuncs(payload)
        assert len(value) == 0 

# #  # #-------------------------addAttack---------------------

    def test_addAttack(self):
        payload = {'attackName':'ZerothOrderOptimization','attackDataType':self.targetDataType,'algorithmSupported':self.targetClassifier,'attackFunc':'ZerothOrderOptimization'}
        expectedOutput = 'Attack Already Exists'
        value = Infosys.addAttack(payload)
        assert value == expectedOutput

    def test_addAttack_None(self):
        payload = {'attackName': None,'attackDataType':None,'algorithmSupported':self.targetClassifier,'attackFunc':'ZerothOrderOptimization'}
        expectedOutPut = 'Attack Addition Failed! Please Try Again'
        value = Infosys.addAttack(payload)   
        assert value == expectedOutPut 

# # #---------------------setAttack-------------------------

    def test_setAttack_MembershipInferenceRule(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'MembershipInferenceRule'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_MembershipInferenceBlackBox(self):
        attackName = 'MembershipInferenceBlackBox'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'MembershipInferenceBlackBox'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_ZerothOrderOptimization(self):
        attackName = 'ZerothOrderOptimization'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'ZerothOrderOptimization'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_HopSkipJumpTabular(self):
        attackName = 'HopSkipJumpTabular'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'HopSkipJumpTabular'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_QueryEfficient(self):
        attackName = 'QueryEfficient'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'QueryEfficient'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_ProjectedGradientDescentTabular(self):
        attackName = 'ProjectedGradientDescentTabular'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'ProjectedGradientDescentTabular'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_InferenceLabelOnlyGap(self):
        attackName = 'InferenceLabelOnlyGap'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'InferenceLabelOnlyGap'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_AttributeInference(self):
        attackName = 'AttributeInference'
        batchId = TestService.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'AttributeInference'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput

    def test_setAttack_AttributeInferenceWhiteBoxDecisionTree(self):
        attackName = 'AttributeInferenceWhiteBoxDecisionTree'
        batchId = TestService.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'AttributeInferenceWhiteBoxDecisionTree'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_AttributeInferenceWhiteBoxLifestyleDecisionTree(self):
        attackName = 'AttributeInferenceWhiteBoxLifestyleDecisionTree'
        batchId = TestService.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'AttributeInferenceWhiteBoxLifestyleDecisionTree'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_DecisionTree(self):
        attackName = 'DecisionTree'
        batchId = TestService.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'DecisionTree'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_LabelOnlyDecisionBoundary(self):
        attackName = 'LabelOnlyDecisionBoundary'
        batchId = TestService.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'LabelOnlyDecisionBoundary'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput  

    def test_setAttack_BasicIterativeMethod(self):
        attackName = 'BasicIterativeMethod'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'BasicIterativeMethod'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_Boundary(self):
        attackName = 'Boundary'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'Boundary'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_CarliniL2Method(self):
        attackName = 'CarliniL2Method'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'CarliniL2Method'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_Deepfool(self):
        attackName = 'Deepfool'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'Deepfool'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_ElasticNet(self):
        attackName = 'ElasticNet'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'ElasticNet'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_FastGradientMethod(self):
        attackName = 'FastGradientMethod'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'FastGradientMethod'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_IterativeFrameSaliency(self):
        attackName = 'IterativeFrameSaliency'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'IterativeFrameSaliency'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_NewtonFool(self):
        attackName = 'NewtonFool'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'NewtonFool'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_SaliencyMapMethod(self):
        attackName = 'SaliencyMapMethod'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'SaliencyMapMethod'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_SimBA(self):
        attackName = 'SimBA'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'SimBA'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_SpatialTransformation(self):
        attackName = 'SpatialTransformation'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'SpatialTransformation'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_Square(self):
        attackName = 'Square'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'Square'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_UniversalPerturbation(self):
        attackName = 'UniversalPerturbation'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'UniversalPerturbation'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_Wasserstein(self):
        attackName = 'Wasserstein'
        batchId = TestService.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        payload = {"batchId":batchId, "modelUrl":'Wasserstein'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_QueryEfficientGradientAttackEndPoint(self):
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'QueryEfficientGradientAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_BoundaryAttackEndPoint(self):
        attackName = 'BoundaryAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'BoundaryAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_HopSkipJumpAttackEndPoint(self):
        attackName = 'HopSkipJumpAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'HopSkipJumpAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_LabelOnlyGapAttackEndPoint(self):
        attackName = 'LabelOnlyGapAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'LabelOnlyGapAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_MembershipInferenceBlackBoxRuleBasedAttackEndPoint(self):
        attackName = 'MembershipInferenceBlackBoxRuleBasedAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'MembershipInferenceBlackBoxRuleBasedAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_LabelOnlyDecisionBoundaryAttackEndPoint(self):
        attackName = 'LabelOnlyDecisionBoundaryAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'LabelOnlyDecisionBoundaryAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_MembershipInferenceBlackBoxAttackEndPoint(self):
        attackName = 'MembershipInferenceBlackBoxAttackEndPoint'
        batchId = TestService.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'MembershipInferenceBlackBoxAttackEndPoint'}
        TestService.reportDeletion()
        response =  Infosys.setAttack(payload)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert response == expectedOutput 

    def test_setAttack_ModelIdNone(self):
        payload = {"batchId":None, "modelUrl":'MembershipInferenceRule'}
        expectedOutput = {"Oops! Something is Wrong With Input, Please Retry!"} 
        response = Infosys.setAttack(payload)  
        assert response == expectedOutput

    def test_setAttack_AttackNone(self):
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,['None'])
        payload = {"batchId":batchId, "modelUrl":None}
        response = Infosys.setAttack(payload)  
        assert response == None

# #----------------------loadApi----------------------

    def test_loadApi(self,mocker):
        expectedOutput =  {
        "attackName": "LabelOnlyGapAttack",
        "attackDataType": "Tabular",
        "algorithmSupported": "SklearnAPIClassifier",  
        "attackFunc": "LabelOnlyGapAttackEndPoint"
        }
        mocked_loadApi = mocker.patch.object(Bulk, "loadApi", return_value = expectedOutput)
        response = Bulk.loadApi()
        assert response == expectedOutput

# # -----------------------batchAttack-------------------------

    def test_batchAttack(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":'MembershipInferenceRule'}
        TestService.reportDeletion()
        response = Bulk.batchAttack(payload)
        assert response == batchId

    def test_batchAttack_Model_None(self):
        payload = {"batchId":None, "modelUrl":'MembershipInferenceRule'} 
        TestService.reportDeletion()
        value = Bulk.batchAttack(payload) 
        expectedOutput = {"Oops! Something is Wrong With Input, Please Retry!"}  
        assert value == expectedOutput

    def test_batchAttack_Attack_None(self):
        attackName = 'MembershipInferenceRule'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        payload = {"batchId":batchId, "modelUrl":None} 
        TestService.reportDeletion()
        value = Bulk.batchAttack(payload) 
        expectedOutput = {"Oops! Something is Wrong With Input, Please Retry!"}  
        assert value == expectedOutput 

#-----------------------------combinereport--------------------

    def test_combinereport(self):
        TestService.reportDeletion()
        attackName = 'MembershipInferenceRule'
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        Payload = {"batchId":batchId, "modelUrl":attackName}
        Bulk.batchAttack(Payload)
        combineReportId = Bulk.combinereport({'batchid':batchId,'attackList':[attackName]})
        combineId = combineReportId['combineReportFileId'] 
        expectedId = Html.find_one(batchId, 3.3)
        assert combineId == expectedId

    def test_combinereport_attackNone(self):
        TestService.reportDeletion()
        batchId = TestService.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,['None'])
        payload = {'batchid':batchId,'attackList': None}
        with pytest.raises(Exception):
            Batch.combinereport(payload)  

    def test_combinereport_batchidNone(self):
        TestService.reportDeletion()
        attackName = 'ZerothOrderOptimization'
        payload = {'batchid':None,'attackList': [attackName]}
        with pytest.raises(Exception):
            Batch.combinereport(payload) 

# #----------------------runAllAttack----------------------

    def test_runAllAttack(self,mocker):
        id = time.time()
        mocked_loadApi = mocker.patch.object(Bulk, "runAllAttack", return_value = id)
        response = Bulk.runAllAttack()
        assert response == id

    def test_runAllAttack_None(self):
        with pytest.raises(Exception):
            Bulk.runAllAttack(None) 

#-----------------------AttributeDict------------------

    def test_AttributeDict(self):
        TestService.reportDeletion()
        expectedOutput = {"attackName":"ZerothOrderOptimization","attackid":"123"} 
        response = AttributeDict(expectedOutput)
        assert response == expectedOutput          





