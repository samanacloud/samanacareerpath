import strawberry
from typing import Optional

from modules.analytics.schemas import ProcessCandidateAnalytics, RecruitmentProcessAnalyticsResponse, CandidateAnalytics
from modules.analytics.repository import get_recruitment_process_analytics, get_candidate_analytics

@strawberry.type
class AnalyticsQueries:
    @strawberry.field
    async def recruitmentProcessAnalytics(self, recruitmentProcessId: str) -> RecruitmentProcessAnalyticsResponse:
        """
        Get analytics for all candidates in a specific recruitment process.
        
        Args:
            recruitmentProcessId: The ID of the recruitment process to analyze
            
        Returns:
            Analytics data for all candidates in the recruitment process
        """
        results = await get_recruitment_process_analytics(recruitmentProcessId)
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
    
    @strawberry.field
    async def candidateAnalytics(self, email: str) -> CandidateAnalytics:
        """
        Get analytics for a specific candidate by email.
        
        Args:
            email: The email of the candidate to analyze
            
        Returns:
            Analytics data for the candidate
        """
        result = await get_candidate_analytics(email)
        return CandidateAnalytics(
            skillsetAvg=result.get("skillsetAvg", 0),
            interviewYes=result.get("interviewYes", 0),
            interviewMaybe=result.get("interviewMaybe", 0),
            interviewNo=result.get("interviewNo", 0),
            interviewRating=result.get("interviewRating", 0),
            certificationCount=result.get("certificationCount", 0)
        ) 