import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.core.management import CommandError

from helpers.logger import log


class Command(BaseCommand):
    """Creates a superuser"""

    def handle(self, *args, **options):
        user_name = os.environ.get('ADMIN_USER_NAME')
        user_email = os.environ.get('ADMIN_USER_EMAIL')
        user_password = os.environ.get('ADMIN_USER_PASSWORD')

        if not all([user_name, user_email, user_password]):
            raise CommandError("all user data (name, email, password) is required to be set in app's .env file")

        log('querying db for user {} ...'.format(user_name))
        exists = User.objects.filter(username=user_name).exists()
        if exists:
            log('db already has user {}'.format(user_name))
            return

        User.objects.create_superuser(user_name, user_email, user_password)
        log('successfully created superuser {} with email {}'.format(user_name, user_email))
