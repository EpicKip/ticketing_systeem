__author__ = 'Aaron'

from django.conf.urls import url

urlpatterns = [
    url('^$', 'tickets.views.index', name='index'),
    url(r'^(?P<event_id>\d+)/$', 'tickets.views.show_event', name='show_event'),
    url(r'^(?P<event_id>\d+)/step1/$', 'tickets.views.step1', name='step1'),
    url(r'^(?P<event_id>\d+)/step2/$', 'tickets.views.step2', name='step2'),
    url(r'^(?P<event_id>\d+)/step3/$', 'tickets.mollie_views.pay', name='step3'),
    url(r'^(?P<event_id>\d+)/step4/$', 'tickets.views.step4', name='step4'),
    url(r'^logout/$', 'tickets.views.user_logout', name='logout'),
    url(r'^(?P<event_id>\d+)/setItems/$', 'tickets.views.set_items', name='set_items'),
    url(r'^(?P<event_id>\d+)/mail/$', 'tickets.views.mail', name='mail'),

]