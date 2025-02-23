from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database
import logging

class RecruitmentRepository:
    def __init__(self):
        self.collection_name = "recruitment"

    async def create_recruitment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        db = await get_database()
        
        recruitment_doc = {
            "companyId": data["companyId"],
            "companyName": data["companyName"],
            "jobCategory": data["jobCategory"],
            "jobName": data["jobName"],
            "jobDetails": data["jobDetails"],
            "workplaceType": data["workplaceType"],
            "jobType": data["jobType"],
            "salaryRange": data["salaryRange"],
            "postUrl": data["postUrl"],
            "status": data.get("status", "active"),
            "createdAt": datetime.utcnow(),
            "createdBy": data["createdBy"],
            "updatedAt": datetime.utcnow(),
            "updatedBy": data["updatedBy"],
            "jobDetailsArray": data.get("jobDetailsArray", [])
        }
        
        result = await db[self.collection_name].insert_one(recruitment_doc)
        recruitment_doc["id"] = str(result.inserted_id)
        return recruitment_doc

    async def update_recruitment(self, recruitment_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = await get_database()
        
        update_doc = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        if "updatedBy" in data:
            update_doc["updatedBy"] = data["updatedBy"]
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(recruitment_id)},
            {"$set": update_doc},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_recruitment_by_id(self, recruitment_id: str) -> Optional[Dict[str, Any]]:
        db = await get_database()
        result = await db[self.collection_name].find_one({"_id": ObjectId(recruitment_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_recruitment_by_company_id(self, company_id: str) -> List[Dict[str, Any]]:
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        recruitments = []
        async for recruitment in cursor:
            recruitment["id"] = str(recruitment.pop("_id"))
            recruitments.append(recruitment)
        return recruitments

    async def delete_recruitment(self, recruitment_id: str) -> bool:
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(recruitment_id)})
        return result.deleted_count > 0

    async def update_job_details(self, recruitment_id: str, job_details: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        db = await get_database()
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(recruitment_id)},
            {"$set": {"jobDetailsArray": job_details}},
            return_document=True
        )
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_job_details_by_id(self, id: str):
        try:
            oid = ObjectId(id)
        except Exception as e:
            logging.error(f"Invalid id format: {id} - {e}")
            return []
        db = await get_database()
        document = await db[self.collection_name].find_one(
            {"_id": oid},
            {"jobDetailsArray": 1, "_id": 0}
        )
        if document and document.get("jobDetailsArray"):
            return document["jobDetailsArray"]
        return []

# Module-level function to expose get_job_details_by_id from RecruitmentRepository
async def get_job_details_by_id(id: str):
    repo = RecruitmentRepository()
    return await repo.get_job_details_by_id(id) 