# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # view post detail
    url(r'^(?P<posts_id>[0-9]+)/$', views.view_posts, name='detail'),

    # create a new post
    url(r'^add/$', views.type_select, name='add'),

    url(r'^add/(?P<types>(rent|car|shared|entire_rent))/$', views.posts_create, name='add'),
    url(r'^addsuccess/$',views.success_notice, name='addsuccess'),
    url(r'^complete/(?P<pk>[0-9]+)$', views.success_notice, name='complete_post'),
    url(r'^buycar/$', views.buy_car, name='buycar'),
    url(r'changepost/(?P<posts_id>[0-9]+)/$', views.ChangePost.as_view(), name='changeposts'),
    # list posts by module
    # url(r'^listPosts/(?P<belong_to>[0-9]+)/$', views.posts_view, name='list'),
    # 整租url配置
    url(r'^list_entire_rent/$', views.ListEntireRent.as_view(), name='list_entire_rent'),

    url(r'^listRent/$', views.ListRent.as_view(), name='listrent'),
    url(r'^Roommate/$', views.RoomMate.as_view(), name='roommate'),
    url(r'^Car/$', views.ListCar.as_view(), name='car'),
    url(r'^CarInspect/(?P<ciid>[0-9]+)/$', views.CarInspect.as_view(), name='carinspect'),


    # delete one post
    url(r'^delete/(?P<pk>[0-9]+)$', views.DeletePost.as_view(), name='delete'),

    #
    url(r'^newposts/$', views.new_posts, name='new_posts'),
    url(r'^poststop/(?P<posts_id>[0-9]+)$', views.set_top, name='settop'),
    url(r'^add233/$', views.CreatePosts2.as_view(), name='add'),
    url(r'^used/$', views.CreateUsed.as_view()),

    url(r'^usedgoods/view/$', views.ListUsedGoods.as_view()),
    url(r'^usedgoods/add/$', views.usedgoods_add),

    url(r'^usedbook/view/$', views.ListUsedBook.as_view()),
    url(r'^usedbook/add/$', views.usedbook_add),

    url(r'^exposure/view/$', views.ListExposure.as_view()),
    url(r'^exposure/add/$', views.exposure_add),

    url(r'^postmessage/leave/$', views.postmessage_leave),
    url(r'^postmessage/listview/(?P<pmid>[0-9]+)/$', views.postmessage_listview),
    url(r'^post/delete/(?P<pid>[0-9]+)/$', views.post_delete),


]
