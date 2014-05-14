__author__ = 'Aaron'

from django.conf.urls import url

urlpatterns = [
    url('^$', 'tickets.views.index', name='index'),
    url(r'^(?P<event_id>\d+)/$', 'tickets.views.show_event', name='show_event'),
    url(r'^(?P<event_id>\d+)/step1/$', 'tickets.views.step1', name='step1'),
    url(r'^(?P<event_id>\d+)/step2/$', 'tickets.views.step2', name='step2'),
    url(r'^(?P<event_id>\d+)/step3/$', 'tickets.views.step3', name='step3'),
    url(r'^(?P<event_id>\d+)/step4/$', 'tickets.views.step4', name='step4'),
    url(r'^logout/$', 'tickets.views.user_logout', name='logout'),
    url(r'^midstep/$', 'tickets.views.mid_step', name='midstep'),
    url(r'^setItems/$', 'tickets.views.set_itmes', name='set_items'),
    url(r'^test/$', 'tickets.views.test', name='test')
]