from pydantic import BaseModel, Field

class AWSReq(BaseModel):
    credName:str=Field(example="aws")
    awsAccessKeyId:str=Field(example="xyz")
    awsSecretAccessKey:str=Field(example="xyz")
    awsSessionToken:str=Field(example="xyz")

class AWSStatus(BaseModel):
    status:str=Field(example="success")
    class Config:
        orm_mode = True

class AWSRes(BaseModel):
    credName:str=Field(example="aws")
    awsAccessKeyId:str=Field(example="xyz")
    awsSecretAccessKey:str=Field(example="xyz")
    awsSessionToken:str=Field(example="xyz")
    class Config:
        orm_mode = True

class CredUpdate(BaseModel):
    credName:str=Field(example="aws")
    awsAccessKeyId:str=Field(example="xyz")
    awsSecretAccessKey:str=Field(example="xyz")
    awsSessionToken:str=Field(example="xyz")
        