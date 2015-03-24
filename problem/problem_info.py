import os.path
from utils import config_info
from problem.models import Problem, Testcase

def get_problem(problem):
    problem.testcase = Testcase.objects.filter(problem=problem)
    return problem

def has_special_judge_code(problem):
    speJudge_path = config_info.get_config('path', 'special_judge_path')
    return os.path.isfile("%s%d.c" % (speJudge_path, problem.pk))

def has_partial_judge_code(problem):
    partial_path = config_info.get_config('path', 'partial_judge_path')
    return os.path.isfile("%s%d.c" % (speJudge_path, problem.pk))

