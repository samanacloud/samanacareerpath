import strawberry
from .schemas import Company
from .repository import CompanyRepository

@strawberry.type
class CompanyQueries:
    @strawberry.field
    async def get_company_info(self, info, companyId: str) -> Company:
        """Get company information by companyId"""
        company = await CompanyRepository.get_company_info(companyId)
        if not company:
            raise ValueError(f"Company with id {companyId} not found")
        
        return Company(**company) 