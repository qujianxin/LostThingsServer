from alive.views import hello_html, news_html
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^id=(?P<id_>\d+)/$', hello_html),
    url(r'^86id=(?P<id_>\d+)/$', news_html),   
    # for CSS/JS file to be used as static
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


