from __future__ import absolute_import, unicode_literals

from emailer.celery import app

from service.email_service import EmailService


@app.task()
def process_newsletter(newsletter_id):
    return EmailService.process_newsletter(newsletter_id=newsletter_id)


@app.task
def process_newsletters():
    return EmailService.process_newsletters()
