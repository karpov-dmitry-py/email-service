from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CustomerListView.as_view(), name='customer-list'),
    url('customers/', views.CustomerListView.as_view(), name='customer-list'),
    url('topics/', views.TopicListView.as_view(), name='topic-list'),
    url('newsletters/', views.NewsletterListView.as_view(), name='newsletter-list'),
    url(r'^tracking/([\w-]+)/$', views.TrackingListView.as_view(), name='tracking-list'),
    url(r'^open/([\w-]+)/$', views.handle_open_email, name='handle-open-email'),
    url('template/', views.view_email_template, name='view-template'),
]
