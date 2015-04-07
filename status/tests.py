"""
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
"""
from datetime import datetime, timedelta

from django.test import TestCase

from users.models import User
from contest.models import Contest
from team.models import Team, TeamMember
from problem.models import Problem, Submission
from status.templatetags.status_filters import show_detail, show_submission


# Create your tests here.


class StatusTestCase(TestCase):
    def submissionComplement(self, submissions):
        complement = []
        all_submissions = Submission.objects.all()
        for submission in all_submissions:
            if submission not in submissions:
                complement.append(submission)
        return complement

    def setUp(self):
        self.admin = User.objects.create(username='admin', password='admin', user_level='ADMIN')
        self.judge = User.objects.create(username='judge', password='judge', user_level='JUDGE')
        self.subjudge = User.objects.create(username='subjudge', password='subjudge', user_level='SUB_JUDGE')
        self.user = User.objects.create(username='user', password='user', user_level='USER')

        self.admin_problem = Problem.objects.create(pname='Admin Problem', owner_id=self.admin, visible=True)
        self.judge_problem = Problem.objects.create(pname='Judge Problem', owner_id=self.judge, visible=True)
        self.subjudge_problem = Problem.objects.create(pname='SubJudge Problem', owner_id=self.subjudge, visible=True)
        self.invisible_problem = Problem.objects.create(pname='Invisible Problem', owner_id=self.subjudge, visible=False)
        self.contest_problem = Problem.objects.create(pname='Contest Problem', owner_id=self.subjudge, visible=True)

        # crete a contest held by judge and subjudge for 5 hours (ie, active during the unit test)
        self.contest = Contest.objects.create(cname='Contest by judge & subjudge', owner=self.judge,
            start_time=datetime.now()-timedelta(hours=1), end_time=datetime.now()+timedelta(hours=4))

        self.contest.coowner.add(self.subjudge) # subjudge as coowner
        self.contest.problem.add(self.contest_problem)

        users = [self.subjudge, self.judge, self.admin]
        problems = [
            self.admin_problem,
            self.judge_problem,
            self.subjudge_problem,
            self.invisible_problem,
            self.contest_problem
        ]
        # generate submissions of different case
        for user in users:
            for problem in problems:
                Submission.objects.create(problem=problem, user=user)

        for problem in problems:
            if problem.visible:  # by no mean will a normal user send invisible problem
                Submission.objects.create(problem=problem, user=self.user)

    def test_admin_view_submissions(self):
        """Test if admin can view all submissions"""
        submissions = Submission.objects.all()
        for submission in submissions:
            can_show = show_submission(submission, self.admin)
            self.assertEqual(can_show, True)

    def test_not_admin_view_submissions(self):
        """When the user is not admin, they are treated as normal user if they
        don't have special authorities (problem owner, contest owner, etc)

        In this case, we use user to test that kind of authorties"""
        hidden_submissions = []
        # all submission should be seen except these 4 conditions
        # 1. admin's submissions can't be seen
        submissions = Submission.objects.filter(user=self.admin)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, False)

        # 2. invisible problem can't be seen
        submissions = Submission.objects.filter(problem=self.invisible_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, False)

        # 3. problem owner's submission can't be seen
        problems = Problem.objects.all()
        submissions = []
        for problem in problems:
            submissions += Submission.objects.filter(problem=problem, user=problem.owner_id)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, False)

        # 4. contest owner/coowner's submissions can't be seen if a contest is not ended
        # contest owner case
        submissions = Submission.objects.filter(user=self.judge, problem=self.contest_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, False)
        # contest coowner case
        submissions = Submission.objects.filter(user=self.subjudge, problem=self.contest_problem)
        hidden_submissions += submissions
        for submission in submissions:
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, False)

        # all submissions subtract hidden submissions are what normal user can see
        for submission in self.submissionComplement(hidden_submissions):
            can_show = show_submission(submission, self.user)
            self.assertEqual(can_show, True)

    def test_admin_view_details(self):
        """Test if admin can view everyone's details"""
        submissions = Submission.objects.all()
        for submission in submissions:
            can_show = show_detail(submission, self.admin)
            self.assertEqual(can_show, True)

    def test_not_admin_view_details_with_contests(self):
        """Test if non-admin can view details when there are contests"""
        # during the contest, only contest owner/coowner can view detail

        # 1. judge/subjudge can view all contest detail (as a contest owner/coowner)
        submissions = Submission.objects.filter(problem=self.contest_problem)
        submissions = submissions.exclude(user=self.admin)

        for submission in submissions:
            can_show = show_detail(submission, self.judge)
            self.assertEqual(can_show, True)
        for submission in submissions:
            can_show = show_detail(submission, self.subjudge)
            self.assertEqual(can_show, True)

        # on the other hand, other details can't be seen
        for submission in self.submissionComplement(submissions):
            can_show = show_detail(submission, self.judge)
            self.assertEqual(can_show, False)
        for submission in self.submissionComplement(submissions):
            can_show = show_detail(submission, self.subjudge)
            self.assertEqual(can_show, False)

        # 2. user can't see any detail
        submissions = Submission.objects.all()
        for submission in submissions:
            can_show = show_detail(submission, self.user)
            self.assertEqual(can_show, False)

    def test_not_admin_view_details_without_contests(self):
        """Test if non-admin can view details when there are no contests"""
        # delete all contests
        Contest.objects.all().delete()
        # all submissions exclude admin's
        all_submissions = Submission.objects.all().exclude(user=self.admin)
        all_problems = Problem.objects.all()

        # 1. one can see his own detail
        for submission in all_submissions:
            can_show = show_detail(submission, submission.user)
            self.assertEqual(can_show, True)

        # 2. problem owner can see all detail in his problem
        for problem in all_problems:
            submissions = all_submissions.filter(problem=problem)
            user = User.objects.get(username=problem.owner_id)
            for submission in submissions:
                can_show = show_detail(submission, user)
                self.assertEqual(can_show, True)

        # 3. team member can see all detail when submitted as team
        # create a team with subjudge as leader and user as member
        team = Team.objects.create(team_name='test_team', leader=self.subjudge)
        TeamMember.objects.create(team=team, member=self.user)

        # both subjudge and user submit as team
        subjudge_submission = Submission.objects.create(
            problem=self.admin_problem, user=self.subjudge, team=team)
        user_submission = Submission.objects.create(
            problem=self.admin_problem, user=self.user, team=team)

        # can see each others' detail
        can_show = show_detail(subjudge_submission, self.user)
        self.assertEqual(can_show, True)
        can_show = show_detail(user_submission, self.subjudge)
        self.assertEqual(can_show, True)
