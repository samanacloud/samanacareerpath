from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class CandidateRepository:
    def __init__(self):
        self.collection_name = "candidates"

    async def create_candidate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new candidate"""
        db = await get_database()
        
        candidate_doc = {
            "companyId": data["companyId"],
            "companyName": data["companyName"],
            "recruitmentProcessId": data["recruitmentProcessId"],
            "recruitmentProcessName": data["recruitmentProcessName"],
            "candidateName": data["candidateName"],
            "email": data["email"],
            "country": data["country"],
            "phone": data["phone"],
            "candidateCV": data["candidateCV"],
            "status": data.get("status", "active"),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        result = await db[self.collection_name].insert_one(candidate_doc)
        candidate_doc["id"] = str(result.inserted_id)
        return candidate_doc

    async def update_candidate(self, candidate_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a candidate by ID"""
        db = await get_database()
        
        update_doc = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_doc},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """Get a candidate by ID"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"_id": ObjectId(candidate_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_candidate_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a candidate by email"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"email": email})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_candidates_by_company_id(self, company_id: str) -> List[Dict[str, Any]]:
        """Get all candidates for a specific company"""
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        candidates = []
        async for candidate in cursor:
            candidate["id"] = str(candidate.pop("_id"))
            candidates.append(candidate)
        return candidates

    async def get_candidates_by_recruitment_process_id(self, recruitment_process_id: str) -> List[Dict[str, Any]]:
        """Get all candidates for a specific recruitment process"""
        db = await get_database()
        cursor = db[self.collection_name].find({"recruitmentProcessId": recruitment_process_id})
        candidates = []
        async for candidate in cursor:
            candidate["id"] = str(candidate.pop("_id"))
            candidates.append(candidate)
        return candidates

    async def delete_candidate(self, candidate_id: str) -> bool:
        """Delete a candidate by ID"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(candidate_id)})
        return result.deleted_count > 0 