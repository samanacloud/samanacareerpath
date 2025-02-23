import strawberry
from typing import List
from .schemas import Skillset, SkillsetMutationResponse
from .repository import SkillsetRepository

@strawberry.type
class SkillsetQueries:
    @strawberry.field
    async def get_all_skillsets(self, companyId: str) -> SkillsetMutationResponse:
        """Get all skillsets for a company"""
        repo = SkillsetRepository()
        try:
            skillsets = await repo.get_all_skillsets(companyId)
            return SkillsetMutationResponse(
                status="success",
                skillsets=skillsets,
                message="Skillsets retrieved successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.field
    async def get_skillset_by_id(self, id: str, companyId: str) -> SkillsetMutationResponse:
        """Get a skillset by ID for a company"""
        repo = SkillsetRepository()
        try:
            skillset = await repo.get_skillset_by_id(id, companyId)
            if not skillset:
                return SkillsetMutationResponse(
                    status="error",
                    error="Skillset not found"
                )
            return SkillsetMutationResponse(
                status="success",
                skillset=skillset,
                message="Skillset retrieved successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.field
    async def get_skillsets_by_category(self, companyId: str, skillsetCategory: str) -> SkillsetMutationResponse:
        """Get all skillsets in a specific category for a company"""
        repo = SkillsetRepository()
        try:
            skillsets = await repo.get_skillsets_by_category(companyId, skillsetCategory)
            return SkillsetMutationResponse(
                status="success",
                skillsets=skillsets,
                message="Skillsets retrieved successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            ) 