from typing import Any, Optional
from pydantic import BaseModel, Field

class Credentials(BaseModel):
    email: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=1, max_length=200)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    jurisdiction: str = 'India'
    language: str = 'English'

class ChatResponse(BaseModel):
    answer: str
    confidence: str
    jurisdiction: str
    language: str
    citations: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    abstained: bool = False
    reason: Optional[str] = None
    suggested_next_steps: list[str] = []

class AnalyzeRequest(BaseModel):
    title: str = ''
    description: str = Field(min_length=1, max_length=10000)
    jurisdiction: str = 'India'

class FormulationDNA(BaseModel):
    problem: str
    limitations: str
    solution: str
    mechanism: str
    novel: str
    relationships: str
    functional: str
    advantages: str
    differentiating: str

class TwoSidedRequest(BaseModel):
    title: str = ''
    description: str = ''
    dna: Optional[dict[str, str]] = None
    jurisdiction: str = 'India'

class TwoSidedResponse(BaseModel):
    innovator_side: list[str]
    ip_side: list[str]

class RiskItem(BaseModel):
    area: str
    level: str
    note: str

class RiskRadarRequest(BaseModel):
    title: str = ''
    description: str = ''
    dna: Optional[dict[str, str]] = None
    jurisdiction: str = 'India'

class RiskRadarResponse(BaseModel):
    items: list[RiskItem]

class PathwayRequest(BaseModel):
    title: str = ''
    description: str = ''
    dna: Optional[dict[str, str]] = None
    jurisdiction: str = 'India'
    stage: str = 'Product Understanding'

class PathwayStep(BaseModel):
    title: str
    guidance: str
    checklist: list[str]
    references: list[str]

class PathwayResponse(BaseModel):
    stage: str
    steps: list[PathwayStep]

class SaveAnalysisRequest(BaseModel):
    title: str = 'Untitled Innovation'
    jurisdiction: str = 'India'
    dna: dict[str, str]

class AnalysisRecord(BaseModel):
    id: int
    title: str
    jurisdiction: str
    dna: dict[str, str]
    created_at: str
