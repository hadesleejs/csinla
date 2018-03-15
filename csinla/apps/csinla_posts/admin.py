#_*_coding:utf-8_*_
from django.contrib import admin
from .models import *
from SSO.models import IPViewResult
from django.utils.timezone import localtime
import django.utils.timezone as timezone

# Register your models here.
# admin.site.unregister(Post)


# class PostAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Post, PostAdmin)
# admin.site.unregister(Module)

# admin.site.unregister(Favourite)
# admin.site.register(Favourite)
# class ModuleAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(Module, ModuleAdmin)
# # admin.site.unregister(Favourite)
# # admin.site.register(Favourite)

class CarAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_expire')
    def is_expire(self,obj):
        if obj.expire_date<timezone.now():
            return u'已过期'
        else:
            return u'未过期'
    is_expire.short_description=u'是否过期'
admin.site.register(Car, CarAdmin)

class UsedGoodsItemInline(admin.StackedInline):
      model = UsedGoodsItem
      can_delete = True
      verbose_name_plural = 'post'
      extra=0

class UsedGoodsAdmin(admin.ModelAdmin):
    inlines =(UsedGoodsItemInline,)
    list_display = ('id','title','is_expire')
    def is_expire(self,obj):
        if obj.expire_date<timezone.now():
            return u'已过期'
        else:
            return u'未过期'
    is_expire.short_description=u'是否过期'
admin.site.register(UsedGoods,UsedGoodsAdmin)

class UsedBookItemInline(admin.StackedInline):
      model = UsedBookItem
      can_delete = True
      verbose_name_plural = 'post'
      extra=0

class UsedBookAdmin(admin.ModelAdmin):
    inlines =(UsedBookItemInline,)
    list_display = ('id','title','is_expire')
    def is_expire(self,obj):
        if obj.expire_date<timezone.now():
            return u'已过期'
        else:
            return u'未过期'
    is_expire.short_description=u'是否过期'

admin.site.register(UsedBook,UsedBookAdmin)
# admin.site.register(PostMaterial)
class PostHistoryAdmin(admin.ModelAdmin):
    search_fields = ('post__title',)
    list_display = ('id','create_time_verbose','operator_link','post','remark')

    def create_time_verbose(self,obj):
        return localtime(obj.create_time).strftime('%Y-%m-%d %H:%M:%S')
    create_time_verbose.short_description=u'创建时间'

    def operator_link(self,obj):
        return '<a href="/admin/csinla_accounts/profile/%s/change/">%s</a>' % (obj.operator.id,obj.operator)
    operator_link.allow_tags = True
    operator_link.short_description=u'操作人员'

admin.site.register(PostHistory,PostHistoryAdmin)
admin.site.register(UsedGoodsTag)
class PostMessageAdmin(admin.ModelAdmin):
    list_filter = ('message_type',)
    list_display = ('id','message_type','creator_link','create_time_verbose','post','post_link','content_text')
    def post_link(self,obj):
        return '<a href="/posts/%s/">点击跳转</a>' % obj.post.id
    post_link.allow_tags = True
    post_link.short_description=u'帖子链接'

    def creator_link(self,obj):
        return '<a href="/admin/csinla_accounts/profile/%s/change/">%s</a>' % (obj.creator.id,obj.creator)
    creator_link.allow_tags = True
    creator_link.short_description=u'发起人链接'

    def create_time_verbose(self,obj):
        return localtime(obj.create_time).strftime('%Y-%m-%d %H:%M:%S')
    create_time_verbose.short_description=u'帖子创建时间'

admin.site.register(PostMessage,PostMessageAdmin)
# class ViewRecordAdmin(admin.ModelAdmin):
#     list_filter = ('create_date','belong_to')
#     list_display = ('id','create_date','belong_to','view_count','user_count','collect_count','view_detail')

#     def view_detail(self,obj):
#         return obj.view_detail
#     view_detail.short_description=u'至今总记录'
# admin.site.register(ViewRecord,ViewRecordAdmin)

class IPViewResultAdmin(admin.ModelAdmin):
    list_filter = ('create_date','view_type')
    list_display = ('id','create_date','view_type','view_count','ip_count','user_count','user_view_count','collect_count','view_detail')

    def view_detail(self,obj):
        return obj.view_detail
    view_detail.short_description=u'至今总记录'
admin.site.register(IPViewResult,IPViewResultAdmin)

# class DistrictAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(District, DistrictAdmin)

class RentAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_expire')
    def is_expire(self,obj):
        if obj.expire_date<timezone.now():
            return u'已过期'
        else:
            return u'未过期'
    is_expire.short_description=u'是否过期'
    
admin.site.register(Rent, RentAdmin)

class Rent2Admin(admin.ModelAdmin):
    pass

admin.site.register(Rent2, Rent2Admin)

# class RentpictureAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Rentpicture, RentpictureAdmin)
admin.site.register(CarInspection)
#admin.site.register(Used)

# # admin.site.register(Rentmodule)
#
# class SencondhandAdmin(admin.ModelAdmin):
#     pass

