from lostthings import settings

__author__ = 'hanson'
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'api/member/regist/$', views.regist_member),
    url(r'api/member/login/$', views.login_member),
    url(r'api/member/logout/$', views.logout_member),
    url(r'api/member/get/$', views.get_member),
    url(r'api/member/patch/$', views.patch_member),
    url(r'api/messages/operate/$', views.operate_message),
    url(r'api/messages/add/$', views.add_message),
    url(r'api/messages/get/$', views.get_messages),
    url(r'api/messages/get_one/$', views.get_one_message),
    url(r'api/news/get_one/$', views.get_one_news),
    url(r'api/comments/get/$', views.get_comments),
    url(r'api/news/add/$', views.add_news),
    url(r'api/news/get/$', views.get_news),
    url(r'api/news/operate/$', views.operate_news),
    url(r'api/words/add/$', views.add_words),
    url(r'api/words/get/$', views.get_words),
    url(r'api/words/delete/$', views.delete_words),
    url(r'api/system_messages/get/$', views.get_system_msg),
    url(r'api/replies/get/$', views.get_replies),
    url(r'api/update/get/$', views.get_update),
    url(r'api/feedback/$', views.feedback),
    url(r'api/member/commited/$', views.get_commited),
    url(r'api/verify_phone/$', views.verify_phone),
    url(r'api/member/exist/$', views.check_person_exist),
    url(r'api/ambassador/get/$', views.get_ambassadors),
    url(r"media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),

]
