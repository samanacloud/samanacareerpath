import strawberry
from typing import List, Optional
from .schemas import Recruitment, JobDetailsArray
from .repository import RecruitmentRepository, get_job_details_by_id

@strawberry.type
class RecruitmentQueries:
    @strawberry.field
    async def get_recruitment_process_by_company_id(self, companyId: str) -> List[Recruitment]:
        """Get all recruitment processes for a specific company"""
        repo = RecruitmentRepository()
        results = await repo.get_recruitment_by_company_id(companyId)
        return [Recruitment(**recruitment) for recruitment in results]

    @strawberry.field
    async def get_recruitment_process_by_id(self, id: str) -> Optional[Recruitment]:
        """Get a recruitment process by ID"""
        repo = RecruitmentRepository()
        result = await repo.get_recruitment_by_id(id)
        return Recruitment(**result) if result else None

    @strawberry.field
    async def getJobDetailsById(self, id: str) -> List[JobDetailsArray]:
        job_details = await get_job_details_by_id(id)
        return [JobDetailsArray(category=detail.get('category', ''), description=detail.get('description', '')) for detail in job_details] 