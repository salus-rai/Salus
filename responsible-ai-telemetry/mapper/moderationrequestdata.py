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

class ModerationCheckThresholds(BaseModel):
    PromptinjectionThreshold: float
    JailbreakThreshold: float
    PiientitiesConfiguredToBlock: List[str]
    RefusalThreshold: float
    ToxicityThresholds: ToxicityThresholds
    ProfanityCountThreshold: int
    RestrictedtopicDetails: RestrictedtopicDetails
    CustomTheme: CustomTheme

class ModerationRequestData(BaseModel):
    AccountName: str
    userid: str
    PortfolioName: str
    lotNumber: int
    translate: str
    EmojiModeration: str
    Prompt: str
    ModerationChecks: List[str]
    ModerationCheckThresholds: ModerationCheckThresholds