'''
    The MIT License (MIT)
    Copyright (c) 2014 NTHUOJ team
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    '''
import sys
from operator import methodcaller, attrgetter

USER_ID, PROBLEM_ID, TOTAL_AC, TESTCASE, TIMES, PENALTY, FIRST_AC_TIME = tuple(range(7))

class Scoreboard:
    def __init__(self, start_time):
        self.users = []
        self.problems = []
        self.start_time = start_time

    def add_user(self, user):
        self.users.append(user)

    def add_problem(self, scoreboard_problem):
        self.problems.append(scoreboard_problem)

    def get_problem(self, problem_id):
        for scoreboard_problem in self.problems:
            if (scoreboard_problem.id == problem_id):
                return scoreboard_problem

    # sort by solved descending. if same sort by penalty
    def sort_users_by_penalty(self):
        self.users = sorted(self.users, key=methodcaller('get_penalty', self.start_time))
        self.users = sorted(self.users, key=methodcaller('get_solved'), reverse=True)

    def sort_users_by_solved_testcases(self):
        self.users = sorted(self.users, key=methodcaller('get_testcases_solved'), reverse=True)

class ScoreboardProblem:
    def __init__(self, id, pname, total_testcase):
        self.id = id
        self.pname = pname
        self.total_testcase = total_testcase
        self.pass_user = 0
        self.total_solved = 0
        self.no_submission = True
        self.pass_rate = 0
        self.not_pass_rate = 100

    def add_pass_user(self):
        self.pass_user += 1

    def update_total_solved(self, increment):
        self.total_solved += increment

    def set_no_submission(self):
        self.no_submission = False

    def generate_pass_rate(self, user_count):
        self.pass_rate = float(self.pass_user) / user_count * 100
        self.not_pass_rate = 100 - self.pass_rate

class User:
    def __init__(self, username):
        self.username = username
        self.problems = []
        self.solved = 0
        self.testcases_solved = 0
        self.penalty = '--'

    def add_problem(self, problem):
        self.problems.append(problem)

    def get_solved(self):
        return self.solved

    def get_testcases_solved(self):
        if self.testcases_solved == '--':
            return 0
        return self.testcases_solved

    def get_penalty(self,start_time):
        if self.penalty == '--':
            return 0
        return self.penalty

    def increase_solved(self):
        self.solved += 1

    def update_testcase_solved(self, increment):
        self.testcases_solved += increment

    def update_penalty(self, increment):
        if self.penalty == '--':
            self.penalty = 0
        self.penalty += increment

class UserProblem:
    def __init__(self, id, total_testcases):
        self.submissions = []
        self.id = id
        self.total_testcases = total_testcases
        self.testcases_solved = 0
        self.submit_times = '--'
        self.penalty = '--'
        self.AC_time = '--'
        self.solved = False

    def is_solved(self):
        for submission in self.submissions:
            if submission.is_solved(self.total_testcases):
                return True
        return False

    def get_testcases_solved(self):
        testcases_solved = 0
        for submission in self.submissions:
            testcases_solved = max(testcases_solved, submission.pass_testcases)
        return testcases_solved

    def add_submission(self, submission):
        self.submissions.append(submission)

    def submit_times(self):
        return len(self.submissions)

    def get_penalty(self, start_time):
        # every not passed submission should add addtional penalty
        NOT_PASS_PENALTY_UNIT = 20
        wrong_try = 0
        for submission in self.submissions:
            if submission.is_solved(self.total_testcases):
                return int(wrong_try * NOT_PASS_PENALTY_UNIT + submission.get_penalty(start_time))
            else:
                wrong_try += 1
        return 0

    def set_attributes(self, row):
        self.testcases_solved = row[TOTAL_AC]
        self.submit_times = row[TIMES]
        self.penalty = row[PENALTY]
        self.AC_time = row[FIRST_AC_TIME]
        self.solved = (row[FIRST_AC_TIME]!='--')

class Submission:
    def __init__(self, submit_time, pass_testcases):
        self.submit_time = submit_time
        self.pass_testcases = pass_testcases

    def is_solved(self, total_testcases):
        return (self.pass_testcases == total_testcases)

    def get_penalty(self, start_time):
        MINUTE = 60
        return ((self.submit_time - start_time).total_seconds() / MINUTE)
