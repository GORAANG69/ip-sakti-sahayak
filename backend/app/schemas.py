from typing import Any, Optional
from pydantic import BaseModel, Field

class Credentials(BaseModel):
    email:str=Field(min_length=1,max_length=200)
    password:str=Field(min_length=1,max_length=200)

class ChatRequest(BaseModel):
    message:str=Field(min_length=1,max_length=5000)
    jurisdiction:str='India'
    language:str='English'

class ChatResponse(BaseModel):
    answer:str
    confidence:str
    jurisdiction:str
    language:str
    citations:list[dict[str,Any]]=[]
    evidence:list[dict[str,Any]]=[]
    abstained:bool=False
    reason:Optional[str]=None
    suggested_next_steps:list[str]=[]
