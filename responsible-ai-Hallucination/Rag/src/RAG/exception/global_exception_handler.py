import os,sys

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .global_exception import UnSupportedMediaTypeException
from fastapi.encoders import jsonable_encoder
from RAG.constants import constants


def validation_error_handler(exc: RequestValidationError):
    return JSONResponse(
        status_code=int(constants.HTTP_422_UNPROCESSABLE_ENTITY),
        content=jsonable_encoder({"detail": exc.errors()}),

    )

def  http_exception_handler(exc):
     return JSONResponse(
         status_code=exc.status_code,
         content=jsonable_encoder({"detail": str(exc.detail)})
    )

def unsupported_mediatype_error_handler(exc:UnSupportedMediaTypeException):
     return JSONResponse(
         status_code=exc.status_code,
         content=jsonable_encoder({"detail": str(exc.message)})
    )





#def my_except_hook(exctype, value, traceback):
    #sys.__excepthook__(exctype, value, traceback)


#sys.excepthook = my_except_hook




