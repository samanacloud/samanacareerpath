import strawberry
from modules.users.mutations import UserMutations
from modules.skillsetsdata.mutations import SkillsetDataMutations
from modules.certifications.mutations import CertificationMutations
from modules.employees.mutations import EmployeeMutations
from modules.candidates.mutations import CandidateMutations
from modules.recruitment.mutations import RecruitmentMutations
from modules.interviews.mutations import InterviewMutations
from modules.certificationdata.mutations import CertificationDataMutations
from modules.skillsets.mutations import SkillsetMutations
from modules.temporal.mutations import TemporalMutations


@strawberry.type
class Mutation(UserMutations, SkillsetDataMutations, CertificationMutations, EmployeeMutations, CandidateMutations, RecruitmentMutations, InterviewMutations, CertificationDataMutations, SkillsetMutations, TemporalMutations):
    pass

    @strawberry.mutation
    def test_mutation(self) -> str:
        """A simple test mutation to verify GraphQL mutations are working"""
        return "Mutation is working! 🚀" 