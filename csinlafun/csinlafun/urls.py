# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from fun.views import home
from django.views.static import serve
from csinlafun.settings import MEDIA_ROOT

import xadmin
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fun/', include('fun.urls')),
    url(r'^$', home),
    url(r'^xadmin/', xadmin.site.urls),
    # 富文本编辑器
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
