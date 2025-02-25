import strawberry
from typing import List
from .schemas import CertificationData
from .repository import CertificationDataRepository

@strawberry.type
class CertificationDataQueries:
    @strawberry.field
    async def get_assigned_certifications_by_email(self, email: str) -> List[CertificationData]:
        """Get certifications by email"""
        repo = CertificationDataRepository()
        results = await repo.get_by_email(email)
        return [CertificationData(**cert) for cert in results]

    @strawberry.field
    async def get_assigned_certifications_by_company_id(self, company_id: str, domain: str) -> List[CertificationData]:
        """Get certifications by company and domain"""
        repo = CertificationDataRepository()
        results = await repo.get_by_company_and_domain(company_id, domain)
        return [CertificationData(**cert) for cert in results] 