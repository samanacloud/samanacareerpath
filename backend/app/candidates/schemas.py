class Candidate(BaseModel):
    salaryExpectation: Optional[int] = None

class CreateCandidateInput(BaseModel):
    salaryExpectation: Optional[int] = None

class UpdateCandidateInput(BaseModel):
    salaryExpectation: Optional[int] = None 