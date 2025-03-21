'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024 Infosys Ltd
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from datetime import datetime
from questionnaire.dao.Questionnaires.AiCanvasDb import AICanvasDb
from questionnaire.mapper.Questionnaires.canvasMapper import *
from questionnaire.mapper.Questionnaires.aiCanvasMapper import *
from questionnaire.dao.Questionnaires.UseCaseDetailDb import *
from questionnaire.dao.ExceptionDb import ExceptionDb
from questionnaire.config.logger import request_id_var

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class AICanvasContent:
    def addAICanvasResponse(payload):
        try:
            payload = AttributeDict(payload)

            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
            res = AICanvasDb.findall({"UserId":payload.UserId,"useCaseNameId":useCaseDtl[0]._id})
            # print("payload16====",payload)
            log.debug("payload===="+str(payload))
            value = {"AICanvasResponse":payload.AICanvasResponse.dict(),"LastUpdatedDateTime": datetime.datetime.now()}
            response =""
            if(len(res) == 0):
                # useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId,"UseCaseName":payload.UseCaseName})
                # print("us3eCase dteails====",useCaseDtl)
                log.debug("useCaseDtl===="+str(useCaseDtl))
                responseDtl = AICanvasDb.create({"useCaseNameId":useCaseDtl[0]._id,"UserId":payload.UserId,"AICanvasResponse":payload.AICanvasResponse})
                # print("ResponseDtl23=====",responseDtl)
                log.debug("ResponseDtl===="+str(responseDtl))
                response="Added Successfully"
            else:
                data = res[0]
                responseUpdateDtl = AICanvasDb.update(data["_id"],value)
                response = " Updated Successfully..."
            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"addAICanvasResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
        
    def getSubmittedAICanvasResponse(userId,useCaseName):
        try:
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId,"UseCaseName":useCaseName})
            responseDetails = AICanvasDb.findall({"UserId":userId,"useCaseNameId":useCaseDtl[0]._id})
            if(len(responseDetails) == 0):
                return "No Record Found"
            else:
                # obj = CanvasDataResponse       
                # obj_ResponseData = Canvas(CanvasResponse=responseDetails[0].CanvasResponse)
                # obj.dataResponseList = [obj_ResponseData]
                return responseDetails[0].AICanvasResponse 
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getSubmittedAICanvasResponseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)   
           



