import os
from abc import ABCMeta, abstractmethod

from django.core.mail import get_connection
from django.core.mail import send_mail
from django.template.loader import render_to_string

from app.models import Customer
from app.models import NewsLetter
from app.models import Tracking

from helpers.logger import log


class EmailServiceInterface:
    """
    Email service interface
    """
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def process_newsletter(cls, newsletter_id):
        """
        Processes a newsletter
        """
        pass

    @classmethod
    @abstractmethod
    def process_newsletters(cls):
        """
        Processes available newsletters
        """
        pass


# noinspection PyUnresolvedReferences
class EmailService(EmailServiceInterface):
    """
    Email service implementation
    """
    APP_BASE_TRACK_URL = '{}://{}:{}/open'.format(
        os.environ.get('APP_PROTOCOL'),
        os.environ.get('APP_HOST'),
        os.environ.get('APP_EXPOSED_PORT'))

    EMAIL_TEMPLATE_NAME = 'app/email_template.html'
    LEARN_MORE_URL = 'https://github.com/karpov-dmitry-py/email-service'
    COMPANY_NAME = 'it-news.org'
    __EMAIL_FROM_ADDRESS = 'updates@it-news.org'

    @classmethod
    def process_newsletter(cls, newsletter_id):
        """
        Processes a newsletter
        """
        log('start processing newsletter {}'.format(newsletter_id))
        newsletter = NewsLetter.objects.get(pk=newsletter_id)
        if newsletter.is_running:
            return

        newsletter.is_running = True
        newsletter.save()

        topic = newsletter.topic
        customers = Customer.objects.prefetch_related('topics').all()
        receivers = [customer for customer in customers if topic in customer.topics.all()]
        log('fetched {} customers to be emailed for topic {}'.format(len(customers), topic))
        if not len(receivers):
            return

        connection = get_connection(fail_silently=True)
        for customer in receivers:
            tracking = Tracking.objects.create(
                newsletter=newsletter,
                customer=customer,
            )
            log('created a tracking entry {} for newsletter id {} and customer id {}'.
                format(tracking.pk, newsletter.pk, customer.pk))

            render_ctx = {
                'id': tracking.pk,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'created_at': customer.created_at,
                'topic': topic,
                'title': newsletter.title,
                'body': newsletter.body,
                'tracking_id': tracking.pk,
                'company_name': cls.COMPANY_NAME,
                'learn_more_url': cls.LEARN_MORE_URL,
                'app_base_track_url': cls.APP_BASE_TRACK_URL,
            }

            rendered_msg = cls.__render_template(ctx=render_ctx)
            cls.__send_email(
                _to=customer.email,
                subject=newsletter.title,
                body=rendered_msg,
                connection=connection,
            )

        connection.close()
        newsletter.is_running = False
        newsletter.save()

    @classmethod
    def process_newsletters(cls):
        """
        Processes available newsletters
        """
        log('start processing available newsletters')
        newsletters = NewsLetter. \
            objects.prefetch_related('trackings'). \
            filter(run_immediately=False). \
            filter(is_running=False).all()

        for newsletter in newsletters:
            if not newsletter.trackings.count():
                cls.process_newsletter(newsletter.pk)

    @classmethod
    def __send_email(
            cls,
            _to,
            subject,
            body,
            _from=None,
            connection=None,
    ):
        """
        Sends a single email
        """

        log('sending an email to {}'.format(_to))
        _from = _from or cls.__EMAIL_FROM_ADDRESS
        return send_mail(
            subject=subject,
            message=body,
            html_message=body,
            from_email=_from,
            recipient_list=[_to],
            fail_silently=True,
            connection=connection,
        )

    @classmethod
    def __send_mass_emails(cls, messages):
        """
        Sends mass emails
        """

        connection = get_connection(fail_silently=True)
        connection.open()
        connection.send_messages(messages)
        connection.close()

    @classmethod
    def __render_template(cls, ctx, template_name=None):
        """
        Renders a template with given context
        """
        template_name = template_name or cls.EMAIL_TEMPLATE_NAME
        rendered_template = render_to_string(template_name=template_name, context=ctx)
        return str(rendered_template)
