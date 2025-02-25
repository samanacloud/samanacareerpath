import strawberry
from datetime import datetime
from typing import Optional

@strawberry.type
class Skillset:
    id: str = strawberry.field(description="Skillset ID", name="id")
    companyId: str = strawberry.field(description="Company ID")
    skillsetCategory: str = strawberry.field(description="Category of the skillset")
    skillsetName: str = strawberry.field(description="Name of the skillset")
    skillsetDescription: str = strawberry.field(description="Description of the skillset")

@strawberry.input
class CreateSkillsetInput:
    companyId: str
    skillsetCategory: str
    skillsetName: str
    skillsetDescription: str

@strawberry.input
class UpdateSkillsetInput:
    skillsetCategory: Optional[str] = None
    skillsetName: Optional[str] = None
    skillsetDescription: Optional[str] = None 