'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024-2025 Infosys Ltd.
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from src.service.artendpoint import ArtEndPoint
import pytest
from src.config.urls import UrlLinks
from src.service.utility import Utility
import shutil
import os
from test.service.addModelToMockDatabase import AddModel
from test.service.ModelDataAddition import AddModelData,GetBatchPayloadRequest
from src.dao.ModelDb import Model
from src.dao.DataDb import Data

class TestArtEndPoint:
    @classmethod
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModel.SklearnAPIClassifierTabular()
        cls.modelDictSklearnAPIClassifierTabular = Model.findall({'ModelName':'SklearnAPIClassifierTabularModel'})[0]
        cls.modelIdSklearnAPIClassifierTabular = cls.modelDictSklearnAPIClassifierTabular['ModelId']
        cls.dataDictSklearnAPIClassifierTabular = Data.findall({'DataSetName':'SklearnAPIClassifierTabularData'})[0]
        cls.dataIdSklearnAPIClassifierTabular = cls.dataDictSklearnAPIClassifierTabular['DataId']


    def pathFinder():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestArtEndPoint.pathFinder()
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

# #------------------QueryEfficientGradientAttackEndPoint Attack----------------

    def test_QueryEfficientGradientAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'QueryEfficientGradientAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.QueryEfficientGradientAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_QueryEfficientGradientAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            ArtEndPoint.QueryEfficientGradientAttack(None) 


# # #--------------------------------BoundaryAttackEndPoint Attack---------------

    def test_BoundaryAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'BoundaryAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.BoundaryAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_BoundaryAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            self.ArtEndPoint.BoundaryAttack(None)


# #--------------------------------HopSkipJumpAttackEndPoint Attack---------------

    def test_HopSkipJumpAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'HopSkipJumpAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.HopSkipJumpAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_HopSkipJumpAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            ArtEndPoint.HopSkipJumpAttack(None)


# # #--------------------------------LabelOnlyGapAttackEndPoint Attack---------------

    def test_LabelOnlyGapAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'LabelOnlyGapAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.LabelOnlyGapAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_LabelOnlyGapAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            ArtEndPoint.LabelOnlyGapAttack(None)


# #--------------------------------MembershipInferenceBlackBoxRuleBasedAttackEndPoint Attack---------------

    def test_MembershipInferenceBlackBoxRuleBasedAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'MembershipInferenceBlackBoxRuleBasedAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.MembershipInferenceBlackBoxRuleBasedAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_MembershipInferenceBlackBoxRuleBasedAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            ArtEndPoint.MembershipInferenceBlackBoxRuleBasedAttack(None)


# #--------------------------------LabelOnlyDecisionBoundaryAttackEndPoint Attack---------------

    def test_LabelOnlyDecisionBoundaryAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'LabelOnlyDecisionBoundaryAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.LabelOnlyDecisionBoundaryAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_LabelOnlyDecisionBoundaryAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            ArtEndPoint.LabelOnlyDecisionBoundaryAttack(None)
     

# #--------------------------------MembershipInferenceBlackBoxAttackEndPoint Attack---------------

    def test_MembershipInferenceBlackBoxAttack(self):
        TestArtEndPoint.reportDeletion()
        attackName = 'MembershipInferenceBlackBoxAttackEndPoint'
        batchId = TestArtEndPoint.getBatchId(self.modelIdSklearnAPIClassifierTabular,self.dataIdSklearnAPIClassifierTabular,[attackName])
        value = ArtEndPoint.MembershipInferenceBlackBoxAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_MembershipInferenceBlackBoxAttack_None(self):
        TestArtEndPoint.reportDeletion()
        with pytest.raises(Exception):
            self.ArtEndPoint.MembershipInferenceBlackBoxAttack(None)

 










