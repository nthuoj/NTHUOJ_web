from django.test import TestCase, Client

from time import sleep
from datetime import datetime, timedelta

from utils.test_helper import *

class NTHUOJ_TestCase_Basic(TestCase):

    def setUp(self):
        create_test_directory()
        create_test_admin_user()
        create_test_judge_user(2)
        create_test_normal_user()
        self.ADMIN_USER = get_test_admin_user()
        self.ADMIN_CLIENT = get_test_admin_client()
        self.JUDGE_USER = get_test_judge_user()
        self.JUDGE_USER_2 = get_test_judge_user(1)
        self.JUDGE_CLIENT = get_test_judge_client()
        self.NORMAL_USER = get_test_normal_user()
        self.NORMAL_CLIENT = get_test_normal_user_client()
        self.ANONYMOUS_CLIENT = Client()

    def tearDown(self):
        remove_test_directory()


class NTHUOJ_TestCase_Complex01(TestCase):

    def setUp(self):
        create_test_directory()
        create_test_admin_user()
        # create 6 judge level users
        # (1 contest owner, 2 coowners,
        #  2 problem owners, 1 contestant)
        create_test_judge_user(6)
        create_test_normal_user()
        self.ADMIN_USER = get_test_admin_user()
        self.ADMIN_CLIENT = get_test_admin_client()
        self.JUDGE_USERS = [get_test_judge_user(i) for i in xrange(6)]
        self.JUDGE_CLIENTS = [get_test_judge_client(i) for i in xrange(6)]
        self.NORMAL_USER = get_test_normal_user()
        self.NORMAL_CLIENT = get_test_normal_user_client()
        self.ANONYMOUS_CLIENT = Client()
        self.CONTEST_OWNER = self.JUDGE_USERS[0]
        self.CONTEST_COOWNERS = self.JUDGE_USERS[1:3]
        self.CONTEST_PROBLEM_OWNERS = self.JUDGE_USERS[3:5]
        self.CONTEST_CONTESTANTS = [self.JUDGE_USERS[5], self.NORMAL_USER]
        self.CONTEST_PROBLEMS = []
        self.STATUSES = [
            Submission.ACCEPTED, Submission.NOT_ACCEPTED, Submission.COMPILE_ERROR,
            Submission.RESTRICTED_FUNCTION, Submission.JUDGE_ERROR, Submission.JUDGING]
        # create 2 problems for contest
        for i in xrange(2):
            problem = create_problem(
                self.CONTEST_PROBLEM_OWNERS[i], pname='contest_problem'+str(i),
                visible=True)
            self.CONTEST_PROBLEMS.append(problem)
        # create a running contest
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() + timedelta(hours=4)
        self.CONTEST = create_contest(
            self.CONTEST_OWNER, 'test_contest', start_time, end_time,
            self.CONTEST_COOWNERS, self.CONTEST_CONTESTANTS, self.CONTEST_PROBLEMS[0:2])

    def tearDown(self):
        remove_test_directory()

    def all_submisions_when_contest_running(self):
        users = self.JUDGE_USERS + [self.NORMAL_USER]
        submissions = []
        for problem in self.CONTEST_PROBLEMS:
            for user in users:
                for status in self.STATUSES:
                    error_msg = random_word(50)
                    submission = create_submission(
                        problem, user, status, error_msg=error_msg)
                    submissions.append(submission)
        return submissions

    def stop_running_contest(self):
        self.CONTEST.end_time = datetime.now()
        self.CONTEST.save()
        sleep(1)


class NTHUOJ_TestCase_Complex02(TestCase):

    def setUp(self):
        create_test_admin_user()
        # create 6 judge level users
        # (1 as contest owner, 2 as coowner,
        #  2 as problem owner, 1 as contestant)
        create_test_judge_user(6)
        # create 51 normal users as contestants
        create_test_normal_user(51)
        self.ADMIN_USER = get_test_admin_user()
        self.ADMIN_CLIENT = get_test_admin_client()
        self.JUDGE_USERS = [get_test_judge_user(i) for i in xrange(6)]
        self.JUDGE_CLIENTS = [get_test_judge_client(i) for i in xrange(6)]
        self.NORMAL_USERS = [get_test_normal_user(i) for i in xrange(51)]
        self.NORMAL_CLIENTS = [get_test_normal_user_client(i) for i in xrange(51)]
        self.ANONYMOUS_CLIENT = Client()
        self.CONTEST_OWNER = self.JUDGE_USERS[0]
        self.CONTEST_COOWNERS = self.JUDGE_USERS[1:3]
        self.CONTEST_PROBLEM_OWNERS = self.JUDGE_USERS[3:5]
        self.CONTEST_CONTESTANTS = [self.JUDGE_USERS[5]] + self.NORMAL_USERS[0:50]
        self.CONTEST_PROBLEMS = []
        for i in xrange(2):
            problem = create_problem(
                self.CONTEST_PROBLEM_OWNERS[i], pname='contest_problem'+str(i), visible=True)
            self.CONTEST_PROBLEMS.append(problem)
        self.CONTEST = create_contest(
            self.CONTEST_OWNER, coowners=self.CONTEST_COOWNERS,
            contestants=self.CONTEST_CONTESTANTS, problems=self.CONTEST_PROBLEMS[0:2])
