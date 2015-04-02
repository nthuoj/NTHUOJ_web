import os.path
from utils import config_info
from problem.models import Problem, Testcase
from django.db.models import Q

SPECIAL_PATH = config_info.get_config('path', 'special_judge_path')
PARTIAL_PATH = config_info.get_config('path', 'partial_judge_path')

def get_testcase(problem):
    return Testcase.objects.filter(problem=problem)

def get_problem_list(user):
    if user.is_anonymous():
        return Problem.objects.filter(visible=True)
    else:
        if user.is_admin:
            return Problem.objects.all()
        else:
            return Problem.objects.filter(Q(visible=True) | Q(owner=user))

def has_special_judge_code(problem):
    if problem.judge_language == problem.C:
        return os.path.isfile("%s%d.c" % (SPECIAL_PATH, problem.pk))
    if problem.judge_language == problem.CPP:
        return os.path.isfile("%s%d.cpp" % (SPECIAL_PATH, problem.pk))

def has_partial_judge_code(problem):
    if problem.judge_language == problem.C:
        return os.path.isfile("%s%d.c" % (PARTIAL_PATH, problem.pk))
    if problem.judge_language == problem.CPP:
        return os.path.isfile("%s%d.cpp" % (PARTIAL_PATH, problem.pk))

