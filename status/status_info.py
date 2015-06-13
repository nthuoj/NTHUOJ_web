from datetime import datetime
from django.db.models import Q

from contest.contest_info import get_running_contests, \
    get_freeze_time_datetime, get_contestant
from contest.models import Contest
from problem.models import Problem, Submission, SubmissionDetail
from users.models import User
from utils.user_info import validate_user, has_contest_ownership


def regroup_submission(submissions):
    submission_groups = []
    for submission in submissions:
        submission_groups.append({
            'grouper': submission,
            'list': SubmissionDetail.objects.filter(
                sid=submission.id
            ).order_by('tid')
        })

    return submission_groups


def get_visible_submission(user):
    """Get all submissions that can be viewed by the given user."""
    user = validate_user(user)
    submissions = Submission.objects.all()

    # Admin can view all submissions
    if user.has_admin_auth():
        return submissions

    # No one can view admins' submissions
    submissions = submissions.exclude(
        user__in=User.objects.filter(user_level=User.ADMIN)
    )

    # Invisible problem is
    invisible_problem = Problem.objects.filter(
        visible=False
    ).exclude(
        owner=user
    )

    # Not ended contest has something to judge
    contests = Contest.objects.filter(
        is_homework=False,
        end_time__gte=datetime.now()
    )
    for contest in contests:
        # Those who don't have contest ownership has some limitations
        if not has_contest_ownership(user, contest):
            # 1. Can't view contest owner/coowners' submission before the end
            submissions = submissions.exclude(
                Q(user__in=contest.coowner.all()) | Q(user=contest.owner),
                problem__in=contest.problem.all(),
                submit_time__gte=contest.creation_time
            )
            # 2. Can't view other contestants' submission after contest freeze
            submissions = submissions.exclude(
                user=get_contestant(contest).exclude(username=user.username),
                problem__in=contest.problem.all(),
                submit_time__gte=get_freeze_time_datetime(contest)
            )
        else:
            # Exclude contest problem from invlsible problem for owner/coowners
            invisible_problem = invisible_problem.exclude(
                id__in=contest.problem.filter(visible=False).values_list('id', flat=True)
            )

    # Invisible problems' submission can't be seen
    submissions = submissions.exclude(
        problem__in=invisible_problem
    )

    return submissions
