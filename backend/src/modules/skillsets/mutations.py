import strawberry
from typing import Optional
from .schemas import Skillset, SkillsetMutationResponse, SkillsetInput, UpdateSkillsetInput
from .repository import SkillsetRepository

@strawberry.type
class SkillsetMutations:
    @strawberry.mutation
    async def create_skillset(self, input: SkillsetInput) -> SkillsetMutationResponse:
        """Create a new skillset"""
        repo = SkillsetRepository()
        try:
            skillset = await repo.create_skillset({
                "companyId": input.companyId,
                "skillsetCategory": input.skillsetCategory,
                "skillsetName": input.skillsetName,
                "skillsetDescription": input.skillsetDescription
            })
            return SkillsetMutationResponse(
                status="success",
                skillset=skillset,
                message="Skillset created successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.mutation
    async def update_skillset(self, input: UpdateSkillsetInput) -> SkillsetMutationResponse:
        """Update an existing skillset"""
        repo = SkillsetRepository()
        try:
            updateData = {
                "skillsetCategory": input.skillsetCategory,
                "skillsetName": input.skillsetName,
                "skillsetDescription": input.skillsetDescription
            }
            # Remove None values
            updateData = {k: v for k, v in updateData.items() if v is not None}
            
            skillset = await repo.update_skillset(input.id, input.companyId, updateData)
            if not skillset:
                return SkillsetMutationResponse(
                    status="error",
                    error="Skillset not found or no changes provided"
                )
            
            return SkillsetMutationResponse(
                status="success",
                skillset=skillset,
                message="Skillset updated successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.mutation
    async def delete_skillset(self, id: str, companyId: str) -> SkillsetMutationResponse:
        """Delete a skillset"""
        repo = SkillsetRepository()
        try:
            success = await repo.delete_skillset(id, companyId)
            if not success:
                return SkillsetMutationResponse(
                    status="error",
                    error="Skillset not found"
                )
            
            return SkillsetMutationResponse(
                status="success",
                message="Skillset deleted successfully"
            )
        except Exception as e:
            return SkillsetMutationResponse(
                status="error",
                error=str(e)
            ) 