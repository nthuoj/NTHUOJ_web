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
from users.models import User
from django.test import TestCase
from contest.models import Contest
from datetime import datetime, timedelta
from problem.models import Problem, Submission, SubmissionDetail, Testcase
from status.templatetags.status_filters import show_detail, show_submission

# Create your tests here.


class StatusSubmissionTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin', password='admin', user_level='ADMIN')
        self.judge = User.objects.create(username='judge', password='judge', user_level='JUDGE')
        self.subjudge = User.objects.create(username='subjudge', password='subjudge', user_level='SUB-JUDGE')
        self.user1 = User.objects.create(username='user1', password='user1', user_level='USER')
        # user2 is normal user (not problem owner, contest owner, etc)
        self.user2 = User.objects.create(username='user2', password='user2', user_level='USER')

        self.admin_problem = Problem.objects.create(pname='Admin Problem', owner_id=self.admin, visible=True)
        self.admin_testcase = Testcase.objects.create(problem=self.admin_problem)

        self.judge_problem = Problem.objects.create(pname='Judge Problem', owner_id=self.judge, visible=True)
        self.judge_testcase = Testcase.objects.create(problem=self.judge_problem)

        self.subjudge_problem = Problem.objects.create(pname='SubJudge Problem', owner_id=self.subjudge, visible=True)
        self.subjudge_testcase = Testcase.objects.create(problem=self.subjudge_problem)

        self.user1_problem = Problem.objects.create(pname='User1 Problem', owner_id=self.user1, visible=True)
        self.user1_testcase = Testcase.objects.create(problem=self.user1_problem)

        self.invisible_problem = Problem.objects.create(pname='Invisible Problem', owner_id=self.user1, visible=False)
        self.invisible_testcase = Testcase.objects.create(problem=self.invisible_problem)

        self.contest_problem = Problem.objects.create(pname='Contest Problem', owner_id=self.user1, visible=True)
        self.contest_testcase = Testcase.objects.create(problem=self.contest_problem)

        # crete a contest held by subjudge and user1 for 5 hours (ie, active during the unit test)
        self.contest = Contest.objects.create(cname='Contest by user1 & subjudge', owner=self.subjudge,
            start_time=datetime.now()-timedelta(hours=1), end_time=datetime.now()+timedelta(hours=4))
        self.contest.coowner.add(self.user1) # user1 as coowner
        self.contest.problem.add(self.contest_problem)

        users = [self.user1, self.subjudge, self.judge, self.admin]
        problems = [
            (self.admin_problem, self.admin_testcase),
            (self.judge_problem, self.judge_testcase),
            (self.subjudge_problem, self.subjudge_testcase),
            (self.user1_problem, self.user1_testcase),
            (self.invisible_problem, self.invisible_testcase),
            (self.contest_problem, self.contest_testcase)
        ]
        # generate submissions of different case
        for user in users:
            for problem in problems:
                submission = Submission.objects.create(problem=problem[0], user=user, status='AC')
                SubmissionDetail.objects.create(sid=submission, tid=problem[1], virdect='AC')

    def test_admin_view_submissions(self):
        '''Test if admin can view all submissions'''
        submissions = Submission.objects.all()
        for submission in submissions:
            can_show = show_submission(submission, self.admin)
            self.assertEqual(can_show, True)

    def test_not_admin_view_submissions(self):
        '''When the user is not admin, they are treated as normal user if they
        don't have special authorities (problem owner, contest owner, etc)

        In this case, we use user2 to test that kind of authorties'''
        hidden_submissions = []

        # 1. admin's submissions can't be seen
        submissions = Submission.objects.filter(user=self.admin)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user2)
            self.assertEqual(can_show, False)

        # 2. invisible problem can't be seen
        submissions = Submission.objects.filter(problem=self.invisible_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user2)
            self.assertEqual(can_show, False)

        # 3. problem owner's submission can't be seen
        problems = Problem.objects.all()
        submissions = []
        for problem in problems:
            submissions += Submission.objects.filter(problem=problem, user=problem.owner_id)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user2)
            self.assertEqual(can_show, False)

        # 4. contest owner/coowner's submissions can't be seen if a contest is not ended
        # contest owner case
        submissions = Submission.objects.filter(user=self.subjudge, problem=self.contest_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user2)
            self.assertEqual(can_show, False)
        # contest coowner case
        submissions = Submission.objects.filter(user=self.user1, problem=self.contest_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user2)
            self.assertEqual(can_show, False)

        # all submissions subtract hidden submissions are what normal user can see
        print hidden_submissions
        submissions = Submission.objects.all()
        for submission in submissions:
            if submission not in hidden_submissions:
                can_show = show_submission(submission, self.user2)
                self.assertEqual(can_show, True)
