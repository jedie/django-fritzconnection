from django.contrib.auth.models import User
from model_bakery import baker

from djfritz.permissions import get_or_create_normal_user_group


def get_normal_pydjfritz_user(**baker_kwargs):
    pydjfritz_user_group = get_or_create_normal_user_group()[0]
    pydjfritz_user = baker.make(
        User,
        is_staff=True, is_active=True, is_superuser=False,
        **baker_kwargs
    )
    pydjfritz_user.groups.set([pydjfritz_user_group])
    return pydjfritz_user
