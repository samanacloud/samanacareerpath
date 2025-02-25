from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class Interview:
    id: str = strawberry.field(description="Interview ID", name="id")
    companyId: str
    companyName: str
    email: str
    recruitmentProcessId: str
    recruitmentProcessName: str
    availability: str
    evaluationField: str
    rating: int
    interviewedBy: str
    interviewerEmail: str
    observations: str
    approved: str
    createdAt: datetime

@strawberry.input
class AddInterviewInput:
    companyId: str
    companyName: str
    email: str
    recruitmentProcessId: str
    recruitmentProcessName: str
    availability: str
    evaluationField: str
    rating: int
    interviewedBy: str
    interviewerEmail: str
    observations: str
    approved: str

@strawberry.input
class EditInterviewInput:
    availability: Optional[str] = None
    evaluationField: Optional[str] = None
    rating: Optional[int] = None
    observations: Optional[str] = None
    approved: Optional[str] = None 