import strawberry
from typing import List, Optional
from .schemas import User
from .repository import UserRepository

@strawberry.type
class UserQueries:
    @strawberry.field
    async def user(self, id: str) -> Optional[User]:
        """Get a user by ID"""
        repo = UserRepository()
        result = await repo.get_user(id)
        return User(**result) if result else None

    @strawberry.field
    async def users_by_company(self, company_id: str) -> List[User]:
        """Get all users for a specific company"""
        repo = UserRepository()
        results = await repo.get_users_by_company(company_id)
        return [User(**user) for user in results]

    @strawberry.field
    async def user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        repo = UserRepository()
        result = await repo.get_user_by_email(email)
        return User(**result) if result else None

    @strawberry.field
    async def listUsersByCompany(self, companyId: str) -> List[User]:
        """List all users for a company"""
        users = await UserRepository.list_users_by_company(companyId)
        return [User(**user) for user in users] 