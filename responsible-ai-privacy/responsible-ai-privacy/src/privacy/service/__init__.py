import contextvars
from presidio_analyzer import Pattern, PatternRecognizer, AnalyzerEngine, RecognizerRegistry,predefined_recognizers
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.entities import (RecognizerResult,
    OperatorResult,
    OperatorConfig,ConflictResolutionStrategy)
from privacy.config.logger import CustomLogger
from presidio_image_redactor import ImageRedactorEngine,ImageAnalyzerEngine,ImagePiiVerifyEngine       
from presidio_image_redactor import DicomImageRedactorEngine

from privacy.util.encrypt import EncryptImage
from privacy.config.logger import CustomLogger
log = CustomLogger()
print("===========init==========")
error_dict={}
admin_par={}
session_dict = contextvars.ContextVar('session_dict', default={})

# Example usage:
def update_session_dict(key, value):
    session_dict.get()[key] = value

def get_session_dict():
    return session_dict.get()

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
registry = RecognizerRegistry()
# log.info("============2a")
# analyzer = AnalyzerEngine(registry=registry)
# log.debug("============2b")
anonymizer = AnonymizerEngine()
# Create NLP engine based on configuration
# flair_recognizer = (
#     FlairRecognizer()
# ) 
# registry.add_recognizer(flair_recognizer)
# provider = NlpEngineProvider(nlp_configuration=configuration)
analyzer = AnalyzerEngine(registry=registry)
imageAnalyzerEngine = ImageAnalyzerEngine(analyzer_engine=analyzer)
imageRedactorEngine = ImageRedactorEngine(image_analyzer_engine=imageAnalyzerEngine)
imagePiiVerifyEngine = ImagePiiVerifyEngine(image_analyzer_engine=imageAnalyzerEngine) 
encryptImageEngin=EncryptImage(image_analyzer_engine=imageAnalyzerEngine)
deanonymizer = DeanonymizeEngine()
DicomEngine = DicomImageRedactorEngine()
registry.load_predefined_recognizers()

    
