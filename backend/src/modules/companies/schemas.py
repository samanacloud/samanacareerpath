from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class Company:
    id: str = strawberry.field(description="Company ID")
    companyName: str = strawberry.field(description="Company Name")
    email: str = strawberry.field(description="Company Email")
    phoneNumber: str = strawberry.field(description="Phone Number")
    adminName: str = strawberry.field(description="Admin Name")
    website: Optional[str] = strawberry.field(description="Website URL", default=None)
    country: Optional[str] = strawberry.field(description="Country", default=None)
    employeeRange: Optional[str] = strawberry.field(description="Employee Range", default=None)
    status: str = strawberry.field(description="Company Status")
    createdAt: datetime = strawberry.field(description="Creation Date")
    updatedAt: Optional[datetime] = strawberry.field(description="Last Update Date", default=None)

@strawberry.input
class CreateCompanyInput:
    companyName: str
    email: str
    phoneNumber: str
    adminName: str
    website: Optional[str] = None
    country: Optional[str] = None
    employeeRange: Optional[str] = None
    status: str = "active"

@strawberry.input
class UpdateCompanyInput:
    companyName: Optional[str] = None
    phoneNumber: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    employeeRange: Optional[str] = None
    status: Optional[str] = None 