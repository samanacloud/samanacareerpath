import strawberry
from typing import List, Optional
from datetime import datetime
from .schemas import License, LicenseMetadata
from .repository import LicenseRepository

@strawberry.type
class LicenseQueries:
    @strawberry.field
    async def license(self, id: str) -> Optional[License]:
        """Get a license by ID"""
        repo = LicenseRepository()
        result = await repo.get_license(id)
        if result:
            # Convert datetime objects to proper format
            if result.get("createdAt"):
                result["createdAt"] = datetime.fromisoformat(str(result["createdAt"]))
            if result.get("updatedAt"):
                result["updatedAt"] = datetime.fromisoformat(str(result["updatedAt"]))
            if result.get("expiresAt"):
                result["expiresAt"] = datetime.fromisoformat(str(result["expiresAt"]))
            
            # Convert metadata to LicenseMetadata type
            if result.get("metadata"):
                result["metadata"] = LicenseMetadata(**result["metadata"])
                
            return License(**result)
        return None

    @strawberry.field
    async def licenses(self, company_id: Optional[str] = None) -> List[License]:
        """Get all licenses, optionally filtered by company ID"""
        repo = LicenseRepository()
        filters = {"companyId": company_id} if company_id else None
        results = await repo.get_licenses(filters)
        return [License(
            id=str(license["id"]),
            licenseKey=license["licenseKey"],
            licenseType=license["licenseType"],
            licenseStatus=license["licenseStatus"],
            createdAt=datetime.fromisoformat(str(license["createdAt"])),
            updatedAt=datetime.fromisoformat(str(license["updatedAt"])),
            createdBy=license["createdBy"],
            updatedBy=license["updatedBy"],
            companyId=license["companyId"],
            assignedTo=license.get("assignedTo"),
            expiresAt=datetime.fromisoformat(str(license["expiresAt"])) if license.get("expiresAt") else None,
            metadata=LicenseMetadata(**license.get("metadata", {})) if license.get("metadata") else None
        ) for license in results]

    @strawberry.field
    async def licenses_by_company_id(self, company_id: str) -> List[License]:
        """Get all licenses for a specific company ID"""
        repo = LicenseRepository()
        results = await repo.get_licenses({"companyId": company_id})
        return [License(
            id=str(license["id"]),
            licenseKey=license["licenseKey"],
            licenseType=license["licenseType"],
            licenseStatus=license["licenseStatus"],
            createdAt=datetime.fromisoformat(str(license["createdAt"])),
            updatedAt=datetime.fromisoformat(str(license["updatedAt"])),
            createdBy=license["createdBy"],
            updatedBy=license["updatedBy"],
            companyId=license["companyId"],
            assignedTo=license.get("assignedTo"),
            expiresAt=datetime.fromisoformat(str(license["expiresAt"])) if license.get("expiresAt") else None,
            metadata=LicenseMetadata(**license.get("metadata", {})) if license.get("metadata") else None
        ) for license in results]

    @strawberry.field
    async def active_licenses_by_company_id(self, company_id: str) -> List[License]:
        """Get all non-expired licenses for a specific company ID"""
        repo = LicenseRepository()
        current_time = datetime.utcnow()
        
        filters = {
            "companyId": company_id,
            "$or": [
                {"expiresAt": {"$gt": current_time}},
                {"expiresAt": None}
            ]
        }
        
        results = await repo.get_licenses(filters)
        return [License(
            id=str(license["id"]),
            licenseKey=license["licenseKey"],
            licenseType=license["licenseType"],
            licenseStatus=license["licenseStatus"],
            createdAt=datetime.fromisoformat(str(license["createdAt"])),
            updatedAt=datetime.fromisoformat(str(license["updatedAt"])),
            createdBy=license["createdBy"],
            updatedBy=license["updatedBy"],
            companyId=license["companyId"],
            assignedTo=license.get("assignedTo"),
            expiresAt=datetime.fromisoformat(str(license["expiresAt"])) if license.get("expiresAt") else None,
            metadata=LicenseMetadata(**license.get("metadata", {})) if license.get("metadata") else None
        ) for license in results] 