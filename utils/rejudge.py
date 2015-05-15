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
from problem.models import Problem
from problem.models import Submission
from problem.models import SubmissionDetail

from contest.models import Contest

'''
rejudge:
1. problem's all submission
2. a single submission
3. submissions during contest
'''
def rejudge(obj):
    if isinstance(obj,problem):
        rejudge_problem(obj)
    elif isinstance(obj,submission):
        rejudge_submission(obj)
    elif isinstance(obj,contest):
        rejudge_contest(obj)

#rejudge submissions of problem
def rejudge_problem(problem):
    submissions = Submission.objects.filter(problem = problem)
    for submission in submissions:
        rejudge_submission(submission)

#rejudge single submission
def rejudge_submission(submission):
    submission.status = Submission.WAIT
    submission.save()
    sd = SubmissionDetail.objects.filter(sid = submission)
    sd.delete()

#rejudge submissions during contest
def rejudge_contest(contest):
    for problem in contest.problem.all():
        rejudge_contest_problem(contest, problem)

#rejudge submissions of problem in contest
def rejudge_contest_problem(contest, problem):
    contestants = Contestant.objects.filter(contest = contest).values_list('user', flat=True)
    submissions = Submission.objects.filter(
        problem = problem,
        submit_time__gte = contest.start_time, 
        submit_time__lte = contest.end_time,
        user__in = contestants)
    for submission in submissions:
        rejudge_submission(submission)
