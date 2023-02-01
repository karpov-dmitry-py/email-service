from django.db.models.signals import post_save

from .models import NewsLetter
from .tasks import process_newsletter


def newsletter_saved_handler(sender, instance, created, **kwargs):
    if created and instance.run_immediately:
        process_newsletter.delay(instance.pk)
        # from service.email_service import EmailService
        # EmailService.process_newsletter(newsletter_id=instance.pk)


post_save.connect(newsletter_saved_handler, NewsLetter, dispatch_uid="newsletter_saved")
