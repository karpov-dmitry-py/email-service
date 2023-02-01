import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABCMeta, abstractmethod

from django.core.mail import get_connection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app.models import Customer
from app.models import NewsLetter
from app.models import Tracking

from helpers.logger import log
from helpers.logger import error


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

        cls.__toggle_newsletter_state(newsletter)
        topic = newsletter.topic
        customers = Customer.objects.prefetch_related('topics').all()
        receivers = [customer for customer in customers if topic in customer.topics.all()]
        log('fetched {} customer(s) to be emailed for newsletter {}'.format(len(receivers), newsletter))
        if not len(receivers):
            return

        conn, err = cls.__new_smtp_conn()
        if err:
            error(err)
            return

        for customer in receivers:
            tracking = Tracking.objects.create(
                newsletter=newsletter,
                customer=customer,
            )
            log('created tracking {} for newsletter {} and customer {}'.
                format(tracking.pk, newsletter.pk, customer))

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
            send_err = cls.__send_email_with_smtplib(
                _to=customer.email,
                subject=newsletter.title,
                body=rendered_msg,
                conn=conn,
            )

            if isinstance(send_err, dict) and len(send_err):
                cls.__append_sending_error_to_tracking(
                    tracking=tracking,
                    error_on_send=str(send_err.get(customer.email, ''))
                )

        conn.quit()

        cls.__toggle_newsletter_state(newsletter)

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
        Sends a single email with django built-in functionality (an error occurs when sending emails from within celery)
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
    def __send_email_with_smtplib(
            cls,
            _to,
            subject,
            body,
            conn,
            _from=None,

    ):
        """
        Sends a single email with smtplib standard library and returns result as dict: {'_to': (error_code, error_text)}
        """

        _from = _from or cls.__EMAIL_FROM_ADDRESS

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = _from
        message["To"] = _to

        text = strip_tags(body)
        html = body

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        log('sending an email to {} ...'.format(_to))
        return conn.sendmail(_from, _to, message.as_string())

    @classmethod
    def __new_smtp_conn(cls):
        """
        Creates a new smtp connection with given credentials
        """

        host = os.environ.get('EMAIL_HOST')
        port = os.environ.get('EMAIL_PORT')
        login = os.environ.get('EMAIL_HOST_USER')
        password = os.environ.get('EMAIL_HOST_PASSWORD')

        server_address = '{}:{}'.format(host, port)
        log('connecting to smtp server: {} with user {} ... '.format(server_address, login))

        try:
            conn = smtplib.SMTP(server_address)
            conn.starttls()
            conn.login(login, password)
            return conn, None
        except Exception as e:
            return None, 'failed to connect to mail server {}, err: {}'.format(server_address, str(e))

    @classmethod
    def __send_mass_emails(cls, messages):
        """
        Sends mass emails with django built-in functionality
        """

        connection = get_connection(fail_silently=True)
        connection.open()
        connection.send_messages(messages)
        connection.close()

    @classmethod
    def __render_template(cls, ctx, template_name=None):
        """
        Renders a template to raw html with given context
        """

        template_name = template_name or cls.EMAIL_TEMPLATE_NAME
        rendered_template = render_to_string(template_name=template_name, context=ctx)
        return str(rendered_template)

    @staticmethod
    def __toggle_newsletter_state(newsletter):
        """
        Toggles a newsletter instance's running state
        """

        newsletter.is_running = not newsletter.is_running
        newsletter.save()

    @staticmethod
    def __append_sending_error_to_tracking(tracking, error_on_send):
        """
        Appends a sending error to a tracking instance
        """

        tracking.error_on_send = error_on_send
        tracking.save()
