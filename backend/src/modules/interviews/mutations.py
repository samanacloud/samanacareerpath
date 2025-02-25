import strawberry
from typing import Optional
from .schemas import Interview, AddInterviewInput, EditInterviewInput
from .repository import InterviewRepository

@strawberry.type
class InterviewMutations:
    @strawberry.mutation
    async def add_interview(self, input: AddInterviewInput) -> Optional[Interview]:
        """Create new interview entry"""
        repo = InterviewRepository()
        result = await repo.create_interview(input.__dict__)
        return Interview(**result) if result else None

    @strawberry.mutation
    async def edit_interview(self, id: str, input: EditInterviewInput) -> Optional[Interview]:
        """Update existing interview"""
        repo = InterviewRepository()
        update_data = {k: v for k, v in input.__dict__.items() if v is not None}
        result = await repo.update_interview(id, update_data)
        return Interview(**result) if result else None

    @strawberry.mutation
    async def delete_interview(self, id: str) -> bool:
        """Delete interview entry"""
        repo = InterviewRepository()
        return await repo.delete_interview(id) 