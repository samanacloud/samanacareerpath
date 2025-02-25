from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class SkillsetData:
    id: str
    companyId: str
    companyName: str
    email: str
    skillsetCategory: str
    skillsetName: str
    skillsetRating: int
    reviewedBy: str
    reviewerEmail: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

@strawberry.input
class AssignSkillsetInput:
    companyId: str
    companyName: str
    email: str
    skillsetCategory: str
    skillsetName: str
    skillsetRating: int
    reviewedBy: str
    reviewerEmail: str 