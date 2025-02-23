from typing import Optional, List
import strawberry

@strawberry.type
class Skillset:
    id: str = strawberry.field(description="Skillset ID")
    companyId: str = strawberry.field(description="Company ID")
    skillsetCategory: str = strawberry.field(description="Category of the skillset")
    skillsetName: str = strawberry.field(description="Name of the skillset")
    skillsetDescription: str = strawberry.field(description="Description of the skillset")

@strawberry.type
class SkillsetMutationResponse:
    status: str = strawberry.field(description="Operation status (success/error)")
    message: Optional[str] = strawberry.field(description="Response message", default=None)
    error: Optional[str] = strawberry.field(description="Error message if any", default=None)
    skillset: Optional[Skillset] = strawberry.field(description="Single skillset response", default=None)
    skillsets: List[Skillset] = strawberry.field(description="List of skillsets", default_factory=list)

@strawberry.input
class SkillsetInput:
    companyId: str = strawberry.field(description="Company ID")
    skillsetCategory: str = strawberry.field(description="Category of the skillset")
    skillsetName: str = strawberry.field(description="Name of the skillset")
    skillsetDescription: str = strawberry.field(description="Description of the skillset")

@strawberry.input
class UpdateSkillsetInput:
    id: str = strawberry.field(description="ID of the skillset to update")
    companyId: str = strawberry.field(description="Company ID")
    skillsetCategory: Optional[str] = strawberry.field(description="Category of the skillset", default=None)
    skillsetName: Optional[str] = strawberry.field(description="Name of the skillset", default=None)
    skillsetDescription: Optional[str] = strawberry.field(description="Description of the skillset", default=None) 