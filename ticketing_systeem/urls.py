from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),

    # admin site URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^events/', include('tickets.urls')),

    # login page
    url(r'^accounts/login/$', 'tickets.views.user_login', name='login'),

    # register page
    url(r'^accounts/register/$', 'tickets.views.register', name='register'),

    # terms & conditions page
    url(r'^termsandconditions/$', 'tickets.views.terms', name='terms'),

    # Mollie webhook
    url(r'^webhook/$', 'tickets.mollie_views.pay_report', name='webhook'),
) + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
