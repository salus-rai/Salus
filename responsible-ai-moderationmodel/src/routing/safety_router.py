'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from flask import Blueprint
import time
from flask import  request
from werkzeug.exceptions import HTTPException
# from service.safety_service import ImageGen
import uuid
from exception.exception import modeldeploymentException
from config.logger import CustomLogger, request_id_var
from io import BytesIO
import base64


img_router = Blueprint('img_router', __name__,)
log=CustomLogger()

request_id_var.set('startup')
@img_router.post("/ImageGenerate")
def img():
    prompt = request.form.get("prompt")
    st=time.time()
    id=uuid.uuid4().hex
    request_id_var.set(id)
    log.info("Entered create usecase routing method")
    try:
        # log.info("before invoking create usecase service")
        
        # response = ImageGen.generate(prompt)
        # log.info("after invoking create usecase service ")
        
        # log.debug("response : " + str(response))
        log.info("exit create usecase routing method")
        log.info(f"Time taken by toxicity {time.time()-st}")
        imageByte=BytesIO()
        response.save(imageByte, format="png")
        imageByte=imageByte.getvalue()
        
        return base64.b64encode(imageByte).decode('utf-8')
    except modeldeploymentException as cie:
        log.error(cie.__dict__)
        log.info("exit create usecase routing method")
        raise HTTPException(**cie.__dict__)


