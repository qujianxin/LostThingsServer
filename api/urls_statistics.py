import os
from lostthings import settings

__author__ = 'hason'

from django.conf.urls import url
from api import views_statistics

urlpatterns = [
    url(r'statistics/openapp/record/$', views_statistics.record_openapp),
    url(r'statistics/login/$', views_statistics.login_statistcs),
    url(r'statistics/logout/$', views_statistics.logout_statistcs),
    url(r'statistics/index.html$', views_statistics.index_statistcs),
    url(r'css/(?P<path>.*)', "django.views.static.serve", {"document_root": os.path.join(settings.STATIC_ROOT, 'css')}),
    url(r'js/(?P<path>.*)', "django.views.static.serve", {"document_root": os.path.join(settings.STATIC_ROOT, 'js')}),
    url(r'images/(?P<path>.*)', "django.views.static.serve",
        {"document_root": os.path.join(settings.STATIC_ROOT, 'images')}),
]
