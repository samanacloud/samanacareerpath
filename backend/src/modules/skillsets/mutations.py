import strawberry
from typing import Optional
from datetime import datetime
from .schemas import Skillset, CreateSkillsetInput, UpdateSkillsetInput
from .repository import SkillsetRepository

@strawberry.type
class SkillsetMutations:
    @strawberry.mutation
    async def createSkillset(self, input: CreateSkillsetInput) -> Skillset:
        """Create a new skillset"""
        repo = SkillsetRepository()
        data = input.__dict__
        result = await repo.create_skillset(data)
        return Skillset(**result)

    @strawberry.mutation
    async def modifySkillset(self, id: str, input: UpdateSkillsetInput) -> Optional[Skillset]:
        """Update an existing skillset"""
        repo = SkillsetRepository()
        result = await repo.update_skillset(id, input.__dict__)
        return Skillset(**result) if result else None

    @strawberry.mutation
    async def removeSkillset(self, id: str) -> bool:
        """Delete a skillset"""
        repo = SkillsetRepository()
        return await repo.delete_skillset(id) 