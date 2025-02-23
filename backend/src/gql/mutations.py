import strawberry
from modules.users.mutations import UserMutations
from modules.skillsets.mutations import SkillsetMutations
from modules.certifications.mutations import CertificationMutations
from modules.employees.mutations import EmployeeMutations
from modules.candidates.mutations import CandidateMutations
from modules.recruitment.mutations import RecruitmentMutations

@strawberry.type
class Mutation(UserMutations, SkillsetMutations, CertificationMutations, EmployeeMutations, CandidateMutations, RecruitmentMutations):
    pass

    @strawberry.mutation
    def test_mutation(self) -> str:
        """A simple test mutation to verify GraphQL mutations are working"""
        return "Mutation is working! 🚀" 