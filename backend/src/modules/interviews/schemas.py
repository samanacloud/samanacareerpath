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
    evaluationField: str = strawberry.field(description="Evaluation field")
    rating: int
    interviewedBy: str
    interviewerEmail: str
    observations: str
    approved: str
    createdAt: datetime
    
    @classmethod
    def from_db(cls, data: dict):
        """Create an Interview instance from a database document with field name normalization"""
        # Normalize field names
        normalized_data = {}
        field_mapping = {
            "evaluationfield": "evaluationField",
            "companyid": "companyId",
            "companyname": "companyName",
            "recruitmentprocessid": "recruitmentProcessId",
            "recruitmentprocessname": "recruitmentProcessName",
            "interviewedby": "interviewedBy",
            "intervieweremail": "interviewerEmail",
            "createdat": "createdAt"
        }
        
        for key, value in data.items():
            # Check if the lowercase key is in our mapping
            if key.lower() in field_mapping:
                normalized_key = field_mapping[key.lower()]
                normalized_data[normalized_key] = value
            else:
                normalized_data[key] = value
                
        return cls(**normalized_data)

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