from contest.contest_info import get_running_contests
from problem.models import Submission, SubmissionDetail
from users.models import User
from utils.user_info import validate_user


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

    # During the contest, only owner/coowner can view contestants' detail
    contests = get_running_contests()

    return submissions
