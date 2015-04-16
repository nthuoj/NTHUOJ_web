import requests, base64, json, bs4
from problem.models import Submission, Problem
from vjudge.models import VjudgeID
from vjudge.status import status_url
from utils.log_info import get_logger

logger = get_logger()

vjudge_user = 'henryyang42'
vjudge_password = '1234'
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
            judge_source=problem.judge_type,
            judge_source_id=problem.other_judge_id).vjudge_id
        language = LANGUAGE_CHOICE[problem.judge_type][submission.language]

        session = requests.Session()
        session.post(login_url,
            data={'username': vjudge_user, 'password': vjudge_password},
            timeout=3)
        response = session.post(submit_url,
            data={'language':language, 'isOpen':0, 'source': base64.b64encode(code), 'id': vjudge_id},
            timeout=3)

        # Find vjudge sid
        raw_status = requests.get(status_url, timeout=5).text.encode("utf-8")
        raw_status = json.loads(raw_status)['data']
        sid = raw_status[0][0]
        submission.other_judge_sid = sid
        submission.save()
    except:
        logger.error('Submission %d fails to submit to vjudge' % submission.id)
        submission.status = Submission.JUDGE_ERROR
        submission.save()
