import strawberry
from typing import Optional
from .repository import TemporalRepository
from .schemas import TemporalCode, CreateTemporalCodeInput, UpdateTemporalCodeInput

@strawberry.type
class TemporalMutations:
    @strawberry.mutation(description="Create a new temporal code")
    async def add_temporal_code(self, input: CreateTemporalCodeInput) -> TemporalCode:
        repository = TemporalRepository()
        return await repository.create(input)

    @strawberry.mutation(description="Update an existing temporal code")
    async def edit_temporal_code(self, id: str, input: UpdateTemporalCodeInput) -> Optional[TemporalCode]:
        repository = TemporalRepository()
        return await repository.update(id, input)

    @strawberry.mutation(description="Remove a temporal code")
    async def remove_temporal_code(self, id: str) -> bool:
        repository = TemporalRepository()
        return await repository.delete(id) 