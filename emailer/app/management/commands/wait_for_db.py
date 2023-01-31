import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand

from helpers.logger import log


class Command(BaseCommand):
    """Waits for db to run migrations"""

    def handle(self, *args, **options):
        log('waiting for db ...')
        secs = 1
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:

                log('db is still unavailable, waiting for {} second ...'.format(secs))
                time.sleep(secs)

        time.sleep(secs)
        log('db is ready')
