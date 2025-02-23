import strawberry
from typing import Optional
from .schemas import CertificationInput, UpdateCertificationInput, CertificationMutationResponse, Certification
from .repository import CertificationRepository

@strawberry.type
class CertificationMutations:
    @strawberry.mutation
    async def create_certification(
        self,
        data: CertificationInput
    ) -> CertificationMutationResponse:
        """Create a new certification"""
        try:
            repository = CertificationRepository()
            result = await repository.create_certification(data.__dict__)
            
            if result:
                return CertificationMutationResponse(
                    status="success",
                    message="Certification created successfully",
                    certification=Certification(**result)
                )
            return CertificationMutationResponse(
                status="error",
                error="Failed to create certification"
            )
        except Exception as e:
            return CertificationMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.mutation
    async def update_certification(
        self,
        data: UpdateCertificationInput
    ) -> CertificationMutationResponse:
        """Update an existing certification"""
        try:
            repository = CertificationRepository()
            result = await repository.update_certification(
                data.id,
                data.companyId,
                data.__dict__
            )
            
            if result:
                return CertificationMutationResponse(
                    status="success",
                    message="Certification updated successfully",
                    certification=Certification(**result)
                )
            return CertificationMutationResponse(
                status="error",
                error="Certification not found or no changes made"
            )
        except Exception as e:
            return CertificationMutationResponse(
                status="error",
                error=str(e)
            )

    @strawberry.mutation
    async def delete_certification(
        self,
        certificationId: str,
        companyId: str
    ) -> CertificationMutationResponse:
        """Delete a certification"""
        try:
            repository = CertificationRepository()
            result = await repository.delete_certification(certificationId, companyId)
            
            if result:
                return CertificationMutationResponse(
                    status="success",
                    message="Certification deleted successfully"
                )
            return CertificationMutationResponse(
                status="error",
                error="Certification not found"
            )
        except Exception as e:
            return CertificationMutationResponse(
                status="error",
                error=str(e)
            ) 