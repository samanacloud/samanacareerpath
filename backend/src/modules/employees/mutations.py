import strawberry
from typing import Optional
from datetime import datetime
from .schemas import Employee, CreateEmployeeInput, UpdateEmployeeInput
from .repository import EmployeeRepository

@strawberry.type
class EmployeeMutations:
    @strawberry.mutation
    async def create_employee(self, input: CreateEmployeeInput) -> Employee:
        """Create a new employee"""
        repo = EmployeeRepository()
        employee_data = {
            **input.__dict__,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await repo.create_employee(employee_data)
        if isinstance(result, dict):
            result['id'] = str(result.pop('_id'))
            return Employee(**result)
        return None

    @strawberry.mutation
    async def update_employee(self, id: str, input: UpdateEmployeeInput) -> Optional[Employee]:
        """Update an existing employee"""
        repo = EmployeeRepository()
        update_data = {
            k: v for k, v in input.__dict__.items() 
            if v is not None
        }
        
        result = await repo.update_employee(id, update_data)
        if not result:
            return None
        
        result.pop('_id', None)
        result.pop('id', None)
        result.pop('updatedAt', None)
        
        return Employee(
            id=id,
            **result,
            updatedAt=datetime.utcnow()
        )

    @strawberry.mutation
    async def delete_employee(self, id: str) -> bool:
        """Delete an employee"""
        repo = EmployeeRepository()
        return await repo.delete_employee(id) 