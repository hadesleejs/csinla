from django.conf.urls import url

from api.views import *
urlpatterns = [
    url(r'^login_wx/$', Login.as_view(),name='login'),

    # accounts
    url(r'^accounts/$', home),
    url(r'^accounts/registerstu/$', registerview),
    url(r'^accounts/active/(?P<active_code>.*)/$', registerview),
    url(r'^accounts/resetpassword/$', emailpassword),
    url(r'^accounts/resetpass/$',resetpassword),
    url(r'^accounts/myinfo/$', myinfo),
    url(r'^accounts/Feedback1/$', feedback_func),
    url(r'^accounts/Feedback2/$', feedback_account),
    url(r'^accounts/Feedback3/$', feedback_exper),
    url(r'^accounts/Feedback4/$', feedback_other),
    url(r'^accounts/accountsecurity/$',accountsecurity),
    url(r'^accounts/changeavatar/$', user_avatar),
    url(r'^accounts/password/change/$', change_pass),
    url(r'^accounts/sendemail/$', again_send_email),
    url(r'^accounts/contactservice/$', contactservice),
    url(r'^accounts/protocol_get/$', protocol_get),
    url(r'^fav/$', MyFavView.as_view(),name='my_fav'),
    url(r'^comments/$', MyCommentsView.as_view(), name='my_comments'),
    url(r'^carfax/$', CarFaxView.as_view(), name='carfax'),
    url(r'^feedback/$', FeedbackView.as_view(), name='feedback'),
    url(r'^myposts/$', MyPostsView.as_view(),name='my_posts'),
    url(r'^newstu/$', NewStudentView.as_view(), name='new_stu'),
    url(r'^apply/$', ApplyPickUpView.as_view(), name='apply'),
    url(r'^myinfo/$', MyInfo.as_view(), name='my_info'),

    # curricular
    url(r'^curricular/$', curricular),
    url(r'^curricular/subjects_compare$', subjects_compare),
    # posts
    url(r'^posts/search/$', search),
    url(r'^posts/listrent/$', listrent),
    url(r'^posts/listerent/$', listerent),
    url(r'^posts/roommate/$', roommate),
    url(r'^posts/car/$', listcar),
    url(r'^posts/usedgoods/view/$', listusedgoods),
    url(r'^posts/usedgoods/add/$', usedgoods_add),
    url(r'^posts/usedbook/view/$', listusedbook),
    url(r'^posts/usedbook/add/$', usedbook_add),
    url(r'^posts/exposure/view/$', listexposure,name='listexposure'),
    url(r'^posts/exposure/add/$', exposure_add),
    url(r'^posts/(?P<posts_id>[0-9]+)/$', view_posts),
    url(r'^post/delete/(?P<pid>[0-9]+)/$', post_delete),
    url(r'^post/add/(?P<types>(rent|car|shared))/$', posts_create),
    url(r'^post/carinspect/(?P<ciid>[0-9]+)/$', carinspect),
    url(r'^post/buycar/$',buy_car),
    url(r'^post/delete/(?P<pk>[0-9]+)$', deletepost),
    url(r'^post/changepost/(?P<posts_id>[0-9]+)/$', changepost),
    url(r'^post/poststop/(?P<posts_id>[0-9]+)$', set_top),
    url(r'^post/postmessage/leave/$', postmessage_leave),
    url(r'^post/postmessage/listview/(?P<pmid>[0-9]+)/$', postmessage_listview),

    # operations
    url(r'^operations/off/(?P<posts_id>[0-9]+)/(?P<code>.*)/$', off_posts),
    url(r'^operations/stop/(?P<posts_id>[0-9]+)/(?P<code>.*)/$', stop_posts),
    url(r'^posts/second/$', second_hand,name='second_hand'),

]