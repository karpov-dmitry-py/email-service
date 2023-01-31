# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.http import HttpResponse

from app.models import Customer
from app.models import Topic
from app.models import NewsLetter
from app.models import Tracking

from helpers.logger import log


# noinspection PyUnresolvedReferences,PyArgumentList
class CustomerListView(ListView):
    model = Customer
    template_name = 'app/customer_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        ctx = super(CustomerListView, self).get_context_data(**kwargs)
        ctx['title'] = 'Customers'
        return ctx


# noinspection PyUnresolvedReferences,PyArgumentList
class TopicListView(ListView):
    model = Topic
    template_name = 'app/topic_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        ctx = super(TopicListView, self).get_context_data(**kwargs)
        ctx['title'] = 'Topics'
        return ctx


# noinspection PyUnresolvedReferences,PyArgumentList
class NewsletterListView(ListView):
    model = NewsLetter
    template_name = 'app/newsletter_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        ctx = super(NewsletterListView, self).get_context_data(**kwargs)
        ctx['title'] = 'Newsletters'
        return ctx


# noinspection PyUnresolvedReferences,PyArgumentList
class TrackingListView(ListView):
    model = Tracking
    template_name = 'app/tracking_list.html'

    def __init__(self, *args, **kwargs):
        super(TrackingListView, self).__init__(*args, **kwargs)
        self.__newsletter = None
        self.__qs = None

    def get_queryset(self):
        if self.__qs is None:
            self.__newsletter = get_object_or_404(NewsLetter, pk=self.args[0])
            self.__qs = self.__newsletter.trackings.all()

        return self.__qs

    def get_context_data(self, **kwargs):
        ctx = super(TrackingListView, self).get_context_data(**kwargs)
        ctx['items'] = self.__qs
        ctx['newsletter'] = self.__newsletter
        ctx['title'] = 'Trackings'
        return ctx


# noinspection PyUnresolvedReferences
@require_GET
def handle_open_email(request, tracking_id):
    log('start handling tracking for tracking id {}'.format(tracking_id))
    trackings = Tracking.objects.filter(id=tracking_id)
    if trackings:
        tracking = trackings[0]
        if tracking.opened_at is None:
            tracking.opened_at = datetime.datetime.now()
            tracking.save()

    return HttpResponse('tracking {} handled'.format(tracking_id))


def view_email_template(request):
    from service.email_service import EmailService
    ctx = {
        'tracking_id': 100500,
        'first_name': 'John',
        'last_name': 'Doe',
        'created_at': datetime.datetime.now(),
        'topic': 'Python',
        'title': 'Python 01/23 newsletter title',
        'body': 'Python 01/23 newsletter body here ' * 10,
        'company_name': EmailService.COMPANY_NAME,
        'learn_more_url': EmailService.LEARN_MORE_URL,
        'app_base_track_url': EmailService.APP_BASE_TRACK_URL,
    }

    return render(request=request, template_name=EmailService.EMAIL_TEMPLATE_NAME, context=ctx)
