from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class User:
    id: str = strawberry.field(description="User ID", name="id")
    companyId: str = strawberry.field(description="Company ID")
    companyName: str = strawberry.field(description="Company Name")
    name: str = strawberry.field(description="Full Name")
    email: str = strawberry.field(description="Email")
    country: str = strawberry.field(description="Country")
    role: str = strawberry.field(description="User Role")
    phone: str = strawberry.field(description="Phone Number")
    license: str = strawberry.field(description="License Type")
    status: str = strawberry.field(description="User Status")
    createdAt: datetime = strawberry.field(description="Creation timestamp")
    updatedAt: datetime = strawberry.field(description="Last update timestamp")

@strawberry.input
class CreateUserInput:
    companyId: str
    companyName: str
    name: str
    email: str
    country: str
    role: str = strawberry.field(default="user", description="User role")
    phone: str
    license: str = strawberry.field(default="t0", description="License type")
    status: str = strawberry.field(default="active", description="User status")

@strawberry.input
class UpdateUserInput:
    name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    license: Optional[str] = None
    status: Optional[str] = None 