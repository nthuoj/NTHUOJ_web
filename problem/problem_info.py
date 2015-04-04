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

def get_problem_file_extension(problem):
    if problem.judge_language == problem.C:
        return ".c"
    if problem.judge_language == problem.CPP:
        return ".cpp"

def has_special_judge_code(problem):
    file_ex = get_problem_file_extension(problem)
    return os.path.isfile("%s%d%s" % (SPECIAL_PATH, problem.pk, file_ex))

def has_partial_judge_code(problem):
    file_ex = get_problem_file_extension(problem)
    return os.path.isfile("%s%d%s" % (PARTIAL_PATH, problem.pk, file_ex))

