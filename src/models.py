from typing import List, Optional
from pydantic import BaseModel

class TechnicalSkill(BaseModel):
    name: str
    level: str
    years: str

class SoftSkill(BaseModel):
    skill: str
    examples: List[str]

class ProfileSkills(BaseModel):
    technical_skills: List[TechnicalSkill]
    soft_skills: List[SoftSkill]

class RequiredSkill(BaseModel):
    name: str
    level: str
    must_have: bool

class JobRequirements(BaseModel):
    required_skills: List[RequiredSkill]
    min_experience: str
    soft_skills: List[str]

class MissingSkill(BaseModel):
    skill: str
    severity: str

class UpgradeNeededSkill(BaseModel):
    skill: str
    current_level: str
    required_level: str
    severity: str

class GapAnalysis(BaseModel):
    missing_skills: List[MissingSkill]
    upgrade_needed: List[UpgradeNeededSkill]

class LearningResource(BaseModel):
    name: str
    url: Optional[str] = None
    type: str

class LearningPathItem(BaseModel):
    skill: str
    resources: List[LearningResource]
    estimated_time: str
    prerequisites: List[str]
    milestones: List[str]

class LearningPath(BaseModel):
    learning_path: List[LearningPathItem]
