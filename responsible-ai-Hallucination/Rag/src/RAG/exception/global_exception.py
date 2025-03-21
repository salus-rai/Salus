import sys, traceback

from RAG.constants import constants
from abc import ABC

class AicloudException(Exception, ABC):
    """
    Abstract base class of all Aicloud DB exceptions.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DbConnectionError(AicloudException):
     def __init__(self,name):
        self.status_code = constants.HTTP_STATUS_SERVICE_UNAVAILBLE
        self.message = constants.ERR_CONNECTION_REFUSED + name

class DataError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_DATA_PROCESSING_ERROR
        if not msg:
            self.message = constants.DATA_ERROR
        else: 
            self.message=msg

class OperationalError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_SERVICE_UNAVAILBLE
        if not msg:
            self.message = constants.OPERATIONAL_ERROR
        else: 
            self.message=msg

class IntegrityError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_SERVICE_UNAVAILBLE
        if not msg:
            self.message = constants.OPERATIONAL_ERROR
        else: 
            self.message=msg


class InternalError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_BAD_REQUEST
        if not msg:
            self.message = constants.DATA_ERROR
        else: 
            self.message=msg

class NotSupportedError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_NOT_ALLLOWED
        if not msg:
            self.message = constants.NOT_ALLOWED_MESSAGE
        else: 
            self.message=msg

class DatabaseError(AicloudException):
     def __init__(self,name):
        self.status_code = constants.HTTP_STATUS_NOT_FOUND
        self.message = name + constants.DATABASE_ERROR + name

class ForbiddenError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_FORBIDDEN
        if not msg:
            self.message = constants.FORBIDDEN_ERROR_MESSAGE
        else: 
            self.message=msg

class InternalServerError(AicloudException):
     def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_BAD_REQUEST
        if not msg:
            self.message = constants.DATA_ERROR
        else: 
            self.message=msg

class IncompleteRead(AicloudException):
    def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_BAD_REQUEST
        if not msg:
            self.message = constants.DATA_ERROR
        else: 
            self.message=msg

class MethodArgumentNotValidException(AicloudException):
    def __init__(self,msg):
        self.status_code = constants.HTTP_STATUS_BAD_REQUEST
        if not msg:
            self.message = constants.DATA_ERROR
        else: 
            self.message=msg

class UnSupportedMediaTypeException(AicloudException):
    def __init__(self,contentTypeStr):
        self.status_code = constants.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        self.message = constants.UNSUPPPORTED_MEDIA_TYPE_ERROR + contentTypeStr
        