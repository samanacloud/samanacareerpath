from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class Candidate:
    id: str = strawberry.field(description="Candidate ID", name="id")
    companyId: str = strawberry.field(description="Company ID")
    companyName: str = strawberry.field(description="Company Name")
    recruitmentProcessId: str = strawberry.field(description="Recruitment Process ID")
    recruitmentProcessName: str = strawberry.field(description="Recruitment Process Name")
    candidateName: str = strawberry.field(description="Candidate Name")
    email: str = strawberry.field(description="Email")
    country: str = strawberry.field(description="Country")
    phone: str = strawberry.field(description="Phone Number")
    candidateCV: str = strawberry.field(description="Candidate CV URL")
    status: str = strawberry.field(description="Candidate Status")
    createdAt: datetime = strawberry.field(description="Creation timestamp")
    updatedAt: datetime = strawberry.field(description="Last update timestamp")

@strawberry.input
class CreateCandidateInput:
    companyId: str
    companyName: str
    recruitmentProcessId: str
    recruitmentProcessName: str
    candidateName: str
    email: str
    country: str
    phone: str
    candidateCV: str
    status: str = strawberry.field(default="active", description="Candidate status")

@strawberry.input
class UpdateCandidateInput:
    companyId: Optional[str] = None
    companyName: Optional[str] = None
    recruitmentProcessId: Optional[str] = None
    recruitmentProcessName: Optional[str] = None
    candidateName: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    candidateCV: Optional[str] = None
    status: Optional[str] = None

@strawberry.input
class EnrollCandidateInput:
    id: str
    recruitmentProcessId: str
    recruitmentProcessName: str 