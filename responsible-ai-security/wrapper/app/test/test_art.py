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
from src.service.art import Art
from src.config.urls import UrlLinks
import os
import shutil
import pytest
class TestArt:
    @classmethod
    def setup_class(cls):
        AddModelData.loadtenets()
        AddModelData.loadmodelattributes()
        AddModelData.loaddataattributes()
        AddModel.SklearnClasifierTabular()
        AddModel.ScikitlearnClassifierTabular()
        AddModel.KerasClassifierImage()        
        AddModel.TensorFlowV2ClassifierImage()
        
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
        
        cls.modelDictTensorFlowV2ClassifierImage = Model.findall({'ModelName':'TensorFlowV2ClassifierImageModel'})[0]
        cls.modelIdTensorFlowV2ClassifierImage = cls.modelDictTensorFlowV2ClassifierImage['ModelId']
        cls.dataDictTensorFlowV2ClassifierImage = Data.findall({'DataSetName':'TensorFlowV2ClassifierImageData'})[0]
        cls.dataIdTensorFlowV2ClassifierImage = cls.dataDictTensorFlowV2ClassifierImage['DataId']
        


    def pathFinder():
        root_path = os.getcwd()
        directories = root_path.split(os.path.sep)
        src_index = directories.index("src")
        new_path = os.path.sep.join(directories[:src_index])
        return new_path 

    def reportDeletion():
        new_path = TestArt.pathFinder()
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
            title='TestAttack',
            modelId = modelId,
            dataId = dataId,
            tenetName = ['Security'],
            appAttacks = attackList
        )
        batchdoc = AddModelData.getBatchList(payload)
        batchid = batchdoc[0]['BatchId']
        return batchid



#     #-------------------- MembershipInferenceRule Attack ----------------------------------

    def test_MembershipInferenceRule(self):
        TestArt.reportDeletion()
        attackName = 'MembershipInferenceRule'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.MembershipInferenceRule(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput


    def test_MembershipInferenceRule_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.MembershipInferenceRule(None)

# # # #-------------------- MembershipInferenceBlackBox Attack ----------------------------------

    def test_MembershipInferenceBlackBox(self):
        TestArt.reportDeletion()
        attackName = 'MembershipInferenceBlackBox'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.MembershipInferenceBlackBox(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_MembershipInferenceBlackBox_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.MembershipInferenceBlackBox(None) 

#     #-------------------- ZerothOrderOptimization Attack ----------------------------------

    def test_ZooAttackVectors(self):
        TestArt.reportDeletion()
        attackName = 'ZerothOrderOptimization'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.ZooAttackVectors(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_ZooAttackVectors_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.ZooAttackVectors(None)


#     #-------------------- HopSkipJumpTabular Attack ----------------------------------

    def test_HopSkipJumpCSV(self):
        TestArt.reportDeletion()
        attackName = 'HopSkipJumpTabular'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.HopSkipJumpCSV(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_HopSkipJumpCSV_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.HopSkipJumpCSV(None)


#     #-------------------------QueryEfficient Attack-------------------

    def test_QueryEfficient(self):
        TestArt.reportDeletion()
        attackName = 'QueryEfficient'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.QueryEfficient(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_QueryEfficient_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.QueryEfficient(None)
 

#     #-------------------------ProjectedGradientDescentTabular Attack-------------------

    def test_ProjectedGradientDescentZoo(self):
        TestArt.reportDeletion()
        attackName = 'ProjectedGradientDescentTabular'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.ProjectedGradientDescentZoo(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_ProjectedGradientDescentZoo_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.ProjectedGradientDescentZoo(None)


#     #------------------------------InferenceLabelOnlyGap Attack------------

    def test_InferenceLabelOnlyAttack(self):
        TestArt.reportDeletion()
        attackName = 'InferenceLabelOnlyGap'
        batchId = TestArt.getBatchId(self.modelIdSklearnClassifierTabular,self.dataIdSklearnClassifierTabular,[attackName])
        value = Art.InferenceLabelOnlyAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_InferenceLabelOnlyAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.InferenceLabelOnlyAttack(None)

#     #------------------------------AttributeInference Attack------------

    def test_AttributeInference(self):
        TestArt.reportDeletion()
        attackName = 'AttributeInference'
        batchId = TestArt.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        value = Art.AttributeInference(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_AttributeInference_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.AttributeInference(None)


#     #----------------------------AttributeInferenceWhiteBoxDecisionTree Attack-----------------

    def test_AttributeInferenceWhiteBoxDecisionTreeAttack(self):
        TestArt.reportDeletion()
        attackName = 'AttributeInferenceWhiteBoxDecisionTree'
        batchId = TestArt.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        value = Art.AttributeInferenceWhiteBoxDecisionTreeAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_AttributeInferenceWhiteBoxDecisionTreeAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.AttributeInferenceWhiteBoxDecisionTreeAttack(None)


#     #--------------------------AttributeInferenceWhiteBoxLifestyleDecisionTree Attack--------------------

    def test_AttributeInferenceWhiteBoxLifestyleDecisionTreeAttack(self):
        TestArt.reportDeletion()
        attackName = 'AttributeInferenceWhiteBoxLifestyleDecisionTree'
        batchId = TestArt.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        value = Art.AttributeInferenceWhiteBoxLifestyleDecisionTreeAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_AttributeInferenceWhiteBoxLifestyleDecisionTreeAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.AttributeInferenceWhiteBoxLifestyleDecisionTree(None)


#     #--------------------------DecisionTree Attack-------------------------

    def test_DecisionTreeAttackVectors(self):
        TestArt.reportDeletion()
        attackName = 'DecisionTree'
        batchId = TestArt.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        value = Art.DecisionTreeAttackVectors(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_DecisionTreeAttackVectors_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.DecisionTreeAttackVectors(None)


    #------------------------------LabelOnlyDecisionBoundary Attack----------------

    def test_LabelOnlyDecisionBoundaryAttack(self):
        TestArt.reportDeletion()
        attackName = 'LabelOnlyDecisionBoundary'
        batchId = TestArt.getBatchId(self.modelIdScikitlearnClassifierTabular,self.dataIdScikitlearnClassifierTabular,[attackName])
        value = Art.LabelOnlyDecisionBoundaryAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_LabelOnlyDecisionBoundaryAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.LabelOnlyDecisionBoundaryAttack(None)

# #------------------------------BasicIterativeMethod Attack----------------

    def test_BasicIterativeMethodAttack(self):
        TestArt.reportDeletion()
        attackName = 'BasicIterativeMethod'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.BasicIterativeMethodAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput

    def test_BasicIterativeMethodAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.BasicIterativeMethodAttack(None)

# #-----------------------Boundary Attack-----------------------------

    def test_BoundaryAttack(self):
        TestArt.reportDeletion()
        attackName = 'Boundary'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.BoundaryAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_BoundaryAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.BoundaryAttack(None)     

#     #---------------------------CarliniL2Method Attack---------------------  

    def test_CarliniAttack(self):
        TestArt.reportDeletion()
        attackName = 'CarliniL2Method'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.CarliniAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_CarliniAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.CarliniAttack(None)     

#     #------------------------Deepfool Attack----------------

    def test_DeepfoolAttack(self):
        TestArt.reportDeletion()
        attackName = 'Deepfool'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.DeepfoolAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_DeepfoolAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.DeepfoolAttack(None)

#     #-------------------------------ElasticNet Attack-----------------------

    def test_ElasticNetAttack(self):
        TestArt.reportDeletion()
        attackName = 'ElasticNet'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.ElasticNetAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_ElasticNetAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.ElasticNetAttack(None)

#     #-----------------------FastGradientMethod Attack---------------      

    def test_FastGradientMethodAttack(self):
        TestArt.reportDeletion()
        attackName = 'FastGradientMethod'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.FastGradientMethodAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_FastGradientMethodAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            self.Art.FastGradientMethodAttack(None)
      

#     #-----------------------IterativeFrameSaliency Attack---------------      

    def test_IterativeFrameSaliencyAttack(self):
        TestArt.reportDeletion()
        attackName = 'IterativeFrameSaliency'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.IterativeFrameSaliencyAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_IterativeFrameSaliencyAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.IterativeFrameSaliencyAttack(None)



#     #-----------------------NewtonFool Attack---------------      

    def test_NewtonFoolAttack(self):
        TestArt.reportDeletion()
        attackName = 'NewtonFool'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.NewtonFoolAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_NewtonFoolAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.NewtonFoolAttack(None)
  

#     # #-----------------------Pixel Attack---------------      

    def test_PixelAttack(self):
        TestArt.reportDeletion()
        attackName = 'Pixel'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.PixelAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_PixelAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.PixelAttack(None)    

#     #-----------------------SaliencyMapMethod Attack---------------      

    def test_SaliencyMapMethodAttack(self):
        TestArt.reportDeletion()
        attackName = 'SaliencyMapMethod'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.SaliencyMapMethodAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_SaliencyMapMethodAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.SaliencyMapMethodAttack(None)

#     #-----------------------SimBA Attack---------------      

    def test_SimbaAttack(self):
        TestArt.reportDeletion()
        attackName = 'SimBA'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.SimbaAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_SimbaAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.SimbaAttack(None)
    

#     #-----------------------SpatialTransformation Attack---------------      

    def test_SpatialTransformation(self):
        TestArt.reportDeletion()
        attackName = 'SpatialTransformation'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.SpatialTransformation(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_SpatialTransformation_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.SpatialTransformation(None)
        

#     #-----------------------Square Attack---------------      

    def test_SquareAttack(self):
        TestArt.reportDeletion()
        attackName = 'Square'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.SquareAttack(batchId)
        id = UrlLinks.Current_ID - 1
        attackName = 'Square'
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_SquareAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.SquareAttack(None)
     

#     #-----------------------UniversalPerturbation Attack---------------      

    def test_UniversalPerturbationAttack(self):
        TestArt.reportDeletion()
        attackName = 'UniversalPerturbation'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.UniversalPerturbationAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_UniversalPerturbationAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.UniversalPerturbationAttack(None)


#     #-----------------------Wasserstein Attack---------------      

    def test_WassersteinAttack(self):
        TestArt.reportDeletion()
        attackName = 'Wasserstein'
        batchId = TestArt.getBatchId(self.modelIdKerasClassifierImage,self.dataIdKerasClassifierImage,[attackName])
        value = Art.WassersteinAttack(batchId)
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        assert isinstance(value, dict)
        assert value == expectedOutput 

    def test_WassersteinAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.WassersteinAttack(None)
            
# # # #-------------------- GeometricDecisionBased Attack ----------------------------------

    def test_GeometricDecisionBasedAttack(self):
        TestArt.reportDeletion()
        attackName = 'GeometricDecisionBasedAttack'      
        batchId = TestArt.getBatchId(self.modelIdTensorFlowV2ClassifierImage,self.dataIdTensorFlowV2ClassifierImage,[attackName])        
        value = Art.GeometricDecisionAttack(batchId)
        
        id = UrlLinks.Current_ID - 1
        k = f'{attackName}_{id}'
        expectedOutput = {"Job_Id":f'{k}'}
        
        assert isinstance(value, dict)
        assert value == expectedOutput
                    
    def test_GeometricDecisionBasedAttack_None(self):
        TestArt.reportDeletion()
        with pytest.raises(Exception):
            Art.GeometricDecisionAttack(None)
        