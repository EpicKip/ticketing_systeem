__author__ = 'Aaron'

from django.contrib.auth.decorators import login_required
from django.conf.urls import url

urlpatterns = [
    url('^$', 'tickets.views.index', name='index'),
    url(r'(?P<event_id>\d+)/$', 'tickets.views.show_event', name='show_event'),
    url(r'step2(?P<event_id>\d+)/$', login_required('tickets.views.step2'), name='step2'),
    url(r'step3/(?P<event_id>\d+)/$', 'tickets.views.step3', name='step3'),
    url(r'step4/(?P<event_id>\d+)/$', 'tickets.views.step4', name='step4'),
    url(r'^login/$', 'tickets.views.user_login', name='login'),
    url(r'^logout/$', 'tickets.views.user_logout', name='logout'),
]