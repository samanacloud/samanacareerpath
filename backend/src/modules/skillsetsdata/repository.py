from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database
from pymongo import MongoClient  # Or your preferred MongoDB library

class SkillsetDataRepository:
    def __init__(self):
        self.collection_name = "skillsetsdata"

    async def create_skillset(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new skillset entry"""
        db = await get_database()
        skillset_doc = {
            **data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await db[self.collection_name].insert_one(skillset_doc)
        skillset_doc["id"] = str(result.inserted_id)
        return skillset_doc

    async def update_skillset_rating(self, skillset_id: str, rating: int) -> Optional[Dict[str, Any]]:
        """Update skillset rating"""
        db = await get_database()
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(skillset_id)},
            {"$set": {"skillsetRating": rating, "updatedAt": datetime.utcnow()}},
            return_document=True
        )
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def delete_skillset(self, skillset_id: str) -> bool:
        """Delete skillset entry"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(skillset_id)})
        return result.deleted_count > 0

    async def get_by_email(self, email: str) -> List[Dict[str, Any]]:
        """Get skillsets by user email"""
        db = await get_database()
        cursor = db[self.collection_name].find({
            "email": {
                "$regex": f"^{email}$",
                "$options": "i"
            }
        })
        return [self._format_skillset(s) async for s in cursor]

    async def get_by_category(self, company_id: str, category: str) -> List[Dict[str, Any]]:
        """Get skillsets by category"""
        db = await get_database()
        cursor = db[self.collection_name].find({
            "companyId": company_id,
            "skillsetCategory": category
        })
        return [self._format_skillset(s) async for s in cursor]

    async def get_by_name(self, company_id: str, name: str) -> List[Dict[str, Any]]:
        """Get skillsets by name"""
        db = await get_database()
        cursor = db[self.collection_name].find({
            "companyId": company_id,
            "skillsetName": name
        })
        return [self._format_skillset(s) async for s in cursor]

    async def get_by_rating(self, company_id: str, rating: int) -> List[Dict[str, Any]]:
        """Get skillsets by rating"""
        db = await get_database()
        cursor = db[self.collection_name].find({
            "companyId": company_id,
            "skillsetRating": rating
        })
        return [self._format_skillset(s) async for s in cursor]

    async def get_all(self):
        """Retrieves all skillsets from the database."""
        db = await get_database()
        results = await db[self.collection_name].find({}).to_list(None)
        return [self._format_skillset(s) for s in results]

    def _format_skillset(self, skillset: Dict[str, Any]) -> Dict[str, Any]:
        """Format MongoDB document"""
        skillset["id"] = str(skillset.pop("_id"))
        return skillset 