# coding=utf-8
# author=lijiaoshou
# date='2017/7/15 9:43'
import xadmin
from .models import Post,PostHistory,PostMessage,MessageImageItem,PostMaterial,Car
from .models import *


class PostAdmin(object):
	list_display = ['title','author','belong_to','post_date','expire_date','content']
	search_fields = ['title','author','belong_to','content']
	list_filter = ['title','author','belong_to','post_date','expire_date','content']
	ordering = ['-post_date']


class PostHistoryAdmin(object):
	list_display = ['post', 'operator', 'create_time', 'remark','go_to']
	search_fields = ['post', 'operator', 'remark']
	list_filter = ['post', 'operator', 'create_time', 'remark']
	ordering = ['-create_time']


class PostMessageAdmin(object):
	list_display = ['post', 'create_time', 'creator', 'content_text', 'message_type', 'reply_message','go_to']
	search_fields = ['post', 'creator', 'content_text', 'message_type', 'reply_message']
	list_filter = ['post', 'create_time', 'creator', 'content_text', 'message_type', 'reply_message']
	ordering = ['-create_time']

class PostMaterialAdmin(object):
	list_display = ['create_time', 'level', 'material_status', 'material_type', 'content_text', 'content_image']
	search_fields = ['level', 'material_status', 'material_type', 'content_text', 'content_image']
	list_filter = ['create_time', 'level', 'material_status', 'material_type', 'content_text', 'content_image']
	ordering = ['-create_time']

class CarAdmin(object):
	list_display = ['car_id', 'car_type', 'car_type_other', 'brand', 'vehicle_age', 'vehicle_miles','fee','fee2',
                    'price','price2','level_type']
	search_fields = ['car_id', 'car_type', 'car_type_other', 'brand', 'vehicle_age', 'vehicle_miles','fee','fee2',
                    'price','price2','level_type']
	list_filter = ['car_id', 'car_type', 'car_type_other', 'brand', 'vehicle_age', 'vehicle_miles','fee','fee2',
                    'price','price2','level_type']
	ordering = ['-post_date']
	def is_expire(self, obj):
		if obj.expire_date < timezone.now():
			return u'已过期'
		else:
			return u'未过期'

	is_expire.short_description = u'是否过期'


class UsedBookItemInline(object):
      model = UsedBookItem
      can_delete = True
      verbose_name_plural = 'post'
      extra=0

class UsedBookAdmin(object):
    inlines =(UsedBookItemInline,)
    list_display = ('id','title','is_expire')
    ordering = ['-post_date']
    def is_expire(self,obj):
        if obj.expire_date<timezone.now():
            return u'已过期'
        else:
            return u'未过期'
    is_expire.short_description=u'是否过期'


class CarInspectionAdmin(object):
	list_display = ['car', 'engine', 'engine_content', 'transmission','transmission_content',
					'light', 'light_content', 'colour', 'colour_content']
	search_fields = ['car', 'engine', 'engine_content', 'transmission','transmission_content',
	                'light', 'light_content', 'colour', 'colour_content']
	list_filter = ['car', 'engine', 'engine_content', 'transmission',
	               'transmission_content','light', 'light_content', 'colour', 'colour_content']


class RentAdmin(object):
	list_display = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	search_fields = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	list_filter = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	ordering = ['-post_date']
	def is_expire(self, obj):
		if obj.expire_date < timezone.now():
			return u'已过期'
		else:
			return u'未过期'

	is_expire.short_description = u'是否过期'


class Rent2Admin(object):
	list_display = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other', 'fee',
	                'house_type', 'house_type_other', 'pet', 'smoke']
	search_fields = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other', 'fee',
	                 'house_type', 'house_type_other', 'pet', 'smoke']
	list_filter = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other', 'fee',
	               'house_type', 'house_type_other', 'pet', 'smoke']
	ordering = ['-post_date']
class RentEntireAdmin(object):
	list_display = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	search_fields = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	list_filter = ['house_id', 'rent_begins', 'rent_ends', 'district', 'district_other','fee',
	                'share','house_type','house_type_other','pet','smoke']
	ordering = ['-post_date']
	def is_expire(self, obj):
		if obj.expire_date < timezone.now():
			return u'已过期'
		else:
			return u'未过期'

	is_expire.short_description = u'是否过期'

# class UsedAdmin(object):
# 	list_dispaly = ['Name','Content']
# 	search_fields = ['Name','Content']
# 	list_filter = ['Name','Content']


class UsedGoodsItemInline(object):
      model = UsedGoodsItem
      can_delete = True
      verbose_name_plural = 'post'
      extra=0

class UsedGoodsAdmin(object):
	list_display = ['tags','used_id','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	search_fields = ['tags','used_id','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	list_filter = ['tags','used_id','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	ordering = ['-post_date']

class UsedAdmin(object):
	list_display = ['used_id','tags','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	search_fields = ['tags','used_id','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	list_filter = ['tags','used_id','district','address','connect_name','connect_phone','connect_wx',
	                'content_detail']
	ordering = ['-post_date']


class IPViewResultAdmin(object):
    list_filter = ('create_date','view_type')
    list_display = ('id','create_date','view_type','view_count','ip_count','user_count','user_view_count','collect_count','view_detail')
    ordering = ['-create_date']
    def view_detail(self,obj):
        return obj.view_detail
    view_detail.short_description=u'至今总记录'


xadmin.site.register(Used,UsedAdmin)
xadmin.site.register(EntireRent,RentEntireAdmin)
xadmin.site.register(IPViewResult,IPViewResultAdmin)
xadmin.site.register(UsedGoodsTag)

# xadmin.site.register(Used,UsedAdmin)
xadmin.site.register(UsedGoods,UsedGoodsAdmin)
xadmin.site.register(Rent2,Rent2Admin)
xadmin.site.register(Rent,RentAdmin)
xadmin.site.register(CarInspection,CarInspectionAdmin)
xadmin.site.register(Car,CarAdmin)
xadmin.site.register(PostMaterial,PostMaterialAdmin)
xadmin.site.register(PostMessage,PostMessageAdmin)
xadmin.site.register(Post,PostAdmin)
xadmin.site.register(PostHistory,PostHistoryAdmin)
xadmin.site.register(UsedBook,UsedBookAdmin)
