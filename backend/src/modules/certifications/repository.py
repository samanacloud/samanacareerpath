from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class CertificationRepository:
    def __init__(self):
        self.collectionName = "certifications"

    async def _get_db(self):
        """Get database connection"""
        return await get_database()

    def _format_certification(self, certification: Dict[str, Any]) -> Dict[str, Any]:
        """Format certification document by converting _id to id"""
        if certification:
            certification["id"] = str(certification.pop("_id"))
            return certification
        return None

    async def create_certification(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new certification"""
        db = await self._get_db()
        certificationDoc = {
            "companyId": data["companyId"],
            "certificationVendor": data["certificationVendor"],
            "certificationName": data["certificationName"],
            "certificationShortName": data["certificationShortName"]
        }
        result = await db[self.collectionName].insert_one(certificationDoc)
        createdDoc = await db[self.collectionName].find_one({"_id": result.inserted_id})
        return self._format_certification(createdDoc)

    async def get_certification_by_id(self, certificationId: str, companyId: str) -> Optional[Dict[str, Any]]:
        """Get a certification by ID and company ID"""
        db = await self._get_db()
        result = await db[self.collectionName].find_one({
            "_id": ObjectId(certificationId),
            "companyId": companyId
        })
        return self._format_certification(result)

    async def get_all_certifications(self, companyId: str) -> List[Dict[str, Any]]:
        """Get all certifications for a company"""
        db = await self._get_db()
        cursor = db[self.collectionName].find({"companyId": companyId})
        certifications = []
        async for doc in cursor:
            certifications.append(self._format_certification(doc))
        return certifications

    async def get_certifications_by_vendor(self, companyId: str, certificationVendor: str) -> List[Dict[str, Any]]:
        """Get all certifications from a specific vendor for a company"""
        db = await self._get_db()
        cursor = db[self.collectionName].find({
            "companyId": companyId,
            "certificationVendor": certificationVendor
        })
        certifications = []
        async for doc in cursor:
            certifications.append(self._format_certification(doc))
        return certifications

    async def update_certification(self, certificationId: str, companyId: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a certification"""
        db = await self._get_db()
        updateData = {k: v for k, v in data.items() if v is not None and k != "companyId"}
        if not updateData:
            return None

        result = await db[self.collectionName].find_one_and_update(
            {
                "_id": ObjectId(certificationId),
                "companyId": companyId
            },
            {"$set": updateData},
            return_document=True
        )
        return self._format_certification(result)

    async def delete_certification(self, certificationId: str, companyId: str) -> bool:
        """Delete a certification"""
        db = await self._get_db()
        result = await db[self.collectionName].delete_one({
            "_id": ObjectId(certificationId),
            "companyId": companyId
        })
        return result.deleted_count > 0

    async def get_certification_vendors(self, companyId: str) -> List[str]:
        """Get all unique certification vendors for a company"""
        db = await self._get_db()
        vendors = await db[self.collectionName].distinct("certificationVendor", {"companyId": companyId})
        return vendors

    async def get_certifications_by_company_id(self, companyId: str) -> List[Dict[str, Any]]:
        """Get all certifications for a specific company"""
        db = await self._get_db()
        cursor = db[self.collectionName].find({"companyId": companyId})
        certifications = []
        async for doc in cursor:
            certifications.append(self._format_certification(doc))
        return certifications