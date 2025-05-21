
'''
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from privacy.service.service import PrivacyService as ps
from privacy.config.logger import request_id_var
import uuid
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
class Privacy:
    def textAnalyze(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.analyze(AttributeDict(payload))
        
    def textAnonymize(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.anonymize(AttributeDict(payload))
    
    def imageAnalyze(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.image_analyze(AttributeDict(payload))
    def imageAnonymize(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.image_anonymize(AttributeDict(payload))
    def imageVerify(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.image_verify(AttributeDict(payload))
    def imageEncrypt(payload):
        id = uuid.uuid4().hex
        request_id_var.set(id)
        return ps.imageEncryption(AttributeDict(payload))
    


# d=AttributeDict({
#   "inputText": "Karan is working in Infosys. He is from Mumbai. His appointment for renewing passport is booked on March 12 and his old Passport Number is P2096457. Also, he want to link his Aadhaar Number is 567845678987 with his Pan Number is BNZAA2318A.",
#   "portfolio": None,
#   "account": None,
#   "exclusionList": None
# })
# Privacy.textAnalyze(d)





