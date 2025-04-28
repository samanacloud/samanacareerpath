from datetime import datetime
import strawberry
from typing import Optional

@strawberry.type
class TemporalCode:
    id: str = strawberry.field(description="Code ID")
    code: str = strawberry.field(description="The shared code content")
    createdAt: datetime = strawberry.field(description="Creation Date")
    updatedAt: Optional[datetime] = strawberry.field(description="Last Update Date", default=None)

@strawberry.input
class CreateTemporalCodeInput:
    code: str

@strawberry.input
class UpdateTemporalCodeInput:
    code: str 