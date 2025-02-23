from datetime import datetime
import strawberry
from typing import Optional, List

@strawberry.input
class JobDetailInput:
    category: str
    description: str

@strawberry.type
class JobDetail:
    category: str
    description: str

@strawberry.type
class JobDetailsArray:
    category: str
    description: str

@strawberry.type
class Recruitment:
    id: str = strawberry.field(description="Recruitment Process ID")
    companyId: str = strawberry.field(description="Company ID")
    companyName: str = strawberry.field(description="Company Name")
    jobCategory: str = strawberry.field(description="Job Category")
    jobName: str = strawberry.field(description="Job Name")
    jobDetails: str = strawberry.field(description="Job Details")
    workplaceType: str = strawberry.field(description="Workplace Type")
    jobType: str = strawberry.field(description="Job Type")
    salaryRange: str = strawberry.field(description="Salary Range")
    postUrl: str = strawberry.field(description="Post URL")
    status: str = strawberry.field(description="Status")
    createdAt: datetime = strawberry.field(description="Creation timestamp")
    createdBy: str = strawberry.field(description="Created By")
    updatedAt: datetime = strawberry.field(description="Last update timestamp")
    updatedBy: str = strawberry.field(description="Updated By")
    jobDetailsArray: Optional[List[JobDetail]] = strawberry.field(default=None, description="Job Details Array")

@strawberry.input
class CreateRecruitmentProcessInput:
    companyId: str
    companyName: str
    jobCategory: str
    jobName: str
    jobDetails: str
    workplaceType: str
    jobType: str
    salaryRange: str
    postUrl: str
    status: str = strawberry.field(default="active", description="Status")
    createdBy: str
    updatedBy: str
    jobDetailsArray: Optional[List[JobDetailInput]] = None

@strawberry.input
class UpdateRecruitmentProcessInput:
    jobCategory: Optional[str] = None
    jobName: Optional[str] = None
    jobDetails: Optional[str] = None
    workplaceType: Optional[str] = None
    jobType: Optional[str] = None
    salaryRange: Optional[str] = None
    postUrl: Optional[str] = None
    status: Optional[str] = None
    updatedBy: Optional[str] = None 