from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class UserRepository:
    def __init__(self):
        self.collection_name = "users"

    async def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        db = await get_database()
        
        # Prepare user document
        user_doc = {
            "companyId": data["companyId"],
            "companyName": data["companyName"],
            "name": data["name"],
            "email": data["email"],
            "country": data["country"],
            "role": data.get("role", "user"),
            "phone": data["phone"],
            "license": data.get("license", "t0"),
            "status": data.get("status", "active"),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        result = await db[self.collection_name].insert_one(user_doc)
        user_doc["id"] = str(result.inserted_id)
        return user_doc

    async def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a user by ID"""
        db = await get_database()
        
        # Prepare update document
        update_doc = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_doc},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by ID"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"_id": ObjectId(user_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_users_by_company(self, company_id: str) -> List[Dict[str, Any]]:
        """Get all users for a specific company"""
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        users = []
        async for user in cursor:
            user["id"] = str(user.pop("_id"))
            users.append(user)
        return users

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user by ID"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"email": email})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None 