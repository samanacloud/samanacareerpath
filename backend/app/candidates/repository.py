from typing import Optional
from bson.objectid import ObjectId

async def get_candidate_by_id(candidate_id: str) -> Optional[dict]:
    return await candidates_collection.find_one(
        {"_id": ObjectId(candidate_id)},
        {"salaryExpectation": 1, ...}  # Keep all other fields
    ) 