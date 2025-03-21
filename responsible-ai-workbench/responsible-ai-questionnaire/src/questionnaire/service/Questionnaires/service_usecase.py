'''
MIT license https://opensource.org/licenses/MIT
Copyright 2024 Infosys Ltd
 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from questionnaire.dao.Questionnaires.UseCaseDetailDb import *

from questionnaire.mapper.Questionnaires.mapper import UseCaseNameRequest
from questionnaire.config.logger import request_id_var
from questionnaire.dao.ExceptionDb import ExceptionDb

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class UseCase:

    def createUseCase(payload) -> UseCaseNameRequest:
        # UseCaseNameDb
        try:
            payload =  AttributeDict(payload)
            # print("payload========",payload)
            log.debug("payload===="+str(payload))
            useCaseDtl = UseCaseNameDb.findall({"UserId":payload.UserId, "UseCaseName":payload.UseCaseName})
            if(len(useCaseDtl) > 0):
                response = "Use Case Already Created !!!!" 
            else:
                res = UseCaseNameDb.create({"UserId":payload.UserId, "UseCaseName":payload.UseCaseName})
                # print("Response======",res)
                log.debug("Response===="+str(res))
                response = "Use Case Created Successfully !!!!"


            return response
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"createUseCaseFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)
    

    def getUseCaseDetail(userId):
        try:
            # print("userID=====",userId)
            log.debug("userID===="+str(userId))
            useCaseDtl = UseCaseNameDb.findall({"UserId":userId})
            res=[]
            # print("useCaseDtl=========",useCaseDtl)
            log.debug("useCaseDtl===="+str(useCaseDtl))
            # res.append({"userid":userId})
            useCase=[]
            for i in useCaseDtl:
                useCaseData = {"UseCaseName": i.UseCaseName}
                use_case_data = {
                "UseCaseName": i.get("UseCaseName", None),
                "Score": i.get("Score", 0),
                "Risk_Classification": i.get("Risk_Classification", "NA")
                }
                useCase.append(use_case_data)
                # if hasattr(i, "UseCaseName"):
                #     print("True53========")
                #     print("i======",i)
                # try:
                #     useCaseData["Score"] = i.Score
                # except AttributeError:
                #     useCaseData["Score"] = None
                # if hasattr(i, "Score"):
                #     print("Inside if")
                #     useCaseData["Score"] = i.Score
                # else:
                #     print("Inside else")
                #     useCaseData["Score"] = None
                
                # if hasattr(i, 'Risk_Classification'):
                #     useCaseData["Risk_Classification"] = i.Risk_Classification
                # else:
                #     useCaseData["Risk_Classification"] = None
                
                # useCase.append(useCaseData)
            # for i in useCaseDtl:
            #     useCase.append({"UseCaseName":i.UseCaseName,"Score":i.Score,"Risk_Classification":i.Risk_Classification})
               
            # if(len)
            print("useCase=====",useCase)
            res.append({"useCaseName":useCase})
            return res
        except Exception as e:
            log.error(str(e))
            log.error("Line No:"+str(e.__traceback__.tb_lineno))
            log.error(str(e.__traceback__.tb_frame))
            ExceptionDb.create({"UUID":request_id_var.get(),"function":"getUseCaseDetailFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
            raise Exception(e)