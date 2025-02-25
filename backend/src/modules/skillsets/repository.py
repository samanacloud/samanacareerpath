from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from database import get_database

class SkillsetRepository:
    def __init__(self):
        self.collection_name = "skillsets"

    async def create_skillset(self, data: Dict) -> Dict:
        """Create a new skillset"""
        db = await get_database()
        
        result = await db[self.collection_name].insert_one(data)
        # Fetch the newly created document with proper ID conversion
        inserted_doc = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return self._convert_id(inserted_doc)

    async def update_skillset(self, skillset_id: str, data: Dict) -> Optional[Dict]:
        """Update a skillset by ID"""
        db = await get_database()
        
        update_data = {
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(skillset_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def delete_skillset(self, skillset_id: str) -> bool:
        """Delete a skillset by ID"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(skillset_id)})
        return result.deleted_count > 0

    async def get_skillsets_by_company(self, company_id: str) -> List[Dict]:
        """Get all skillsets for a company"""
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        return [self._convert_id(skillset) async for skillset in cursor]

    async def get_skillset_categories(self, company_id: str) -> List[str]:
        """Get distinct skillset categories for a company"""
        db = await get_database()
        return await db[self.collection_name].distinct(
            "skillsetCategory",
            {"companyId": company_id}
        )

    def _convert_id(self, document: Dict) -> Dict:
        """Convert MongoDB _id to id"""
        document["id"] = str(document.pop("_id"))
        # Remove timestamp fields if they exist
        document.pop("createdAt", None)
        document.pop("updatedAt", None)
        return document 