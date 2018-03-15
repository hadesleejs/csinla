# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from csinla_accounts.views import Home, change_pass,test_page,temp_home
from csinla_posts.views import search, CarInspect
from csinla_accounts.views import SearchFans
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from csinla_accounts.views import ActiveUserView, wx_js, EmailPassword, ResetPassword, send_done, reset_done,contactservice,wx_login
from SSO.views import login,logout,json_login,json_logout,ticket_login
import  xadmin
import os
from django.views.static import serve
from controller import handler
urlpatterns = [
    # home page
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^wx_login/$', wx_login, name='wx_login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^json_login/$', json_login, name='json_login'),
    url(r'^ticket_login/$', ticket_login, name='json_login'),
    url(r'^json_logout/$', json_logout, name='json_logout'),
    # url(r'^$', temp_home, name='home'),    
    # search
    url(r'^search/', include('haystack.urls')),
    # url for apps
    url(r'^accounts/', include('csinla_accounts.urls', namespace='accounts', app_name='csinla_accounts')),
    url(r'^posts/', include('csinla_posts.urls', namespace='posts', app_name='csinla_posts')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^curricular/', include('csinla_curricular.urls')),
    url(r'^manage/', include('csinla_manage.urls')),
    url(r'^api/', include('api.urls')),
    #url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/',xadmin.site.urls),
    url(r'^follow/search/$', SearchFans.as_view(), name='Fansearch'),

    #url(r'^password/change/$', auth_views.password_change, name='password_change'),change_pass
    url(r'^password/change/$', change_pass, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    
    url(r'^resetpassword/$', EmailPassword.as_view(), name='password_reset'),
    url(r'^resetpassword/passwordsent/$', send_done, name='password_reset_done'),
    url(r'^reset/done/$', reset_done, name='password_reset_complete'),
    url(r'^reset/(?P<code>.*)/$', ResetPassword.as_view(), name='password_reset_confirm'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^contactservice/$', contactservice, name="contactservice"),
    url(r'^test/$', CarInspect.as_view()),
    url(r'^test_page/$', test_page),
    url(r'^MP_verify_4QswHXCZFX1CLJUS.txt/$', wx_js),
    url(r'^UE/(?P<path>.*)$',serve, { 'document_root':os.path.join(os.path.dirname(__file__).replace('\\','/')+"/UE")}),
    url(r'^upload/(?P<path>.*)$', serve,{ 'document_root': os.path.join(os.path.dirname(__file__)+"/upload").replace('\\','/') }),
    url(r'ueEditorControler',handler),
    url(r'^test1/$', test_page, name='test'),
    # url(r'^search/', include('haystack.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
