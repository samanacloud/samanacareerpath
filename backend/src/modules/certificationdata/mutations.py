import strawberry
from typing import Optional
from .schemas import CertificationData, AssignCertificationInput, UpdateCertificationInput
from .repository import CertificationDataRepository

@strawberry.type
class CertificationDataMutations:
    @strawberry.mutation
    async def assign_certification(self, input: AssignCertificationInput) -> Optional[CertificationData]:
        """Assign new certification to user"""
        repo = CertificationDataRepository()
        result = await repo.create_certification(input.__dict__)
        return CertificationData(**result) if result else None

    @strawberry.mutation
    async def update_certification(self, id: str, input: UpdateCertificationInput) -> Optional[CertificationData]:
        """Update existing certification"""
        repo = CertificationDataRepository()
        result = await repo.update_certification(id, input.__dict__)
        return CertificationData(**result) if result else None

    @strawberry.mutation
    async def remove_certification(self, id: str) -> bool:
        """Delete certification entry"""
        repo = CertificationDataRepository()
        return await repo.delete_certification(id) 