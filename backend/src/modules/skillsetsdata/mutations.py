import strawberry
from typing import Optional
from .schemas import SkillsetData, AssignSkillsetInput
from .repository import SkillsetDataRepository

@strawberry.type
class SkillsetDataMutations:
    @strawberry.mutation
    async def assign_skillset(self, input: AssignSkillsetInput) -> Optional[SkillsetData]:
        """Assign new skillset to user"""
        repo = SkillsetDataRepository()
        result = await repo.create_skillset(input.__dict__)
        return SkillsetData(**result) if result else None

    @strawberry.mutation
    async def edit_skillset(self, id: str, skillset_rating: int) -> Optional[SkillsetData]:
        """Update skillset rating"""
        repo = SkillsetDataRepository()
        result = await repo.update_skillset_rating(id, skillset_rating)
        return SkillsetData(**result) if result else None

    @strawberry.mutation
    async def delete_skillset(self, id: str) -> bool:
        """Delete skillset entry"""
        repo = SkillsetDataRepository()
        return await repo.delete_skillset(id) 