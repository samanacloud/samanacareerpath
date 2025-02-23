from strawberry.types import Info
import strawberry

from modules.users.queries import UserQueries
from modules.ai.queries import AIQueries
from modules.skillsets.queries import SkillsetQueries
from modules.certifications.queries import CertificationQueries
from modules.employees.queries import EmployeeQueries
from modules.candidates.queries import CandidateQueries
from modules.recruitment.queries import RecruitmentQueries


@strawberry.type
class Query(UserQueries, AIQueries, SkillsetQueries, CertificationQueries, EmployeeQueries, CandidateQueries, RecruitmentQueries):
    @strawberry.field
    def test_query(self) -> str:
        """A simple test query to verify GraphQL is working"""
        return "GraphQL is working! 🚀" 