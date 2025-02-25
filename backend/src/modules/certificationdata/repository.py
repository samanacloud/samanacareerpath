from datetime import datetime
from typing import List, Dict, Optional, Any
from bson import ObjectId
from database import get_database

class CertificationDataRepository:
    def __init__(self):
        self.collection_name = "certificationsdata"

    async def create_certification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new certification assignment"""
        db = await get_database()
        cert_doc = {
            **data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await db[self.collection_name].insert_one(cert_doc)
        cert_doc["id"] = str(result.inserted_id)
        return cert_doc

    async def update_certification(self, cert_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing certification"""
        db = await get_database()
        update_data = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(cert_id)},
            {"$set": update_data},
            return_document=True
        )
        if result:
            return self._format_certification(result)
        return None

    async def delete_certification(self, cert_id: str) -> bool:
        """Delete certification entry"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(cert_id)})
        return result.deleted_count > 0

    async def get_by_email(self, email: str) -> List[Dict[str, Any]]:
        """Get certifications by exact email match (case-sensitive)"""
        db = await get_database()
        cursor = db[self.collection_name].find({
            "email": email  # Direct match without regex
        })
        return [self._format_certification(doc) async for doc in cursor]

    async def get_by_company_and_domain(self, company_id: str, domain: str) -> List[Dict[str, Any]]:
        """Get certifications by company and email domain"""
        db = await get_database()
        regex_pattern = f"@{domain}$"
        cursor = db[self.collection_name].find({
            "companyId": company_id,
            "email": {"$regex": regex_pattern, "$options": "i"}
        })
        return [self._format_certification(doc) async for doc in cursor]

    def _format_certification(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Format document without adding timestamps"""
        doc["id"] = str(doc.pop("_id"))
        
        # Remove timestamp fields from response
        doc.pop("createdAt", None)
        doc.pop("updatedAt", None)
        
        return doc 