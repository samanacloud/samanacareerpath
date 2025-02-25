import strawberry
from typing import List
from .schemas import Interview
from .repository import InterviewRepository

@strawberry.type
class InterviewQueries:
    @strawberry.field
    async def get_interviews(self, email: str) -> List[Interview]:
        """Get interviews by candidate email"""
        repo = InterviewRepository()
        results = await repo.get_by_candidate_email(email)
        return [Interview(**interview) for interview in results]

    @strawberry.field
    async def get_interviews_by_company_id(self, company_id: str) -> List[Interview]:
        """Get interviews by company ID"""
        repo = InterviewRepository()
        results = await repo.get_by_company_id(company_id)
        return [Interview(**interview) for interview in results]

    @strawberry.field
    async def get_interviews_by_interviewer_email(self, interviewer_email: str) -> List[Interview]:
        """Get interviews by interviewer email"""
        repo = InterviewRepository()
        results = await repo.get_by_interviewer_email(interviewer_email)
        return [Interview(**interview) for interview in results]

    @strawberry.field
    async def getInterviewsByEmail(self, email: str) -> List[Interview]:
        """Get interviews by candidate email"""
        repo = InterviewRepository()
        results = await repo.get_by_candidate_email(email)
        return [Interview(**interview) for interview in results] 