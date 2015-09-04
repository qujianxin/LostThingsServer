from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('api.urls')),
                       url(r'^', include('api.urls_statistics')),
                       url(r'^alive/', include('alive.urls')),
                       )
