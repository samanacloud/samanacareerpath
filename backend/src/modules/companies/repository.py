from database import db
from bson import ObjectId
from typing import Dict, Any
from datetime import datetime

class CompanyRepository:
    collection = db.companies

    @classmethod
    def _clean_company_data(cls, company: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB _id to string id"""
        if company:
            company["id"] = str(company.pop("_id"))
        return company

    @classmethod
    async def get_company_info(cls, company_id: str) -> Dict[str, Any]:
        """Get company information by ID"""
        try:
            company = await cls.collection.find_one({"_id": ObjectId(company_id)})
            if not company:
                return None
            return cls._clean_company_data(company)
        except Exception as e:
            raise Exception(f"Failed to fetch company info: {str(e)}")

    @classmethod
    async def update_company(cls, company_id: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update company information"""
        try:
            company_data["updatedAt"] = datetime.utcnow()
            result = await cls.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": company_data}
            )
            
            if result.modified_count:
                updated_company = await cls.collection.find_one({"_id": ObjectId(company_id)})
                return cls._clean_company_data(updated_company)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to update company: {str(e)}") 