from django.conf.urls import url

from csinla_manage.views import *

urlpatterns = [
    # carfax
    url(r'^carfax/view/$', carfax_view),
    url(r'^carfax/reply_change/(?P<cfid>\d+)/$', carfax_reply_change),
    url(r'^carfax/status_change/(?P<cfid>\d+)/$', carfax_status_change),

]

        