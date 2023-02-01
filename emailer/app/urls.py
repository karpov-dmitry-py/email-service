from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CustomerListView.as_view(), name='customer-list'),
    url('^customer/$', views.CustomerListView.as_view(), name='customer-list'),
    url('customer/new/$', views.CustomerCreateView.as_view(), name='customer-create'),
    url('^topic/$', views.TopicListView.as_view(), name='topic-list'),
    url('^topic/new/$', views.TopicCreateView.as_view(), name='topic-create'),
    url('^newsletter/$', views.NewsletterListView.as_view(), name='newsletter-list'),
    url('^newsletter/new/$', views.NewsLetterCreateView.as_view(), name='newsletter-create'),
    url(r'^tracking/([\w-]+)/$', views.TrackingListView.as_view(), name='tracking-list'),
    url(r'^open/([\w-]+)/$', views.handle_open_email, name='handle-open-email'),
    url('template/', views.view_email_template, name='view-template'),
]
