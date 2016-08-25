from django.test import Client

import os
import random
import string
import filecmp
import shutil
from datetime import datetime, timedelta

from problem.models import Problem, Tag, Testcase, Submission
from contest.models import Contest, Clarification
from contest.register_contest import add_contestants
from users.models import User
from utils import config_info

TESTCASE_PATH = config_info.get_config('path', 'testcase_path')
SPECIAL_PATH = config_info.get_config('path', 'special_judge_path')
PARTIAL_PATH = config_info.get_config('path', 'partial_judge_path')
TEST_PATH = './testestestestestestest/'


def create_test_directory():
    if not os.path.isdir(TEST_PATH):
        os.makedirs(TEST_PATH)

def remove_test_directory():
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)

def create_test_user(username, password, user_level):
    test_user = User.objects.create_user(username, password)
    test_user.user_level = user_level
    test_user.is_active = True
    test_user.save()

def create_test_admin_user(num=1):
    for i in range(num):
        username = "test_admin%s" % (i)
        password = "test_admin%s" % (i)
        user_level = User.ADMIN
        create_test_user(username, password, user_level)

def create_test_judge_user(num=1):
    for i in range(num):
        username = "test_judge%s" % (i)
        password = "test_judge%s" % (i)
        user_level = User.JUDGE
        create_test_user(username, password, user_level)

def create_test_normal_user(num=1):
    for i in range(num):
        username = "test_user%s" % (i)
        password = "test_user%s" % (i)
        user_level = User.USER
        create_test_user(username, password, user_level)

def get_test_admin_user(index=0):
    name = "test_admin%s" % (index)
    return User.objects.get(username=name)

def get_test_judge_user(index=0):
    name = "test_judge%s" % (index)
    return User.objects.get(username=name)

def get_test_normal_user(index=0):
    name = "test_user%s" % (index)
    return User.objects.get(username=name)

def get_test_admin_client(index=0):
    test_admin_client = Client()
    text = "test_admin%s" % (index)
    test_admin_client.login(username=text, password=text)
    return test_admin_client

def get_test_judge_client(index=0):
    test_judge_client = Client()
    text = "test_judge%s" % (index)
    test_judge_client.login(username=text, password=text)
    return test_judge_client

def get_test_normal_user_client(index=0):
    test_user_client = Client()
    text = "test_user%s" % (index)
    test_user_client.login(username=text, password=text)
    return test_user_client

def create_problem(owner, pname=None, visible=False):
    if pname == None:
        pname = random_word(20)
    problem = Problem.objects.create(pname=pname, owner=owner, visible=visible)
    return problem

def random_word(length):
    return ''.join(random.choice(string.lowercase) for i in range(length)) 

def create_judge_code(prefix, pid, file_ex, size=100):
    file_name = "%s%s%s%s" % (TEST_PATH, prefix, pid, file_ex)
    try:
        with open(file_name, 'w') as fp:
            fp.write(random_word(size))
    except (IOError, OSError):
        print "Failed to create judge code for testing..."
        raise
    return file_name

def create_testcase_files(file_name, size=100, uploaded=False):
    if file_name == "":
        file_name = random_word(50)
    if not uploaded:
        path = TEST_PATH
    else:
        path = TESTCASE_PATH
    input_file_name = "%s%s.in" % (path, file_name)
    output_file_name = "%s%s.out" % (path, file_name)
    try:
        with open(input_file_name, 'w') as t_in:
            t_in.write(random_word(size))
        with open(output_file_name, 'w') as t_out:
            t_out.write(random_word(size))
    except (IOError, OSError):
        print "Failed to create testcase files for testing..."
        raise
    return file_name

def create_testcase(problem, time_limit=1, memory_limit=32, local_files=True, uploaded_files=False):
    testcase = Testcase.objects.create(problem=problem, time_limit=time_limit,
                                       memory_limit=memory_limit)
    if local_files:
        create_testcase_files(testcase.pk)
    if uploaded_files:
        create_testcase_files(testcase.pk, uploaded=True)
    return testcase

def remove_file_if_exists(file_name):
    try:
        if os.path.isfile(file_name):
            os.remove(file_name)
    except (IOError, OSError):
        print "Something went wrong when removing file: %s" % (file_name)

def remove_testcase_file(local_file_name, uploaded_file_name=None):
    local_input_file_name = "%s%s.in" % (TEST_PATH, local_file_name)
    local_output_file_name = "%s%s.out" % (TEST_PATH, local_file_name)
    remove_file_if_exists(local_input_file_name)
    remove_file_if_exists(local_output_file_name)
    if uploaded_file_name != None:
        uploaded_input_file_name = "%s%s.in" % (TESTCASE_PATH, uploaded_file_name)
        uploaded_output_file_name = "%s%s.out" % (TESTCASE_PATH, uploaded_file_name)
        remove_file_if_exists(uploaded_input_file_name)
        remove_file_if_exists(uploaded_output_file_name)

def compare_local_and_uploaded_file(local_file_name, uploaded_file_name):
    try:
        return filecmp.cmp(local_file_name, uploaded_file_name)
    except (IOError, OSError):
        print "Something went wrong during file I/O..."
        print "Please make sure the path for special/parcial judge code in nthuoj.cfg\
               is an existing directory."
        print "Also, the user account of this machine that nthuoj depends on\
               should have permission to access and modify all the files in this directory."
        raise

def compare_local_and_uploaded_testcase_files(local_file_name, uploaded_file_name):
    in_local = "%s%s.in" % (TEST_PATH, local_file_name)
    out_local = "%s%s.out" % (TEST_PATH, local_file_name)
    in_upload = "%s%s.in" % (TESTCASE_PATH, uploaded_file_name)
    out_upload = "%s%s.out" % (TESTCASE_PATH, uploaded_file_name)
    try:
        return filecmp.cmp(in_upload, in_local) and filecmp.cmp(out_upload, out_local)
    except (IOError, OSError):
        print "Something went wrong during file I/O..."
        print "Please make sure the path for testcase in nthuoj.cfg is an existing directory."
        print "Also, the user account of this machine that nthuoj depends on\
               should have permission to access and modify all the files in this directory."
        raise

def create_tag(tag_name, problem):
    new_tag, created = Tag.objects.get_or_create(tag_name=tag_name)
    #new_tag = Tag.objects.create(tag_name=tag_name)
    problem.tags.add(new_tag)
    problem.save()
    return new_tag

def create_submission(problem, user, status, submit_time=None, error_msg=None):
    submission = Submission.objects.create(problem=problem, user=user, status=status)
    if submit_time!=None:
        submission.submit_time = submit_time
    if error_msg!=None:
        submission.error_msg = error_msg
    submission.save()
    return submission

def POST_data_of_editing_Problem(owner, pname=None, description=None, input=None,
                                 output=None, sample_in=None, sample_out=None,
                                 visible=True, judge_source=Problem.LOCAL,
                                 judge_type=Problem.NORMAL, judge_language=Problem.CPP):
    data = {
        'pname': 'testProblem',
        'owner': owner.username,
        'description': 'This is a problem for testing.',
        'input': 'No input.',
        'output': 'Display "Hello World!" in standard output.',
        'sample_in': '--',
        'sample_out': 'Hello World!',
        'visible': visible,
        'judge_source': judge_source,
        'judge_type': judge_type,
        'judge_language': judge_language,
    }
    if pname:
        data['pname'] = pname
    if description:
        data['description'] = description
    if input:
        data['input'] = input
    if output:
        data['output'] = output
    if sample_in:
        data['sample_in'] = sample_in
    if sample_out:
        data['sample_out'] = sample_out
    return data

def create_contest(owner, cname=None, start_time=None, end_time=None,
                   coowners=[], contestants=[], problems=[],
                   is_homework=False, open_register=True):
    if cname == None:
        cname = random_word(20)
    if start_time == None:
        start_time = datetime.now() - timedelta(hours=1)
    if end_time == None:
        end_time = start_time + timedelta(hours=4)
    new_contest = Contest.objects.create(
        cname=cname, owner=owner, start_time=start_time, end_time=end_time,
        is_homework=is_homework, open_register=open_register)
    for user in coowners:
        new_contest.coowner.add(user)
    add_contestants(contestants, new_contest)
    for p in problems:
        new_contest.problem.add(p)
    return new_contest

def create_contest_by_data(data):
    owner = User.objects.get(username=data['owner'])
    cname = data['cname']
    start_time = data['start_time']
    end_time = data['end_time']
    is_homework = data['is_homework']
    open_register = data['open_register']
    coowners = User.objects.filter(username__in=list(data['coowner']))
    contestants=[]
    problems = Problem.objects.filter(pk__in=list(data['problem']))
    return create_contest(owner, cname, start_time, end_time,
        coowners, contestants, problems, is_homework, open_register)

def create_source_code(path, sid, file_ex, size=100):
    file_name = "%s%s.%s" % (path, sid, file_ex)
    content = random_word(size)
    try:
        with open(file_name, 'w') as fp:
            fp.write(content)
    except (IOError, OSError):
        print "Failed to create judge code for testing..."
        raise
    return file_name, content

def POST_data_of_editing_Contest(owner, cname=None, start_time=None, end_time=None,
                                 freeze_time=0, is_homework=False, open_register=True,
                                 coowners=[], problems=[]):
    if cname == None:
        cname = random_word(20)
    if start_time == None:
        start_time = datetime.now() - timedelta(hours=1)
    if end_time == None:
        end_time = start_time + timedelta(hours=4)
    coowner_tuple = tuple([user.username for user in coowners])
    problem_tuple = tuple([problem.pk for problem in problems])
    data = {
        'cname': cname,
        'owner': owner.username,
        'start_time': start_time,
        'end_time': end_time,
        'coowner': coowner_tuple,
        'problem': problem_tuple,
        'freeze_time': freeze_time,
        'is_homework': is_homework,
        'open_register': open_register,
    }
    return data

def create_clarification(contest, problem, asker, content=None):
    if content == None:
        content = random_word(100)
    new_clarification = Clarification.objects.create(
        contest=contest, problem=problem, asker=asker, content=content)
    return new_clarification
