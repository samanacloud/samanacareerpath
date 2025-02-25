from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class CertificationData:
    id: str = strawberry.field(description="Certification ID", name="id")
    companyId: str
    companyName: str
    email: str
    certificationName: str
    certificationExpiration: datetime
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

@strawberry.input
class AssignCertificationInput:
    companyId: str
    companyName: str
    email: str
    certificationName: str
    certificationExpiration: datetime

@strawberry.input
class UpdateCertificationInput:
    certificationName: Optional[str] = None
    certificationExpiration: Optional[datetime] = None 