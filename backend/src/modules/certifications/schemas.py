from typing import Optional, List
import strawberry

@strawberry.type
class Certification:
    id: str = strawberry.field(description="Certification ID")
    companyId: str = strawberry.field(description="Company ID")
    certificationVendor: str = strawberry.field(description="Certification vendor (e.g., AWS, Microsoft)")
    certificationName: str = strawberry.field(description="Name of the certification")
    certificationShortName: str = strawberry.field(description="Short name/code of the certification")

@strawberry.type
class CertificationMutationResponse:
    status: str = strawberry.field(description="Operation status (success/error)")
    message: Optional[str] = strawberry.field(description="Response message", default=None)
    error: Optional[str] = strawberry.field(description="Error message if any", default=None)
    certification: Optional[Certification] = strawberry.field(description="Single certification response", default=None)
    certifications: List[Certification] = strawberry.field(description="List of certifications", default_factory=list)

@strawberry.input
class CertificationInput:
    companyId: str = strawberry.field(description="Company ID")
    certificationVendor: str = strawberry.field(description="Certification vendor (e.g., AWS, Microsoft)")
    certificationName: str = strawberry.field(description="Name of the certification")
    certificationShortName: str = strawberry.field(description="Short name/code of the certification")

@strawberry.input
class UpdateCertificationInput:
    id: str = strawberry.field(description="ID of the certification to update")
    companyId: str = strawberry.field(description="Company ID")
    certificationVendor: Optional[str] = strawberry.field(description="Certification vendor (e.g., AWS, Microsoft)", default=None)
    certificationName: Optional[str] = strawberry.field(description="Name of the certification", default=None)
    certificationShortName: Optional[str] = strawberry.field(description="Short name/code of the certification", default=None) 