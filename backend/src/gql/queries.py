from strawberry.types import Info
import strawberry

from modules.users.queries import UserQueries
from modules.ai.queries import AIQueries
from modules.skillsetsdata.queries import SkillsetDataQueries
from modules.certifications.queries import CertificationQueries
from modules.employees.queries import EmployeeQueries
from modules.candidates.queries import CandidateQueries
from modules.recruitment.queries import RecruitmentQueries
from modules.interviews.queries import InterviewQueries
from modules.certificationdata.queries import CertificationDataQueries
from modules.analytics.queries import AnalyticsQueries



@strawberry.type
class Query(UserQueries, AIQueries, SkillsetDataQueries, CertificationQueries, EmployeeQueries, CandidateQueries, RecruitmentQueries, InterviewQueries, CertificationDataQueries, AnalyticsQueries):
    @strawberry.field
    def test_query(self) -> str:
        """A simple test query to verify GraphQL is working"""
        return "GraphQL is working! 🚀" 