from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),

    # admin site URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^events/', include('tickets.urls')),

    # url(r'events/(?P<event_id>\d+)/$', 'tickets.views.show_event', name='show_event'),
    #
    # url(r'events/(?P<event_id>\d+)/step2/$', 'tickets.views.step2', name='step2'),
    # url(r'events/(?P<event_id>\d+)/step3/$', 'tickets.views.step3', name='step3'),
    # url(r'events/(?P<event_id>\d+)/step4/$', 'tickets.views.step4', name='step4'),
) + staticfiles_urlpatterns()