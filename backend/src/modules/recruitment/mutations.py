import strawberry
from typing import Optional
from datetime import datetime
from .schemas import Recruitment, CreateRecruitmentProcessInput, UpdateRecruitmentProcessInput, JobDetailInput
from .repository import RecruitmentRepository

@strawberry.type
class RecruitmentMutations:
    @strawberry.mutation
    async def create_recruitment_process(self, input: CreateRecruitmentProcessInput) -> Recruitment:
        """Create a new recruitment process"""
        repo = RecruitmentRepository()
        recruitment_data = {
            **input.__dict__,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await repo.create_recruitment(recruitment_data)
        if isinstance(result, dict):
            result['id'] = str(result.pop('_id'))
            return Recruitment(**result)
        return None

    @strawberry.mutation
    async def update_recruitment_process(self, id: str, input: UpdateRecruitmentProcessInput) -> Optional[Recruitment]:
        """Update an existing recruitment process"""
        repo = RecruitmentRepository()
        update_data = {
            k: v for k, v in input.__dict__.items() 
            if v is not None
        }
        
        result = await repo.update_recruitment(id, update_data)
        if not result:
            return None
        
        result.pop('_id', None)
        result.pop('id', None)
        result.pop('updatedAt', None)
        
        return Recruitment(
            id=id,
            **result,
            updatedAt=datetime.utcnow()
        )

    @strawberry.mutation
    async def delete_recruitment_process(self, id: str) -> bool:
        """Delete a recruitment process"""
        repo = RecruitmentRepository()
        return await repo.delete_recruitment(id)

    @strawberry.mutation
    async def add_job_details(self, id: str, category: str, description: str) -> Optional[Recruitment]:
        """Add job details to a recruitment process"""
        repo = RecruitmentRepository()
        result = await repo.get_recruitment_by_id(id)
        if not result:
            return None
            
        job_details = result.get("jobDetailsArray", [])
        job_details.append({"category": category, "description": description})
        
        updated_recruitment = await repo.update_job_details(id, job_details)
        if updated_recruitment:
            updated_recruitment.pop('_id', None)
            updated_recruitment.pop('id', None)
            updated_recruitment.pop('updatedAt', None)
            return Recruitment(
                id=id,
                **updated_recruitment,
                updatedAt=datetime.utcnow()
            )
        return None

    @strawberry.mutation
    async def delete_job_details(self, id: str, category: str) -> Optional[Recruitment]:
        """Delete job details from a recruitment process"""
        repo = RecruitmentRepository()
        result = await repo.get_recruitment_by_id(id)
        if not result:
            return None
            
        job_details = result.get("jobDetailsArray", [])
        # Filter out the job detail with the specified category
        updated_job_details = [jd for jd in job_details if jd["category"] != category]
        
        updated_recruitment = await repo.update_job_details(id, updated_job_details)
        if updated_recruitment:
            updated_recruitment.pop('_id', None)
            updated_recruitment.pop('id', None)
            updated_recruitment.pop('updatedAt', None)
            return Recruitment(
                id=id,
                **updated_recruitment,
                updatedAt=datetime.utcnow()
            )
        return None

    @strawberry.mutation
    async def update_job_details(self, id: str, category: str, description: str) -> Optional[Recruitment]:
        """Update job details in a recruitment process"""
        repo = RecruitmentRepository()
        result = await repo.get_recruitment_by_id(id)
        if not result:
            return None
            
        job_details = result.get("jobDetailsArray", [])
        # Update the description for the matching category
        updated_job_details = [
            {**jd, "description": description} if jd["category"] == category else jd
            for jd in job_details
        ]
        
        updated_recruitment = await repo.update_job_details(id, updated_job_details)
        if updated_recruitment:
            updated_recruitment.pop('_id', None)
            updated_recruitment.pop('id', None)
            updated_recruitment.pop('updatedAt', None)
            return Recruitment(
                id=id,
                **updated_recruitment,
                updatedAt=datetime.utcnow()
            )
        return None