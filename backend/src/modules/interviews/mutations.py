import strawberry
from typing import Optional
from .schemas import Interview, AddInterviewInput, EditInterviewInput
from .repository import InterviewRepository

def normalize_approved(value: str) -> str:
    v = value.lower()
    if v in ['approved', 'yes']:
        return 'Yes'
    elif v in ['rejected', 'no']:
        return 'No'
    else:
        return 'Pending'

@strawberry.type
class InterviewMutations:
    @strawberry.mutation
    async def add_interview(self, input: AddInterviewInput) -> Optional[Interview]:
        """Create new interview entry"""
        # Normalize the approved field in the input
        input_data = dict(input.__dict__)
        if 'approved' in input_data and input_data['approved']:
            input_data['approved'] = normalize_approved(input_data['approved'])

        repo = InterviewRepository()
        result = await repo.create_interview(input_data)
        if result and '_id' in result:
            result['id'] = result.pop('_id')
        if result and 'approved' in result:
            result['approved'] = normalize_approved(result['approved'])
        return Interview(**result) if result else None

    @strawberry.mutation
    async def edit_interview(self, id: str, input: EditInterviewInput) -> Optional[Interview]:
        """Update existing interview"""
        # Normalize the approved field in the input
        input_data = dict(input.__dict__)
        if 'approved' in input_data and input_data['approved']:
            input_data['approved'] = normalize_approved(input_data['approved'])

        repo = InterviewRepository()
        update_data = {k: v for k, v in input_data.items() if v is not None}
        result = await repo.update_interview(id, update_data)
        if result and 'approved' in result:
            result['approved'] = normalize_approved(result['approved'])
        return Interview(**result) if result else None

    @strawberry.mutation
    async def delete_interview(self, id: str) -> bool:
        """Delete interview entry"""
        repo = InterviewRepository()
        return await repo.delete_interview(id) 