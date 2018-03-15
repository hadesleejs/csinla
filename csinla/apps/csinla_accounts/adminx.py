# coding=utf-8
# author=lijiaoshou
# date='2017/7/15 10:58'

from .models import *
import xadmin
from xadmin import views

class BaseSetting(object):
	enable_themes = True
	use_bootswath = True

class GlobalSettings(object):
	site_title = u'CSINLA.COM'
	site_footer = u'CSINLA.COM'
	menu_style = 'accordion'


class CustomizedCarAdmin(object):
	list_display = ['author','car_type','car_type_other','brand','vehicle_age','vehicle_miles']
	search_fields = ['author','car_type','car_type_other','brand','vehicle_age','vehicle_miles']
	list_filter = ['author','car_type','car_type_other','brand','vehicle_age','vehicle_miles']


class CarfaxAdmin(object):
	list_display = ('id', 'create_time', 'name', 'email', 'wechat', 'vin')
	search_fields = ['creator', 'vin', 'name', 'email', 'wechat','is_reply']
	list_filter = ['create_time', 'creator', 'vin', 'name', 'email', 'wechat','is_reply','unreply_time']
	ordering = ['-create_time']

class WechatInfoAdmin(object):
	list_display = ['userinfo','open_id','unionid','scene_id','nickname','headimgurl','sex',
	                'province','city','country']
	search_fields = ['userinfo','open_id','unionid','scene_id','nickname','headimgurl','sex',
	                'province','city','country']
	list_filter = ['userinfo','open_id','unionid','scene_id','nickname','headimgurl','sex',
	                'province','city','country']


class ContactInfoAdmin(object):
    list_display = ('id','email','message',)



class ApplyForPickupAdmin(object):
	list_display = ['name','sex','wx','phone','email','flight',
	                'departure','departure_type', 'landing','landing_type', 'address']
	search_fields = ['name','sex','wx','phone','email','flight',
	                'contactor', 'contacts_phone', 'address']
	list_filter = ['name','sex','wx','phone','email','flight',
	                'departure','landing','address']


class NewStudentCommentAdmin(object):
	list_display = ['comments', 'fav_nums', 'belong', 'user']
	search_fields = ['comments', 'fav_nums', 'belong', 'user']
	list_filter = ['comments', 'fav_nums', 'belong', 'user']


class NewStudentSubmissionAdmin(object):
	list_display = ['title', 'content','content_detail' ,'img', 'url','user','belong','is_valid']
	search_fields = ['title', 'content', 'img', 'url','user','belong']
	list_filter = ['title', 'content', 'img', 'url','user','belong']
	style_fields = {"content_detail":"ueditor"}


class DriveExamnationAdmin(object):
	list_display = ['t_id', 'content', 'bingo']
	search_fields = ['t_id', 'content', 'bingo']
	list_filter = ['t_id', 'content', 'bingo']


class SubmissionPictureAdmin(object):
	list_display = ['post', 'image']
	search_fields = ['post', 'image']
	list_filter = ['post', 'image']


class ApplyEmailAdmin(object):
	list_display = ['belong', 'email','name']
	search_fields = ['belong', 'email','name']
	list_filter = ['belong', 'email','name']


class ApplyUrlAdmin(object):
	list_display = ['url', 'belong','name']
	search_fields = ['url', 'belong','name']
	list_filter = ['url', 'belong','name']

xadmin.site.register(ApplyUrl,ApplyUrlAdmin)
xadmin.site.register(ApplyEmail,ApplyEmailAdmin)
xadmin.site.register(SubmissionPicture,SubmissionPictureAdmin)
xadmin.site.register(ContactInfo,ContactInfoAdmin)
xadmin.site.register(NewStudentComment,NewStudentCommentAdmin)
xadmin.site.register(NewStudentSubmission,NewStudentSubmissionAdmin)
xadmin.site.register(ApplyForPickup,ApplyForPickupAdmin)

xadmin.site.register(WechatInfo,WechatInfoAdmin)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseSetting,)
xadmin.site.register(Carfax,CarfaxAdmin)
xadmin.site.register(CustomizedCar,CustomizedCarAdmin)


xadmin.site.register(FuncFeedback)
xadmin.site.register(AccountFeedback)
xadmin.site.register(ExperFeedback)
xadmin.site.register(OtherFeedback)
# admin.site.register(EmailVerifyRecord)
# xadmin.site.register(CustomizedCar)
# admin.site.register(WxToken)
# admin.site.register(JsToken)
xadmin.site.register(BuyCarNotice)