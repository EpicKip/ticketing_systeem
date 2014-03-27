from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),

    # admin site URLS
    url(r'^admin/', include(admin.site.urls)),

)
