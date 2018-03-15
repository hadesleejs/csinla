#_*_coding:utf-8_*_
from django.contrib import admin
from .models import *
from csinla_posts.models import Post


# Register your models here.
# admin.site.unregister(User)
# admin.site.register(User)
class PostInline(admin.StackedInline):
      model = Post
      can_delete = True
      verbose_name_plural = 'post'
      extra=0

class ProfileAdmin(admin.ModelAdmin):
    inlines =(PostInline,)
    list_filter = ('school',)
    search_fields=('username', 'student_id','email')
    list_display = ('id','username','is_active','join_ip','school','email','reg_time')
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FuncFeedback)
admin.site.register(AccountFeedback)
admin.site.register(ExperFeedback)
admin.site.register(OtherFeedback)
# admin.site.register(EmailVerifyRecord)
admin.site.register(CustomizedCar)
# admin.site.register(WxToken)
# admin.site.register(JsToken)
admin.site.register(BuyCarNotice)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id','email','message',)
admin.site.register(ContactInfo,ContactInfoAdmin)

# class CarfaxReplyInline(admin.StackedInline):
#       model = CarfaxReply
#       can_delete = True
#       verbose_name_plural = 'reply'

class CarfaxAdmin(admin.ModelAdmin):
    # inlines =(CarfaxReplyInline,)
    list_filter = ('carfax_status',)
    list_display = ('id','create_time','name','email','wechat','vin','reply_change')
    def reply_change(self,obj):
        return '<a href="/manage/carfax/reply_change/%s/">%s</a>' % (obj.id,obj.is_reply)
    reply_change.allow_tags = True
    reply_change.short_description=u'点击可修改回复状态'


class WechatInfoAdmin(admin.ModelAdmin):
    '''
    admin显示微信信息
    '''
    list_display = ('nickname','userinfo','sex','province','city','country','open_id')

admin.site.register(WechatInfo,WechatInfoAdmin)
admin.site.register(Carfax,CarfaxAdmin)
# admin.site.register(CarfaxReply)

# admin.site.register(models.Profile,ProfileAdmin)
