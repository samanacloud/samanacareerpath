import strawberry
from typing import List
from .schemas import Skillset
from .repository import SkillsetRepository

@strawberry.type
class SkillsetQueries:
    @strawberry.field
    async def listSkillsetsByCompanyId(self, companyId: str) -> List[Skillset]:
        """List all skillsets for a company"""
        repo = SkillsetRepository()
        results = await repo.get_skillsets_by_company(companyId)
        return [Skillset(**skillset) for skillset in results]

    @strawberry.field
    async def listSkillsetsCategories(self, companyId: str) -> List[str]:
        """List distinct skillset categories for a company"""
        repo = SkillsetRepository()
        return await repo.get_skillset_categories(companyId) 