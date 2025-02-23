from modules.recruitment.queries import RecruitmentQueries
from modules.recruitment.mutations import RecruitmentMutations

@strawberry.type
class Query(UserQueries, CandidateQueries, EmployeeQueries, RecruitmentQueries):
    pass

@strawberry.type
class Mutation(UserMutations, CandidateMutations, EmployeeMutations, RecruitmentMutations):
    pass 