from problem.models import Submission
from users.models import User
from utils.user_info import validate_user


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

    return submissions
