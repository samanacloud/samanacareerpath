import strawberry
from typing import List, Optional
from .schemas import Employee
from .repository import EmployeeRepository

@strawberry.type
class EmployeeQueries:
    @strawberry.field
    async def employee(self, id: str) -> Optional[Employee]:
        """Get an employee by ID"""
        repo = EmployeeRepository()
        result = await repo.get_employee(id)
        return Employee(**result) if result else None

    @strawberry.field
    async def employees_by_company(self, company_id: str) -> List[Employee]:
        """Get all employees for a specific company"""
        repo = EmployeeRepository()
        results = await repo.get_employees_by_company(company_id)
        return [Employee(**employee) for employee in results]

    @strawberry.field
    async def employee_by_email(self, email: str) -> Optional[Employee]:
        """Get an employee by email"""
        repo = EmployeeRepository()
        result = await repo.get_employee_by_email(email)
        return Employee(**result) if result else None 