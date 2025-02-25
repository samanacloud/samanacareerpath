import strawberry
from typing import Optional

@strawberry.type
class ProcessCandidateAnalytics:
    candidateName: str
    email: str
    country: str
    salaryExpectation: int
    skillsetAvg: float
    interviewYes: int
    interviewMaybe: int
    interviewNo: int
    interviewRating: float
    certificationCount: int

@strawberry.type
class CandidateAnalytics:
    skillsetAvg: float
    interviewYes: int
    interviewMaybe: int
    interviewNo: int
    interviewRating: float
    certificationCount: int

@strawberry.type
class RecruitmentProcessAnalyticsResponse:
    candidates: list[ProcessCandidateAnalytics] 