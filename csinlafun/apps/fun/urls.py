from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from fun.views import *
import xadmin

urlpatterns = [
    url(r'^$', home),
    url(r'^fun_home$', fun_home),
    url(r'^contact$', contact),
    url(r'^activity/view/$', activity_view),
    url(r'^activity/detail/(?P<aid>\d+)/$', activity_detail),
    url(r'^activity/add/$', activity_add),
    url(r'^activity/edit/(?P<aid>\d+)/$', ActivityEditView.as_view(),name='activity_edit'),
    url(r'^cover/image/edit/(?P<aid>\d+)/$', cover_image_edit,name='cover_image_edit'),
    url(r'^ticket/image/edit/(?P<aid>\d+)/$', ticket_image_edit,name='ticket_image_edit'),


    url(r'^activity/pay/(?P<atid>\d+)/$', activity_pay),
    url(r'^paid_success/(?P<aoid>\d+)/$', paid_success),
    url(r'^image_process/$', image_process),



]
