import strawberry
from typing import List, Optional
from .schemas import Candidate
from .repository import CandidateRepository

@strawberry.type
class CandidateQueries:
    @strawberry.field
    async def candidate(self, id: str) -> Optional[Candidate]:
        """Get a candidate by ID"""
        repo = CandidateRepository()
        result = await repo.get_candidate(id)
        return Candidate(**result) if result else None

    @strawberry.field
    async def candidate_by_email(self, email: str) -> Optional[Candidate]:
        """Get a candidate by email"""
        repo = CandidateRepository()
        result = await repo.get_candidate_by_email(email)
        return Candidate(**result) if result else None

    @strawberry.field
    async def candidates_by_company_id(self, company_id: str) -> List[Candidate]:
        """Get all candidates for a specific company"""
        repo = CandidateRepository()
        results = await repo.get_candidates_by_company_id(company_id)
        return [Candidate(**candidate) for candidate in results]

    @strawberry.field
    async def candidates_by_recruitment_process_id(self, recruitment_process_id: str) -> List[Candidate]:
        """Get all candidates for a specific recruitment process"""
        repo = CandidateRepository()
        results = await repo.get_candidates_by_recruitment_process_id(recruitment_process_id)
        return [Candidate(**candidate) for candidate in results] 