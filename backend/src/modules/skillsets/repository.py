from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class SkillsetRepository:
    def __init__(self):
        self.collectionName = "skillsets"

    async def _get_db(self):
        """Get database connection"""
        return await get_database()

    def _format_skillset(self, skillset: Dict[str, Any]) -> Dict[str, Any]:
        """Format skillset document by converting _id to id"""
        if skillset:
            skillset["id"] = str(skillset.pop("_id"))
            return skillset
        return None

    async def create_skillset(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new skillset"""
        db = await self._get_db()
        skillsetDoc = {
            "companyId": data["companyId"],
            "skillsetCategory": data["skillsetCategory"],
            "skillsetName": data["skillsetName"],
            "skillsetDescription": data["skillsetDescription"]
        }
        result = await db[self.collectionName].insert_one(skillsetDoc)
        createdDoc = await db[self.collectionName].find_one({"_id": result.inserted_id})
        return self._format_skillset(createdDoc)

    async def get_skillset_by_id(self, skillsetId: str, companyId: str) -> Optional[Dict[str, Any]]:
        """Get a skillset by ID and company ID"""
        db = await self._get_db()
        result = await db[self.collectionName].find_one({
            "_id": ObjectId(skillsetId),
            "companyId": companyId
        })
        return self._format_skillset(result)

    async def get_all_skillsets(self, companyId: str) -> List[Dict[str, Any]]:
        """Get all skillsets for a company"""
        db = await self._get_db()
        cursor = db[self.collectionName].find({"companyId": companyId})
        skillsets = []
        async for doc in cursor:
            skillsets.append(self._format_skillset(doc))
        return skillsets

    async def get_skillsets_by_category(self, companyId: str, skillsetCategory: str) -> List[Dict[str, Any]]:
        """Get all skillsets in a specific category for a company"""
        db = await self._get_db()
        cursor = db[self.collectionName].find({
            "companyId": companyId,
            "skillsetCategory": skillsetCategory
        })
        skillsets = []
        async for doc in cursor:
            skillsets.append(self._format_skillset(doc))
        return skillsets

    async def update_skillset(self, skillsetId: str, companyId: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a skillset"""
        db = await self._get_db()
        updateData = {k: v for k, v in data.items() if v is not None and k != "companyId"}
        if not updateData:
            return None

        result = await db[self.collectionName].find_one_and_update(
            {
                "_id": ObjectId(skillsetId),
                "companyId": companyId
            },
            {"$set": updateData},
            return_document=True
        )
        return self._format_skillset(result)

    async def delete_skillset(self, skillsetId: str, companyId: str) -> bool:
        """Delete a skillset"""
        db = await self._get_db()
        result = await db[self.collectionName].delete_one({
            "_id": ObjectId(skillsetId),
            "companyId": companyId
        })
        return result.deleted_count > 0 