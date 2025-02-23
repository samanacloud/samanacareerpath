import strawberry
from .schemas import Company, UpdateCompanyInput
from .repository import CompanyRepository

@strawberry.type
class CompanyMutations:
    @strawberry.mutation
    async def update_company_info(self, info, companyId: str, company_data: UpdateCompanyInput) -> Company:
        """Update company information"""
        update_dict = {k: v for k, v in company_data.__dict__.items() if v is not None}
        company = await CompanyRepository.update_company(companyId, update_dict)
        
        if not company:
            raise ValueError(f"Company with id {companyId} not found")
        
        return Company(**company) 