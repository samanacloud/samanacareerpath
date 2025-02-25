import strawberry
from typing import List
from .schemas import SkillsetData
from .repository import SkillsetDataRepository

@strawberry.type
class SkillsetDataQueries:
    @strawberry.field
    async def get_skillsets_by_email(self, email: str) -> List[SkillsetData]:
        """Get skillsets by user email (case-insensitive)"""
        repo = SkillsetDataRepository()
        results = await repo.get_by_email(email.lower())
        return [SkillsetData(**s) for s in results]

    @strawberry.field
    async def get_skillsets_by_category(self, company_id: str, skillset_category: str) -> List[SkillsetData]:
        """Get skillsets by category"""
        repo = SkillsetDataRepository()
        results = await repo.get_by_category(company_id, skillset_category)
        return [SkillsetData(**s) for s in results]

    @strawberry.field
    async def get_skillsets_by_name(self, company_id: str, skillset_name: str) -> List[SkillsetData]:
        """Get skillsets by name"""
        repo = SkillsetDataRepository()
        results = await repo.get_by_name(company_id, skillset_name)
        return [SkillsetData(**s) for s in results]

    @strawberry.field
    async def get_skillsets_by_rating(self, company_id: str, skillset_rating: int) -> List[SkillsetData]:
        """Get skillsets by rating"""
        repo = SkillsetDataRepository()
        results = await repo.get_by_rating(company_id, skillset_rating)
        return [SkillsetData(**s) for s in results]

    @strawberry.field
    async def get_all_skillsets(self) -> List[SkillsetData]:
        """Get all skillsets"""
        repo = SkillsetDataRepository()
        results = await repo.get_all()
        return [SkillsetData(**s) for s in results] 