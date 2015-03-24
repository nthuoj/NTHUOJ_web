from utils import log_info, config_info
from problem.models import Problem, Testcase

def get_problem(problem):
    problem.testcase = Testcase.objects.filter(problem=problem)
    return problem

