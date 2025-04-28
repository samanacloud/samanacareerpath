import strawberry
from typing import List
from .repository import TemporalRepository
from .schemas import TemporalCode

@strawberry.type
class TemporalQueries:
    @strawberry.field(description="Get all temporal codes")
    async def list_temporal_codes(self) -> List[TemporalCode]:
        repository = TemporalRepository()
        return await repository.get_all()

    @strawberry.field(description="Get a temporal code by ID")
    async def get_temporal_code(self, id: str) -> TemporalCode:
        repository = TemporalRepository()
        return await repository.get_by_id(id) 