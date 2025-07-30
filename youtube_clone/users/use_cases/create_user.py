import logging

from django.db import IntegrityError, transaction

from youtube_clone.users.models import User


class CreateUserUseCase:
    def __init__(self, user_repo):
        self._logger = logging.getLogger(__name__)
        self.user_repo = user_repo

    @classmethod
    def build(
        cls,
        user_repo=User.objects,
    ):
        return cls(user_repo=user_repo)

    def validate_user_data(self, username, email):

        if self.user_repo.filter(username=username).exists():
            raise IntegrityError(f"User with username '{username}' already exists")

        if self.user_repo.filter(email=email).exists():
            raise IntegrityError(f"User with email '{email}' already exists")

    def execute(self, params: dict = {}) -> User:

        with transaction.atomic():

            username = params.get("username", None)
            email = params.get("email", None)

            self.validate_user_data(username, email)

            user = self.user_repo.create_user(
                username=username,
                password=params.get("password", None),
                email=email,
                name=params.get("name", None),
                last_name=params.get("last_name", None),
                privilege=params.get("privilege", None),
                is_active=True,
            )
            self._logger.debug(f"User ({user.id}) created!")
            return user
