from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class Employee:
    id: str = strawberry.field(description="Employee ID", name="id")
    companyId: str = strawberry.field(description="Company ID")
    companyName: str = strawberry.field(description="Company Name")
    name: str = strawberry.field(description="Full Name")
    email: str = strawberry.field(description="Email")
    country: str = strawberry.field(description="Country")
    role: str = strawberry.field(description="Employee Role")
    phone: str = strawberry.field(description="Phone Number")
    status: str = strawberry.field(description="Employee Status")
    createdAt: datetime = strawberry.field(description="Creation timestamp")
    updatedAt: datetime = strawberry.field(description="Last update timestamp")

@strawberry.input
class CreateEmployeeInput:
    companyId: str
    companyName: str
    name: str
    email: str
    country: str
    role: str = strawberry.field(default="employee", description="Employee role")
    phone: str
    status: str = strawberry.field(default="active", description="Employee status")

@strawberry.input
class UpdateEmployeeInput:
    name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None 