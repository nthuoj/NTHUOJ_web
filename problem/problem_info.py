import os.path
from utils import config_info
from problem.models import Problem, Testcase
from django.db.models import Q

SPECIAL_PATH = config_info.get_config('path', 'special_judge_path')
PARTIAL_PATH = config_info.get_config('path', 'partial_judge_path')

def get_problem(problem):
    problem.testcase = Testcase.objects.filter(problem=problem)
    return problem

def get_problem_list(user):
    if user.is_anonymous():
        return Problem.objects.all(visible=True)
    else:
        if user.is_admin:
            return Problem.objects.all()
        else:
            return Problem.objects.filter(Q(visible=True) | Q(owner=request.user))

def has_special_judge_code(problem):
    return os.path.isfile("%s%d.c" % (SPECIAL_PATH, problem.pk))

def has_partial_judge_code(problem):
    return os.path.isfile("%s%d.c" % (PARTIAL_PATH, problem.pk))

