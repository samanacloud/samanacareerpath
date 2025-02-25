import strawberry

from modules.analytics.schemas import ProcessCandidateAnalytics, RecruitmentProcessAnalyticsResponse
from modules.analytics.repository import get_recruitment_process_analytics

@strawberry.type
class AnalyticsQueries:
    @strawberry.field
    def recruitmentProcessAnalytics(self, recruitmentProcessId: str) -> RecruitmentProcessAnalyticsResponse:
        results = get_recruitment_process_analytics(recruitmentProcessId)
        candidates = []
        for candidate in results:
            candidates.append(ProcessCandidateAnalytics(
                candidateName=candidate.get("candidateName", ""),
                email=candidate.get("email", ""),
                country=candidate.get("country", ""),
                salaryExpectation=candidate.get("salaryExpectation", 0),
                skillsetAvg=candidate.get("skillsetAvg", 0),
                interviewYes=candidate.get("interviewYes", 0),
                interviewMaybe=candidate.get("interviewMaybe", 0),
                interviewNo=candidate.get("interviewNo", 0),
                interviewRating=candidate.get("interviewRating", 0),
                certificationCount=candidate.get("certificationCount", 0)
            ))
        return RecruitmentProcessAnalyticsResponse(candidates=candidates) 