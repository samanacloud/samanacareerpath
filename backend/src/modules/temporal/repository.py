from datetime import datetime
from typing import List, Optional
from database import get_database
from .schemas import TemporalCode, CreateTemporalCodeInput, UpdateTemporalCodeInput
from bson import ObjectId

class TemporalRepository:
    def __init__(self):
        self.collection_name = "temporal"

    async def get_database(self):
        return await get_database()

    async def create(self, data: CreateTemporalCodeInput) -> TemporalCode:
        db = await self.get_database()
        now = datetime.utcnow()
        
        document = {
            "code": data.code,
            "createdAt": now,
            "updatedAt": now
        }
        
        result = await db[self.collection_name].insert_one(document)
        # Create TemporalCode with the correct fields
        return TemporalCode(
            id=str(result.inserted_id),
            code=data.code,
            createdAt=now,
            updatedAt=now
        )

    async def get_all(self) -> List[TemporalCode]:
        db = await self.get_database()
        cursor = db[self.collection_name].find()
        documents = await cursor.to_list(length=None)
        return [
            TemporalCode(
                id=str(doc["_id"]),
                code=doc["code"],
                createdAt=doc["createdAt"],
                updatedAt=doc.get("updatedAt")
            )
            for doc in documents
        ]

    async def get_by_id(self, id: str) -> Optional[TemporalCode]:
        db = await self.get_database()
        try:
            document = await db[self.collection_name].find_one({"_id": ObjectId(id)})
            if document:
                return TemporalCode(
                    id=str(document["_id"]),
                    code=document["code"],
                    createdAt=document["createdAt"],
                    updatedAt=document.get("updatedAt")
                )
        except:
            return None
        return None

    async def update(self, id: str, data: UpdateTemporalCodeInput) -> Optional[TemporalCode]:
        db = await self.get_database()
        update_data = {
            "code": data.code,
            "updatedAt": datetime.utcnow()
        }
        
        try:
            result = await db[self.collection_name].update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_by_id(id)
        except:
            return None
        return None

    async def delete(self, id: str) -> bool:
        db = await self.get_database()
        try:
            result = await db[self.collection_name].delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except:
            return False 