import strawberry
from typing import Optional
from datetime import datetime
from .schemas import User, CreateUserInput, UpdateUserInput
from .repository import UserRepository

@strawberry.type
class UserMutations:
    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> User:
        """Create a new user"""
        repo = UserRepository()
        user_data = {
            **input.__dict__,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await repo.create_user(user_data)
        if isinstance(result, dict):
            # Convert _id to id and remove _id from the result
            result['id'] = str(result.pop('_id'))
            return User(**result)
        return None

    @strawberry.mutation
    async def update_user(self, id: str, input: UpdateUserInput) -> Optional[User]:
        """Update an existing user"""
        repo = UserRepository()
        update_data = {
            k: v for k, v in input.__dict__.items() 
            if v is not None
        }
        
        result = await repo.update_user(id, update_data)
        if not result:
            return None
        
        # Remove duplicate fields
        result.pop('_id', None)
        result.pop('id', None)
        result.pop('updatedAt', None)
        
        return User(
            id=id,
            **result,
            updatedAt=datetime.utcnow()
        )

    @strawberry.mutation
    async def delete_user(self, id: str) -> bool:
        """Delete a user"""
        repo = UserRepository()
        return await repo.delete_user(id) 