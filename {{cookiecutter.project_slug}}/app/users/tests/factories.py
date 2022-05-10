from factory import Factory

from ..models import User


class UserFactory(Factory):
    class Meta:
        model = User
