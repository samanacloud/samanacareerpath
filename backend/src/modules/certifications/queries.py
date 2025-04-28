from typing import List, Optional
import strawberry
from .schemas import Certification
from .repository import CertificationRepository

@strawberry.type
class CertificationQueries:
    @strawberry.field
    async def get_certification_by_id(
        self, 
        certificationId: str,
        companyId: str
    ) -> Optional[Certification]:
        """Get a certification by ID"""
        repository = CertificationRepository()
        result = await repository.get_certification_by_id(certificationId, companyId)
        if result:
            return Certification(**result)
        return None

    @strawberry.field
    async def get_all_certifications(
        self,
        companyId: str
    ) -> List[Certification]:
        """Get all certifications for a company"""
        repository = CertificationRepository()
        results = await repository.get_all_certifications(companyId)
        return [Certification(**cert) for cert in results]

    @strawberry.field
    async def get_certifications_by_vendor(
        self,
        companyId: str,
        certificationVendor: str
    ) -> List[Certification]:
        """Get all certifications from a specific vendor for a company"""
        repository = CertificationRepository()
        results = await repository.get_certifications_by_vendor(companyId, certificationVendor)
        return [Certification(**cert) for cert in results]

    @strawberry.field
    async def get_certification_vendors(
        self,
        companyId: str
    ) -> List[str]:
        """Get all unique certification vendors for a company"""
        repository = CertificationRepository()
        return await repository.get_certification_vendors(companyId)

    @strawberry.field
    async def get_certifications_by_company_id(
        self,
        companyId: str
    ) -> List[Certification]:
        """Get all certifications for a specific company"""
        repository = CertificationRepository()
        results = await repository.get_certifications_by_company_id(companyId)
        return [Certification(**cert) for cert in results]