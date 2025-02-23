from datetime import datetime
import strawberry
from typing import Optional, Dict, Any

@strawberry.type
class LicenseMetadata:
    """Type for license metadata"""
    notes: Optional[str] = None
    custom_field1: Optional[str] = None
    custom_field2: Optional[str] = None

@strawberry.type
class License:
    id: str = strawberry.field(description="License ID")
    licenseKey: str = strawberry.field(description="Unique license key")
    licenseType: str = strawberry.field(description="Type of license (e.g., t0, t1)")
    licenseStatus: str = strawberry.field(description="Status of the license")
    createdAt: datetime = strawberry.field(description="Creation timestamp")
    updatedAt: datetime = strawberry.field(description="Last update timestamp")
    createdBy: str = strawberry.field(description="Creator identifier")
    updatedBy: str = strawberry.field(description="Last updater identifier")
    companyId: str = strawberry.field(description="Associated company ID")
    assignedTo: Optional[str] = strawberry.field(description="User the license is assigned to")
    expiresAt: Optional[datetime] = strawberry.field(description="License expiration date")
    metadata: Optional[LicenseMetadata] = strawberry.field(description="Additional metadata")

@strawberry.input
class CreateLicenseInput:
    licenseType: str
    companyId: str
    createdBy: str
    assignedTo: Optional[str] = None
    expiresAt: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None

@strawberry.input
class UpdateLicenseInput:
    licenseStatus: Optional[str] = None
    updatedBy: Optional[str] = None
    companyId: Optional[str] = None
    assignedTo: Optional[str] = None
    expiresAt: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None 