from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class InterviewRepository:
    def __init__(self):
        self.collection_name = "interviews"

    async def create_interview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new interview entry"""
        db = await get_database()
        interview_doc = {
            **data,
            "createdAt": datetime.utcnow()
        }
        result = await db[self.collection_name].insert_one(interview_doc)
        interview_doc["id"] = str(result.inserted_id)
        return interview_doc

    async def update_interview(self, interview_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing interview"""
        db = await get_database()
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(interview_id)},
            {"$set": data},
            return_document=True
        )
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def delete_interview(self, interview_id: str) -> bool:
        """Delete interview entry"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(interview_id)})
        return result.deleted_count > 0

    async def get_by_candidate_email(self, email: str) -> List[Dict[str, Any]]:
        """Get interviews by candidate email"""
        db = await get_database()
        cursor = db[self.collection_name].find({"email": email})
        return [self._format_interview(doc) async for doc in cursor]

    async def get_by_company_id(self, company_id: str) -> List[Dict[str, Any]]:
        """Get interviews by company ID"""
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        return [self._format_interview(doc) async for doc in cursor]

    async def get_by_interviewer_email(self, email: str) -> List[Dict[str, Any]]:
        """Get interviews by interviewer email"""
        db = await get_database()
        cursor = db[self.collection_name].find({"interviewerEmail": email})
        return [self._format_interview(doc) async for doc in cursor]

    def _format_interview(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Format MongoDB document"""
        doc["id"] = str(doc.pop("_id"))
        return doc 