from datetime import datetime
import secrets
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class LicenseRepository:
    def __init__(self):
        self.collection_name = "licenses"

    async def generate_unique_key(self) -> str:
        """Generate a unique license key"""
        while True:
            key = secrets.token_urlsafe(16)  # Generate a 16-byte URL-safe key
            db = await get_database()
            existing = await db[self.collection_name].find_one({"licenseKey": key})
            if not existing:
                return key

    async def create_license(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new license"""
        db = await get_database()
        
        # Generate unique license key
        license_key = await self.generate_unique_key()
        
        # Prepare license document
        license_doc = {
            "licenseKey": license_key,
            "licenseType": data["licenseType"],
            "licenseStatus": "unused",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "createdBy": data["createdBy"],
            "updatedBy": data["createdBy"],
            "companyId": data["companyId"],
            "assignedTo": data.get("assignedTo"),
            "expiresAt": data.get("expiresAt"),
            "metadata": data.get("metadata", {})
        }
        
        result = await db[self.collection_name].insert_one(license_doc)
        license_doc["id"] = str(result.inserted_id)
        return license_doc

    async def update_license(self, license_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a license by ID"""
        db = await get_database()
        
        # Prepare update document
        update_doc = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(license_id)},
            {"$set": update_doc},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_license(self, license_id: str) -> Optional[Dict[str, Any]]:
        """Get a license by ID"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"_id": ObjectId(license_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_licenses(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get all licenses with optional filters"""
        db = await get_database()
        cursor = db[self.collection_name].find(filters or {})
        licenses = []
        async for license in cursor:
            license["id"] = str(license.pop("_id"))
            licenses.append(license)
        return licenses

    async def delete_license(self, license_id: str) -> bool:
        """Delete a license by ID"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(license_id)})
        return result.deleted_count > 0 