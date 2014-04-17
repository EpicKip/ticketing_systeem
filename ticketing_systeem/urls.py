from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tickets import urls
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),

    # admin site URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', include(urls))
) + staticfiles_urlpatterns()
