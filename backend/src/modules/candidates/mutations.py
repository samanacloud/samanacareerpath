import strawberry
from typing import Optional
from datetime import datetime
from .schemas import Candidate, CreateCandidateInput, UpdateCandidateInput, EnrollCandidateInput
from .repository import CandidateRepository

@strawberry.type
class CandidateMutations:
    @strawberry.mutation
    async def create_candidate(self, input: CreateCandidateInput) -> Candidate:
        """Create a new candidate"""
        repo = CandidateRepository()
        candidate_data = {
            **input.__dict__,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = await repo.create_candidate(candidate_data)
        if isinstance(result, dict):
            result['id'] = str(result.pop('_id'))
            return Candidate(**result)
        return None

    @strawberry.mutation
    async def update_candidate(self, id: str, input: UpdateCandidateInput) -> Optional[Candidate]:
        """Update an existing candidate"""
        repo = CandidateRepository()
        update_data = {
            k: v for k, v in input.__dict__.items() 
            if v is not None
        }
        
        result = await repo.update_candidate(id, update_data)
        if not result:
            return None
        
        result.pop('_id', None)
        result.pop('id', None)
        result.pop('updatedAt', None)
        
        return Candidate(
            id=id,
            **result,
            updatedAt=datetime.utcnow()
        )

    @strawberry.mutation
    async def delete_candidate(self, id: str) -> bool:
        """Delete a candidate"""
        repo = CandidateRepository()
        return await repo.delete_candidate(id)

    @strawberry.mutation
    async def enroll_candidate(self, input: EnrollCandidateInput) -> Optional[Candidate]:
        """Enroll a candidate in a recruitment process"""
        repo = CandidateRepository()
        update_data = {
            "recruitmentProcessId": input.recruitmentProcessId,
            "recruitmentProcessName": input.recruitmentProcessName,
            "updatedAt": datetime.utcnow()
        }
        
        result = await repo.update_candidate(input.id, update_data)
        if not result:
            return None
        
        result.pop('_id', None)
        result.pop('id', None)
        result.pop('updatedAt', None)
        
        return Candidate(
            id=input.id,
            **result,
            updatedAt=datetime.utcnow()
        ) 