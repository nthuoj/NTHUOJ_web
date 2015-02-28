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
from operator import methodcaller
class Scoreboard:
    def __init__(self,start_time):
        self.users = []
        self.problems = []
        self.start_time = start_time

    def add_user(self,user):
        self.users.append(user)

    def add_problem(self,scoreboard_problem):
        self.problems.append(scoreboard_problem)

    def get_problem(self,id):
        for scoreboard_problem in self.problems:
            if (scoreboard_problem.id == id):
                return scoreboard_problem

    #sort by solved descending. if same sort by penalty
    def sort_users(self):
        self.users = sorted(self.users, key=methodcaller('penalty',self.start_time))
        self.users = sorted(self.users, key=methodcaller('solved'), reverse=True)

#for scoreboard
class Scoreboard_Problem:
    def __init__(self,id,pname,total_testcase):
        self.id = id
        self.pname = pname
        self.total_testcase = total_testcase
        self.pass_user = 0

    def add_pass_user(self):
        self.pass_user += 1

class User:
    def __init__(self,username):
        self.username = username
        self.problems = []

    def add_problem(self,problem):
        self.problems.append(problem)

    def get_problem(self,id):
        for problem in self.problems:
            if(problem.id == id):
                return problem

    def solved(self):
        count = 0
        for problem in self.problems:
            if(problem.is_solved() == True):
                count += 1
        return count

    def penalty(self,start_time):
        penalty = 0
        for problem in self.problems:
            penalty += problem.penalty(start_time);
        return penalty

#for each user
class Problem:
    def __init__(self,id):
        self.submissions = []
        self.id = id

    def is_solved(self):
        for submission in self.submissions:
            if submission.is_solved():
                return True
        return False

    def testcase_solved(self):
        testcase_solved = 0
        for submission in self.submissions:
            testcase_solved = max(testcase_solved,submission.pass_testcase)
        return testcase_solved

    def add_submission(self,submission):
        self.submissions.append(submission)

    def submit_times(self):
        return self.submissions.__len__()

    def penalty(self,start_time):
        minute = 60
        #every not passed submission should add addtional penalty
        not_pass_penalty_unit = 20
        addtional_penalty = 0
        penalty = sys.maxsize
        for submission in self.submissions:
            if submission.is_solved():
                penalty = min(penalty,(submission.submit_time - start_time).total_seconds()/minute)
            else:
                addtional_penalty += not_pass_penalty_unit
        if(penalty == sys.maxsize):
            return 0
        return int(penalty) + addtional_penalty

class Submission:
    def __init__(self,submit_time,pass_testcase,total_testcase):
        self.submit_time = submit_time
        self.pass_testcase = pass_testcase
        self.total_testcase = total_testcase

    def is_solved(self):
        if(self.pass_testcase == self.total_testcase):
            return True
        else:
            return False
