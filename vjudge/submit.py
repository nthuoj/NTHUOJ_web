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
import requests, base64, json
from problem.models import Submission, Problem
from vjudge.models import VjudgeID
from vjudge.status import status_url
from utils.config_info import get_config
from utils.log_info import get_logger

logger = get_logger()

vjudge_username = get_config('vjudge', 'username')
vjudge_password = get_config('vjudge', 'password')
login_url = 'http://acm.hust.edu.cn/vjudge/user/login.action'
submit_url = 'http://acm.hust.edu.cn/vjudge/problem/submit.action'

LANGUAGE_CHOICE = {
    Problem.UVA_JUDGE: {Problem.C: 1 ,Problem.CPP: 3, Problem.CPP11: 5},
    Problem.ICPC_JUDGE: {Problem.C: 1 ,Problem.CPP: 3, Problem.CPP11: 5},
    Problem.POJ_JUDGE: {Problem.C: 1 ,Problem.CPP: 0, Problem.CPP11: 0}
}

def submit_to_vjudge(code, submission):
    try:
        # Convert to vjudge problem id
        problem = submission.problem
        vjudge_id = VjudgeID.objects.get(
            judge_source=problem.judge_type.replace('OTHER_', ''),
            judge_source_id=problem.other_judge_id).vjudge_id
        language = LANGUAGE_CHOICE[problem.judge_type][submission.language]

        session = requests.Session()
        session.post(login_url,
            data={'username': vjudge_username, 'password': vjudge_password},
            timeout=3)
        response = session.post(submit_url,
            data={'language':language, 'isOpen':0, 'source': base64.b64encode(code), 'id': vjudge_id},
            timeout=3)
        # Find vjudge sid
        raw_status = requests.get(status_url, timeout=5).text.encode("utf-8")
        raw_status = json.loads(raw_status)['data']
        sid = raw_status[0][0]
        submission.other_judge_sid = sid
        submission.status = Submission.JUDGING
    except:
        logger.error('Submission %d fails to submit to vjudge' % submission.id)
        submission.status = Submission.JUDGE_ERROR
    finally:
        submission.save()
