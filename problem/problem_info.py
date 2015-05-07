import os.path
from utils import config_info
from problem.models import Problem, Testcase
from django.db.models import Q

SPECIAL_PATH = config_info.get_config('path', 'special_judge_path')
PARTIAL_PATH = config_info.get_config('path', 'partial_judge_path')
TESTCASE_PATH = config_info.get_config('path', 'testcase_path')

def get_testcase(problem):
    return Testcase.objects.filter(problem=problem).order_by('id')

def get_problem_list(user):
    if user.is_anonymous():
        return Problem.objects.filter(visible=True).order_by('id')
    else:
        if user.is_admin:
            return Problem.objects.all().order_by('id')
        else:
            return Problem.objects.filter(Q(visible=True) | Q(owner=user)).order_by('id')

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

def has_partial_judge_header(problem):
    return os.path.isfile("%s%d.h" % (PARTIAL_PATH, problem.pk))

def verify_problem_code(problem):
    problem.has_special_judge_code = has_special_judge_code(problem)
    problem.has_partial_judge_code = has_partial_judge_code(problem)
    problem.has_partial_judge_header = has_partial_judge_header(problem)
    file_ex = get_problem_file_extension(problem)
    problem.filename = "%s%s" % (problem.pk, file_ex)
    problem.headername = "%s.h" % (problem.pk)
    return problem

