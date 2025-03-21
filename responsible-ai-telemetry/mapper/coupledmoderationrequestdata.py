from pydantic import BaseModel
from typing import List, Dict

class ToxicityThresholds(BaseModel):
    ToxicityThreshold: float
    SevereToxicityThreshold: float
    ObsceneThreshold: float
    ThreatThreshold: float
    InsultThreshold: float
    IdentityAttackThreshold: float
    SexualExplicitThreshold: float

class RestrictedtopicDetails(BaseModel):
    RestrictedtopicThreshold: float
    Restrictedtopics: List[str]

class CustomTheme(BaseModel):
    Themename: str
    Themethresold: float
    ThemeTexts: List[str]

class SmoothLlmThreshold(BaseModel):
    input_pertubation: float
    number_of_iteration: int
    SmoothLlmThreshold: float

class ModerationCheckThresholds(BaseModel):
    PromptinjectionThreshold: float
    JailbreakThreshold: float
    PiientitiesConfiguredToBlock: List[str]
    RefusalThreshold: float
    ToxicityThresholds: ToxicityThresholds
    ProfanityCountThreshold: int
    RestrictedtopicDetails: RestrictedtopicDetails
    CustomTheme: CustomTheme
    SmoothLlmThreshold: SmoothLlmThreshold

class CoupledModerationRequestData(BaseModel):
    AccountName: str
    PortfolioName: str
    userid: str
    lotNumber: int
    model_name: str
    translate: str
    temperature: str
    LLMinteraction: str
    PromptTemplate: str
    EmojiModeration: str
    Prompt: str
    InputModerationChecks: List[str]
    OutputModerationChecks: List[str]
    llm_BasedChecks: List[str]
    ModerationCheckThresholds: ModerationCheckThresholds