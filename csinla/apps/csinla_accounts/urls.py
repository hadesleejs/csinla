from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import *
from SSO.views import login as sso_login,logout as sso_logout
from django.contrib.auth.decorators import login_required
from .views import search
from operations.views import favorite_posts, list_favorite, delete_posts, off_posts, stop_posts, Read_notice
urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),

    # auth
    url(r'^login/$', sso_login, name='login'),
    url(r'^unregisteredlogin951127/$', Login2.as_view()),
    url(r'^registerstu/$', RegisterView.as_view(), name='registerstu'),
    url(r'^register/$', views.reg_type, name='register'),
    url(r'^registersuccess/$', views.register_success, name='registersuccess'),
    url(r'^logout/$', sso_logout, name='logout'),
    url(r'^resetforgotpassword/$', views.ResetForgot.as_view(), name='resetPassword'),
    # my posts
    url(r'^myPosts/list$',login_required(views.ListMyPosts), name='myPosts'),
    # list my favourite posts
    #url(r'^myFavourites/list$',views.ListMyFavourites.as_view(),name='myFavourites'),
    # follow
    url(r'^search/$', search, name='search'),
    url(r'^favorite/add(?P<posts_id>[0-9]+)', favorite_posts, name='addFavorite'),
    url(r'^follow/del(?P<posts_id>[0-9]+)', delete_posts, name='delFollows'),
    url(r'^myfavorite/list$',list_favorite, name='myFavorites'),
    # url(r'^follow/add/(?P<follows>[0-9]+)$', views.Follow.as_view(), name='follow'),
    url(r'^follow/add/$', views.Follow.as_view(), name='follow'),

    url(r'^follow/listMyFans', views.ListMyFans, name='myFans'),
    #url(r'^follow/listMyFollows', login_required(views.ListMyFollows.as_view()), name='myFollows'),
    url(r'^accountsecurity/$', login_required(views.AccountSecurity.as_view()), name='accountSecurity'),
    url(r'^changeavatar/$', views.user_avatar),
    # url(r'^follow/search/$', views.SearchFans.as_view(), name='Fansearch'),
    # url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',views.Active_user,name='Active_user'),
    url(r'^myinfo/$', login_required(views.MyInfo.as_view()), name='myInfo'),
    url(r'^myhelpcenter/$', login_required(views.MyHelpCenter.as_view()), name = 'myhelpcenter'),
    url(r'^myhelp/$', login_required(views.MyHelp.as_view()), name = 'myhelp'),
    #  Handle user feedback
    url(r'^Feedback1/$', views.feedback_func),
    url(r'^Feedback2/$', views.feedback_account),
    url(r'^Feedback3/$', views.feedback_exper),
    url(r'^Feedback4/$', views.feedback_other),
     #
    url(r'^sendemail/$', views.again_send_email, name='sendemail'),
    url(r'^off/(?P<posts_id>[0-9]+)/(?P<code>.*)/$', off_posts),
    url(r'^stop/(?P<posts_id>[0-9]+)/(?P<code>.*)/$', stop_posts),
    url(r'^deletenotice/$', Read_notice),
    url(r'^resetpass/$', ResetPassword.as_view()),
    url(r'^privacypolicy/$', privacypolicy),
    url(r'^airport/$', airport),
    url(r'^parking/$', parking),
    url(r'^parking2/$', parking2),
    url(r'^salecar/$', salecar),
    url(r'^carfax/$', carfax),
    url(r'^company/$', company),
    # url(r'^newstudent/$', ApplyForPickUpView,name='pickup'),
    url(r'^newstudent/$',ApplyForPickUpView.as_view(),name='apply_for_pickup'),
    url(r'^add_apply/$', AddApplyPickUpView.as_view(), name='add_apply'),
    url(r'^add_comments/$', AddCommentView.as_view(), name='add_comments'),
    url(r'^search/$', SearcheDriverView.as_view(), name='search_drive'),
    url(r'^add_sub/$', AddSubmissionView.as_view(), name='add_sub'),
    url(r'^entrance/$', EntranceView.as_view(), name='entrance'),
    url(r'^license/$',DriveView.as_view(),name='license'),
    url(r'^activity/$',activity,name='activity'),
    url(r'^test/$', test_page, name='test'),
    url(r'^feedback/$', UserFeedbackView.as_view(), name='feedback'),
    url(r'^search1/$', search, name='search_new'),

]


