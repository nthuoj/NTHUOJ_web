import requests, base64, json, bs4
from problem.models import Submission
from vjudge.models import VjudgeID
from utils.log_info import get_logger

logger = get_logger()

vjudge_user = 'henryyang42'
vjudge_password = '1234'
login_url = 'http://acm.hust.edu.cn/vjudge/user/login.action'
submit_url = 'http://acm.hust.edu.cn/vjudge/problem/submit.action'


def submit_to_vjudge(code, submission):
    try:
        # Convert to vjudge problem id
        problem = submission.problem
        vjudge_id = VjudgeID.objects.get(
            judge_source=problem.judge_type,
            judge_source_id=problem.other_judge_id).vjudge_id

        session = requests.Session()
        session.post(login_url,
            data={'username': vjudge_user, 'password': vjudge_password},
            timeout=3)
        response = session.post(submit_url,
            data={'language':1, 'isOpen':0, 'source': base64.b64encode(code), 'id': vjudge_id},
            timeout=3)

        # Find vjudge sid
        soup = bs4.BeautifulSoup(response.text.encode("utf-8"))
        sid = soup.find(id='serverTime').attrs['value']
        sid = sid[:-3]+'000'
        sid = int(sid)
        submission.other_judge_sid = sid
    except:
        logger.error('Submission %d fails to submit to vjudge' % submission.id)
        submission.status = Submission.JUDGE_ERROR
        submission.save()
