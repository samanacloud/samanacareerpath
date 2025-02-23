from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_database

class EmployeeRepository:
    def __init__(self):
        self.collection_name = "employees"

    async def create_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new employee"""
        db = await get_database()
        
        employee_doc = {
            "companyId": data["companyId"],
            "companyName": data["companyName"],
            "name": data["name"],
            "email": data["email"],
            "country": data["country"],
            "role": data.get("role", "employee"),
            "phone": data["phone"],
            "status": data.get("status", "active"),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        result = await db[self.collection_name].insert_one(employee_doc)
        employee_doc["id"] = str(result.inserted_id)
        return employee_doc

    async def update_employee(self, employee_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an employee by ID"""
        db = await get_database()
        
        update_doc = {
            "updatedAt": datetime.utcnow(),
            **{k: v for k, v in data.items() if v is not None}
        }
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(employee_id)},
            {"$set": update_doc},
            return_document=True
        )
        
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get an employee by ID"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"_id": ObjectId(employee_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None

    async def get_employees_by_company(self, company_id: str) -> List[Dict[str, Any]]:
        """Get all employees for a specific company"""
        db = await get_database()
        cursor = db[self.collection_name].find({"companyId": company_id})
        employees = []
        async for employee in cursor:
            employee["id"] = str(employee.pop("_id"))
            employees.append(employee)
        return employees

    async def delete_employee(self, employee_id: str) -> bool:
        """Delete an employee by ID"""
        db = await get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(employee_id)})
        return result.deleted_count > 0

    async def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get an employee by email"""
        db = await get_database()
        result = await db[self.collection_name].find_one({"email": email})
        if result:
            result["id"] = str(result.pop("_id"))
            return result
        return None 