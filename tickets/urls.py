__author__ = 'Aaron'

from django.conf.urls import url

urlpatterns = [
    url('^$', 'tickets.views.index')
]