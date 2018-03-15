# coding=utf-8
# author=lijiaoshou
# date='2017/8/16 10:25'
from fun.models import *

import xadmin
from xadmin import views

class BaseSetting(object):
	enable_themes = True
	use_bootswath = True


class GlobalSettings(object):
	site_title = u'CSINLA.COM'
	site_footer = u'CSINLA.COM'
	menu_style = 'accordion'


# xadmin.site.register(Hoster)
# class ActivityTimeItemInline(xadmin.StackedInline):
#   	model = ActivityTimeItem
#   	can_delete = True
#   	verbose_name_plural = 'activitytimeitem'
#   	extra=0
#
# class ParagraphInline(xadmin.StackedInline):
#   	model = Paragraph
#   	can_delete = True
#   	verbose_name_plural = 'paragraph'
#   	extra=0
#
# class ActivityAdmin(object):
# 	inlines =(ActivityTimeItemInline,ParagraphInline)
# xadmin.site.register(Activity,ActivityAdmin)
# xadmin.site.register(ActivityTimeItem)
# xadmin.site.register(ActivityOrder)

class HosterAdmin(object):
	list_display = ['name', 'gender', 'phone','photo','email','desc']
	search_fields = ['name', 'gender', 'phone','photo','email','desc']
	list_filter = ['name', 'gender', 'phone','photo','email','desc']


class ActivityAdmin(object):
	list_display = ['name', 'hoster', 'pre_price', 'desc', 'level','is_valid','go_editor']
	search_fields = ['hoster', 'name', 'pre_price', 'desc', 'cover_image',
	                'ticket_image','level','is_valid']
	list_filter = ['hoster', 'name', 'pre_price', 'desc', 'cover_image',
	                'ticket_image','level','is_valid']


class ParagraphAdmin(object):

	list_display = ['create_time', 'activity', 'content_text', 'content_img']
	search_fields =  ['activity', 'content_text', 'content_img']
	list_filter =  ['create_time', 'activity', 'content_text', 'content_img']
	style_fields = {'content_text':'ueditor'}


class ActivityTimeItemAdmin(object):

	list_display = ['activity', 'activity_time', 'max_count','join_count']
	search_fields = ['activity', 'max_count']
	list_filter = ['activity', 'activity_time', 'max_count']


class ActivityOrderAdmin(object):
	list_display = ['create_time', 'customer_name', 'customer_email', 'order_status', 'activitytimeitem',
	                'join_count','remark','order_no']
	search_fields = ['create_time', 'customer_name', 'customer_email', 'order_status', 'activitytimeitem',
	                'join_count','remark','order_no']
	list_filter =  ['create_time', 'customer_name', 'customer_email', 'order_status', 'activitytimeitem',
	                'join_count','remark','order_no']


class ContactInfoAdmin(object):
	list_display = ['email', 'message']
	search_fields = ['email', 'message']
	list_filter = ['email', 'message']

xadmin.site.register(Paragraph,ParagraphAdmin)
xadmin.site.register(ActivityTimeItem,ActivityTimeItemAdmin)
xadmin.site.register(ActivityOrder,ActivityOrderAdmin)
xadmin.site.register(Activity,ActivityAdmin)
xadmin.site.register(ContactInfo,ContactInfoAdmin)
xadmin.site.register(Hoster,HosterAdmin)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseSetting,)