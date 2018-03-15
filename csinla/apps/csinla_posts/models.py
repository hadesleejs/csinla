#_*_ encoding: utf-8 _*_
from __future__ import unicode_literals
import datetime
import os
import re
import threading
import cStringIO
import urllib2
import json
import time

import django.utils.timezone as timezone
# from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from decimal import Decimal
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete
from django_comments.models import Comment
from django_comments.signals import comment_was_posted
from DjangoUeditor.models import UEditorField

from utils.email_send import send_util,send_util2

from csinla_accounts.models import Profile
from SSO.models import IPViewResult
class Post(models.Model):
    title = models.TextField(u'标题',max_length=40,default='')
    author = models.ForeignKey(Profile, verbose_name=u"作者",on_delete=models.CASCADE,related_name='posts',null=True,blank=True)
    belong_to = models.CharField(u'帖子类型',max_length=20,default=u'二手车')
    post_date = models.DateTimeField(u'发帖时间',default=timezone.now)
    expire_date = models.DateTimeField(u'到期时间',default=timezone.now()+datetime.timedelta(days=30))
    active = models.DateTimeField(default=timezone.now)
    reply_num = models.IntegerField(default=0)
    content = models.TextField(u'内容',null=True, blank=True)
    phone = models.CharField(u'联系电话',max_length=15,default='0')
    weixin = models.CharField(u"联系微信",max_length=35, default='0')
    is_top = models.BooleanField(u'是否置顶',default=False)
    is_notice = models.BooleanField(u'是否通知',default=True)
    last_change_time=models.DateTimeField(u'最后修改时间',auto_now=True)
    is_sys=models.BooleanField(u'是否系统用户发帖',default=False)
    
    class Meta:
        ordering = ["post_date"]
        verbose_name = u'帖子'
        verbose_name_plural = verbose_name

    def get_date(self):
        delta = self.expire_date - timezone.now()     
        return '%d天%d小时' % (delta.days,(delta.seconds / 60 / 60))
    def is_date(self):
        return timezone.now() < self.expire_date 

    @property
    def is_limitless(self):
        if self.belong_to in [u'二手商品',u'二手书']:
            return True
        else:
            return False

    @property
    def is_today(self):
        create_date=self.post_date.date()
        if create_date==datetime.date.today():
            return True
        return False

    @property
    def sys_reply_str(self):
        return u'系统用户发帖'
        totle_list=self.postmessage_set.filter(message_type='REPLY',is_valid=True)
        sys_list=totle_list.filter(creator__first_name=u'系统用户')
        normal_list=totle_list.exclude(creator__first_name=u'系统用户')
        sys_read_list=sys_list.filter(has_read=True)
        normal_read_list=normal_list.filter(has_read=True)

        total_count=totle_list.count()
        normal_count=normal_list.count()
        normal_read_count=normal_read_list.count()
        normal_unread_count=normal_count - normal_read_count
        sys_count=sys_list.count()
        sys_read_count=sys_read_list.count()
        sys_unread_count=sys_count - sys_read_count

        reply_str=u'评论共%s条，%s条系统用户评论（%s未读，%s已读），%s条普通用户评论（%s未读,%s已读）' % (total_count,sys_count,sys_read_count,sys_unread_count,normal_count,normal_read_count,normal_unread_count)
        return reply_str

    @property
    def reply_message_list(self):
        return self.postmessage_set.filter(message_type='REPLY',reply_message__isnull=True)

    @property
    def last_reply(self):
        if self.postmessage_set.filter(message_type='REPLY',reply_message__isnull=True).exists():
            return self.postmessage_set.filter(message_type='REPLY',reply_message__isnull=True).order_by('-create_time')[0]
        else:
            return None

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', args=[str(self.id)])
       


    def save(self, *args, **kwargs):
        is_first=False
        is_notice_cancel=False
        if self.is_limitless:
            self.expire_date=timezone.now()+datetime.timedelta(days=3600)
        if self.author.first_name==u'系统用户':
            if not self.is_sys:
                self.is_sys=True
        else:
            if self.is_sys:
                self.is_sys=False
        if not self.id:
            is_first=True
        else:
            post=Post.objects.get(id=self.id)
            if self.is_notice==False and post.is_notice!=self.is_notice:
                is_notice_cancel=True
        super(Post, self).save(*args, **kwargs)
        if is_first:
            PostHistory.objects.create(operator=self.author,post=self,remark=u'用户【%s】创建本人帖子【%s】' % (self.author,self))
        if is_notice_cancel:
            PostHistory.objects.create(operator=self.author,post=self,remark=u'用户【%s】取消本人帖子【%s】的消息通知' % (self.author,self))

    def times(self):
        return {
            'time':self.post_date.strftime('%X'),
            'day':self.post_date.strftime("%Y/%m/%d"),
        }


    def images(self):
        # 获取图片URL
        images_url = []
        pics = self.rentpicture_set.all()
        for pic in pics:
            images_url.append(pic.image.url)
        return  images_url
    def pic_nums(self):
        nums = self.rentpicture_set.all().count()
        return  nums
class PostHistory(models.Model):
    post=models.ForeignKey(Post,verbose_name=u'对应帖子')
    operator=models.ForeignKey(Profile,verbose_name=u'操作人员')
    create_time=models.DateTimeField(u'操作时间',auto_now_add=True)
    remark=models.TextField(u'操作内容')
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('''<a href='http://www.csinla.com/posts/%s'>跳转到帖子</a>'''%(self.post.id))
    go_to.short_description =  "跳转"
    class Meta:
        verbose_name = u"帖子历史记录"
        verbose_name_plural = verbose_name
        ordering=["-create_time"]

    def __unicode__(self):
        return u'【%s】%s：%s' % (self.post,self.create_time,self.remark)
            


class PostMessage(models.Model):
    post=models.ForeignKey(Post,verbose_name=u'对应帖子')
    create_time = models.DateTimeField(u'互动创建时间', auto_now_add=True)
    creator = models.ForeignKey(Profile, verbose_name=u'发起者')
    content_text=models.TextField(u'内容',default='')
    MESSAGE_TYPES = (
        ('COLLECT', u'收藏'),
        ('REPLY', u'回复'),
    )
    message_type = models.CharField(
        u'互动类型', max_length=24, choices=MESSAGE_TYPES, default='COMMENT')
    reply_message = models.ForeignKey(
        'self', verbose_name=u'回复的留言', blank=True, null=True)
    floor=models.IntegerField(u'楼层',default=0)
    is_valid = models.BooleanField(u'是否有效', default=True)
    has_read=models.BooleanField(u'是否已查看',default=False)
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('''<a href='http://www.csinla.com/posts/%s'>跳转到帖子</a>'''%(self.post.id))
    go_to.short_description =  "跳转"
    class Meta:
        verbose_name = u"帖子互动"
        verbose_name_plural = verbose_name
        ordering=["-create_time"]

    @property
    def reply_message_list(self):
        message_list = PostMessage.objects.none()
        if self.message_type == 'REPLY':
            temp_list = self.postmessage_set.all()
            message_list = message_list | temp_list
            for item in temp_list:
                message_list = message_list | item.reply_message_list
        return message_list.order_by('create_time')

    @property
    def reply_message_list_top5(self):
        return self.reply_message_list[:5]

    @property
    def floor_message(self):
        if self.reply_message:
            return self.reply_message.floor_message
        else:
            return self

    @property
    def reply_text(self):
        if self.reply_message:
            if self.reply_message.creator!=self.floor_message.creator:
                return u'回复 %s：%s' % (self.reply_message.creator,self.content_text)
        return self.content_text

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'creator_avatar_url':self.creator.avatar.url,
            'creator':str(self.creator),
            'reply_text': self.reply_text,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M'),
        }

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        is_first=False
        is_collect=False
        if not self.id:
            is_first=True
        if self.message_type=='REPLY' and self.floor==0:
            self.floor=self.post.postmessage_set.filter(message_type='REPLY',reply_message__isnull=True).count()+2
        if self.message_type=='COLLECT':
            if not self.id:
                is_collect=True
            else:
                postmessage=PostMessage.objects.get(id=self.id)
                if self.is_valid and postmessage.is_valid!=self.is_valid:
                    is_collect=True
        super(PostMessage, self).save(*args, **kwargs)
        if is_collect:
            try:
                ipviewresult=IPViewResult.objects.get(create_date=datetime.date.today(),view_type=self.post.belong_to)
            except IPViewResult.DoesNotExist:
                ipviewresult=IPViewResult.objects.create(create_date=datetime.date.today(),view_type=self.post.belong_to)
            ipviewresult.collect_count=ipviewresult.collect_count+1
            ipviewresult.save()
            if self.post.is_notice:
                t = threading.Thread(target=send_util, args=('',self.post.author.username, self.post.belong_to, self.post.title, self.post.author.email, self.post.id,self.creator.username))
                t.start()
        if self.message_type=='REPLY':
            if self.post.is_limitless:
                self.post.save()
            if is_first:
                if not  self.reply_message:
                    if self.post.is_notice:
                        t = threading.Thread(target=send_util2, args=('',self.post.author.username, self.post.belong_to, self.post.title, self.post.author.email, self.post.id,self.content_text))
                        t.start()
                else:
                    reply_message=self.reply_message
                    reply_message.has_read=True
                    reply_message.save()

    # @property
    # def content_image_list(self):
    #     pattern = re.compile(r'<img[^>]*src[=\"\']+([^\"\']*)[\"\'][^>]*>', re.I) 
    #     # pattern = re.compile("<img\\b[^>]*\\bsrc\\b\\s*=\\s*('|\")?([^'\"\n\r\f>]+(\\.jpg|\\.bmp|\\.eps|\\.gif|\\.mif|\\.miff|\\.png|\\.tif|\\.tiff|\\.svg|\\.wmf|\\.jpe|\\.jpeg|\\.dib|\\.ico|\\.tga|\\.cut|\\.pic)\\b)[^>]*>", re.I) 
    #     image_list = re.findall(pattern,self.content)
    #     return image_list

class MessageImageItem(models.Model):
    postmessage=models.ForeignKey(PostMessage,verbose_name=u'对应消息')
    content_image = models.ImageField(u'图片', upload_to='csinla_posts/messageimageitem/content_image/')


class PostMaterial(models.Model):
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    level = models.IntegerField(u'显示优先级', default=0)
    MATERIAL_STATUS_LIST = (
        ('ACTIVE', u'使用中'),
        ('OVERDUE', u'已过期'),
        ('WAITING', u'待定'),
    )
    material_status = models.CharField(
        u'素材状态', max_length=24, choices=MATERIAL_STATUS_LIST, default='ACTIVE')
    MATERIAL_TYPE_LIST = (
        ('EXPOSURE_TOP1', u'朋友圈上方（90*90——临时猜测，根据实际定）'),
        ('EXPOSURE_TOP2', u'朋友圈上方（500*90——临时猜测，根据实际定）'),
    )
    material_type = models.CharField(
        u'素材类型', max_length=24, choices=MATERIAL_TYPE_LIST, default='EXPOSURE_TOP1')
    content_text = models.CharField(u'文案', max_length=512, blank=True, null=True)
    content_image = models.ImageField(
        u'图片', upload_to='csinla_posts/PostMaterial/content_image/', blank=True, null=True)
    content_link = models.URLField(u'链接', blank=True, null=True)
    description = models.TextField(u'备注', blank=True, null=True)

    class Meta:
        ordering = ["level","-create_time"]
        verbose_name = u'素材'
        verbose_name_plural = verbose_name

    @property
    def material_status_verbose(self):
        d = dict(self.MATERIAL_STATUS_LIST)
        return d.get(self.material_status, None)

    def __unicode__(self):
        res = str(self.id)
        if not isinstance(res, unicode):
            res = res.decode('utf-8')
        return res

class ViewRecord(models.Model):
    create_date=models.DateField(u'记录日期')
    belong_to= models.CharField(u'帖子类型',max_length=20)
    view_count=models.IntegerField(u'浏览量',default=0)
    user_count=models.IntegerField(u'浏览用户数',default=0)
    collect_count=models.IntegerField(u'收藏用户数',default=0)
    last_change_time=models.DateTimeField(u'最后修改时间',auto_now=True)
    join_list=models.ManyToManyField(Profile,verbose_name=u'访问用户',blank=True)

    class Meta:
        verbose_name = u"模块浏览记录"
        verbose_name_plural = verbose_name
        ordering=['-create_date']

    @property
    def view_detail(self):
        viewrecord_list=ViewRecord.objects.filter(create_date__gte=self.create_date,belong_to=self.belong_to)
        totle_view_count=0
        totle_join_list=Profile.objects.none()
        totle_collect_count=0
        for viewrecord in viewrecord_list:
            totle_view_count+=viewrecord.view_count
            totle_collect_count+=viewrecord.collect_count
            totle_join_list=totle_join_list|viewrecord.join_list.all()
        totle_join_list=totle_join_list.distinct()
        return u'共%s人%s人次浏览，%s次收藏' % (totle_join_list.count(),totle_view_count,totle_collect_count)

    def save(self, *args, **kwargs):
        if self.id:
            self.user_count=self.join_list.all().count()
        super(ViewRecord, self).save(*args, **kwargs)

class Car(Post):
    car_id = models.CharField(
        max_length=20,
        default='C1127'
    )
    car_type = models.CharField(
        max_length=10, 
        default='Japanese'
    )
    car_type_other = models.CharField(
        max_length=10, 
        null=True,
        blank=True
    )
    brand = models.TextField(
        max_length=20
    )

    vehicle_age = models.CharField(u'车龄',max_length=20,default=0)
    vehicle_miles = models.CharField(u'行驶里程',max_length=20,default = 0)
    fee = models.CharField(u'价格',max_length=10,default=0)
    fee2 = models.IntegerField(u'价格2',default=0)

    price=models.DecimalField(u'价格（分数）', max_digits=12, decimal_places=2,default=Decimal(0.0))
    price2=models.DecimalField(u'价格（分数2）', max_digits=12, decimal_places=2,default=Decimal(0.0))


    level_type = models.CharField(
        max_length=10, 
        default='other'
    )
    level_type_other = models.CharField(
        max_length=10, 
        null=True,
        blank=True
    )
    TRANSMISSION_TYPE_CHOICE = (
        (u'自动',u'自动'),
        (u'手动',u'手动')
    )
    transmission_type = models.CharField(
        max_length=10, 
        choices=TRANSMISSION_TYPE_CHOICE, 
        default='auto'
    )
    displacement = models.CharField(
        max_length=30,
        default=0
    )
    DRIVE_TYPE_CHOICE = (
        (u'前驱',u'前驱'),
        (u'后驱',u'后驱'),
        (u'四驱',u'四驱')
    )
    drive_type = models.CharField(
        max_length=20, 
        choices=DRIVE_TYPE_CHOICE, 
        null=True, 
    )
    inside_color = models.TextField(
        max_length=50, 
        null=True, 
    )
    outside_color = models.TextField(
        max_length=50, 
        null=True, 
    )
    OIL_TYPE_CHOICE = (
        (u'汽油',u'汽油'),
        (u'柴油',u'柴油'),
        (u'油电混合',u'油电混合'),
        (u'电力',u'电力')
    )
    oil_type = models.CharField(
        max_length=10, 
        choices=OIL_TYPE_CHOICE, 
        null=True, 
    )
    TURBO_TYPE_CHOICE = (
        ('yes','yes'),
        ('no','no')
    )
    turbo = models.CharField(
        max_length=10, 
        choices=TURBO_TYPE_CHOICE, 
        null=True, 
    )
    vin_number = models.CharField(
        max_length = 20
    )
    contactor = models.TextField(
        max_length = 100,
        default = 'admin'
    )
    contact_way = models.TextField(
        max_length = 100,
        default = ''
    )


    class Meta:
        verbose_name = u"汽车"
        verbose_name_plural = verbose_name
        ordering=['-post_date']
    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        self.car_id = "C" + str(10000 + self.id)
        super(Car, self).save(*args, **kwargs)
        return

    def delete(self, *args, **kwargs):
        print 1
        
        super(Car, self).delete(*args, **kwargs)
        return

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title':self.title,
            'belong_to': self.belong_to,
            'post_date':self.post_date,
            'expire_date':self.expire_date,
            'rentpicture_count':self.rentpicture_set.all().count(),
            'reply_num':self.reply_num,
            'content':self.content,
            'phone':self.phone,
            'weixin':self.weixin,
            'author_id':self.author_id,
            'active':self.active,
            'is_top':self.is_top,
            'is_notice':self.is_notice,
            'last_change_time':self.last_change_time,
            'is_sys':self.is_sys,
            'post_ptr_id':self.post_ptr_id,
            'car_id':self.car_id,
            'car_type':self.car_type,
            'car_type_other':self.car_type_other,
            'brand':self.brand,
            'vehicle_age':self.vehicle_age,
            'vehicle_miles':self.vehicle_miles,
            'fee':self.fee,
            'level_type':self.level_type,
            'level_type_other':self.level_type_other,
            'transmission_type':self.transmission_type,
            'displacement':self.displacement,
            'drive_type':self.drive_type,
            'inside_color':self.inside_color,
            'outside_color':self.outside_color,
            'oil_type':self.oil_type,
            'turbo':self.turbo,
            'vin_number':self.vin_number,
        }



class CarInspection(models.Model):
    car = models.ForeignKey(Car, on_delete = models.CASCADE, related_name = 'car', null = True, blank = True)
    ENGINE_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    engine = models.CharField(u'发动机',max_length=15, choices=ENGINE_CHOICE, null=True, blank = True)
    engine_content = models.CharField(u'发动机详情',max_length=250,null=True,blank = True)
    TRANSMISSION_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    transmission = models.CharField(u'变速器',max_length=15, choices=TRANSMISSION_CHOICE, blank = True,null=True)
    transmission_content = models.CharField(u"变速器详情",max_length=250, blank = True,null=True)

    LIGHT_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    light = models.CharField(
        max_length=15, 
        choices=LIGHT_CHOICE, 
        null=True, 
        blank = True,
        verbose_name=u"前后灯"
    )
    light_content = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"前后灯详情"
    )

    COLOUR_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    colour = models.CharField(
        max_length=15, 
        choices=COLOUR_CHOICE,
        null=True, 
        verbose_name=u"原厂颜色"
    )
    colour_content = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"原厂颜色详情"
    )

    CIRCUIT_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    circuit = models.CharField(
        max_length=15, 
        choices=CIRCUIT_CHOICE, 
        null=True, 
        blank = True,
        verbose_name=u"电路"
    )
    circuit_content = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"电路详情"
    )

    TIRES_CHOICE = (
        (u'正常',u'正常'),
        (u'非正常',u'非正常'),
    )
    tires = models.CharField(
        max_length=15, 
        choices=TIRES_CHOICE, 
        null=True, 
        blank = True,
        verbose_name=u"轮胎"
    )

    tires_wear = models.IntegerField(
        null=True, 
        blank = True,
        verbose_name=u"轮胎磨损度"
    )

    tires_content = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"轮胎详情"
    )
    MODIFIED_CHOICE = (
        (u'有',u'有'),
        (u'无',u'无'),
    )
    description= models.CharField(
        max_length=250, 
        choices=MODIFIED_CHOICE, 
        null=True, 
        blank = True,
        verbose_name=u"有无改装"
    )

    address = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"汽车所在地"
    )
    to = models.CharField(
        max_length=250, 
        null=True, 
        blank = True,
        verbose_name=u"无事故车"
    )
    mileage_min = models.IntegerField(
        null=True, 
        blank = True,
        verbose_name=u"里程min"
    )
    mileage_max = models.IntegerField(
        null=True, 
        blank = True,
        verbose_name=u"里程max"
    )
    image = models.ImageField(
        blank = True,
        upload_to = 'carinspection/',
    )

    class Meta:
        verbose_name = u"汽车检验表单"
        verbose_name_plural = verbose_name

 
class Rent(Post):
    house_id = models.CharField(
        max_length=20, 
        default="H1"
    )
    rent_begins = models.DateField(
        default=timezone.now
    )
    rent_ends = models.DateField(
        default=timezone.now
    )
    district = models.CharField(
        max_length=20,
        null=True,
    )
    district_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    fee = models.IntegerField(
        default=0,
    )

    SHARE_TYPE_CHOICE = (
        ('private','private'),
        ('share','share'),
    )
    share = models.CharField(
        max_length=10,
        choices=SHARE_TYPE_CHOICE,
        null=True,      
    )
    house_type = models.CharField(
        max_length=10,
        default='other'
    )
    house_type_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    room_type = models.CharField(
        max_length=10,
        default='other'
    )
    room_type_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    PET_CHOICE = (
        (u'允许',u'允许'),
        (u'不允许',u'不允许')
    )
    pet = models.CharField(
        max_length = 10,
        choices = PET_CHOICE,
        null = True,      
    )
    SMOKE_TYPE_CHOICE = (
        (u'允许',u'允许'),
        (u'不允许',u'不允许')
    )
    smoke = models.CharField(
        max_length = 10,
        choices = SMOKE_TYPE_CHOICE,
        null = True,     
    )
    PARKING_TYPE_CHOICE = (
        (u'有','有'),
        (u'无','无'),
        ('street parking','street parking')
    )
    parking = models.CharField(
        max_length = 20,
        choices = PARKING_TYPE_CHOICE,
        null = True,    
    )
    GENDER_REQUIRE_CHOICE = (
        (u'限男生',u'限男生'),
        (u'限女生',u'限女生'),
        (u'不限制',u'不限制')
    )
    gender_require = models.CharField(
        max_length = 20,
        choices = GENDER_REQUIRE_CHOICE,
        default = 'no_requirement'
    )
    driving_time_toschool_hour = models.CharField(
        max_length = 20,
        default = u"0"
    )
    driving_time_toschool_minute = models.CharField(
        max_length = 20,
        default = u"0"
    )
    transit_time_toschool_hour = models.CharField(
        max_length = 20,
        default = u"0"
    )
    transit_time_toschool_minute = models.CharField(
        max_length = 20,
        default = u"0"
    )
    address = models.TextField(
        max_length = 100
    )
    contactor = models.TextField(
        max_length = 30,
        default = 'admin'
    )
    contact_way = models.TextField(
        max_length = 50,
        default = '87654321'
    )

    
    class Meta:
        verbose_name = u"个人转租"
        verbose_name_plural = verbose_name
        ordering=['-post_date']\

    @property
    def is_other(self):
        if self.district in ['USC','SMC UCLA','UCSB','UCSD','UCI','ELAC','PCC']:
            return False
        else:
            return True

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'district':self.district,
            'district_other': self.district_other,
            'is_top':self.is_top,
            'title':self.title,
            'rentpicture_count':self.rentpicture_set.all().count(),
            'fee':self.fee,
            'house_type':self.house_type,
            'house_type_other':self.house_type_other,
            'room_type':self.room_type,
            'room_type_other':self.room_type_other,
            'parking':self.parking,
            'get_date':self.get_date(),
        }

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Rent, self).save(*args, **kwargs)
        self.house_id = "H" + str(10000 + self.id)
        super(Rent, self).save(*args, **kwargs)
        return

    def images(self):
        # 获取图片URL
        images_url = []
        pics = self.rentpicture_set.all()
        for pic in pics:
            images_url.append(pic.image.url)
        return  images_url


class EntireRent(Post):
    house_id = models.CharField(
        max_length=20,
        default="H1"
    )
    rent_begins = models.DateField(
        default=timezone.now
    )
    rent_ends = models.DateField(
        default=timezone.now
    )
    district = models.CharField(
        max_length=20,
        null=True,
    )
    district_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    fee = models.IntegerField(
        default=0,
    )

    SHARE_TYPE_CHOICE = (
        ('private', 'private'),
        ('share', 'share'),
    )
    share = models.CharField(
        max_length=10,
        choices=SHARE_TYPE_CHOICE,
        null=True,
    )
    house_type = models.CharField(
        max_length=10,
        default='other'
    )
    house_type_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    room_type_other = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    PET_CHOICE = (
        (u'允许', u'允许'),
        (u'不允许', u'不允许')
    )
    pet = models.CharField(
        max_length=10,
        choices=PET_CHOICE,
        null=True,
    )
    SMOKE_TYPE_CHOICE = (
        (u'允许', u'允许'),
        (u'不允许', u'不允许')
    )
    smoke = models.CharField(
        max_length=10,
        choices=SMOKE_TYPE_CHOICE,
        null=True,
    )
    PARKING_TYPE_CHOICE = (
        (u'有', '有'),
        (u'无', '无'),
        ('street parking', 'street parking')
    )
    parking = models.CharField(
        max_length=20,
        choices=PARKING_TYPE_CHOICE,
        null=True,
    )
    pak_nums = models.CharField(
        max_length=10,
        null=True,
        verbose_name=u'停车位个数'
    )
    driving_time_toschool_hour = models.CharField(
        max_length=20,
        default=u"0"
    )
    driving_time_toschool_minute = models.CharField(
        max_length=20,
        default=u"0"
    )
    transit_time_toschool_hour = models.CharField(
        max_length=20,
        default=u"0"
    )
    transit_time_toschool_minute = models.CharField(
        max_length=20,
        default=u"0"
    )
    address = models.TextField(
        max_length=100
    )
    contactor = models.TextField(
        max_length=30,
        default='admin'
    )
    contact_way = models.TextField(
        max_length=50,
        default='87654321'
    )

    class Meta:
        verbose_name = u"整套出租"
        verbose_name_plural = verbose_name
        ordering = ['-post_date']

    @property
    def is_other(self):
        if self.district in ['USC', 'SMC UCLA', 'UCSB', 'UCSD', 'UCI', 'ELAC', 'PCC']:
            return False
        else:
            return True

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'district': self.district,
            'district_other': self.district_other,
            'is_top': self.is_top,
            'title': self.title,
            'rentpicture_count': self.rentpicture_set.all().count(),
            'fee': self.fee,
            'house_type': self.house_type,
            'house_type_other': self.house_type_other,
            'room_type': self.room_type,
            'room_type_other': self.room_type_other,
            'parking': self.parking,
            'get_date': self.get_date(),
        }

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(EntireRent, self).save(*args, **kwargs)
        self.house_id = "H" + str(10000 + self.id)
        super(EntireRent, self).save(*args, **kwargs)
        return


class Rentpicture(models.Model):
    # 帖子图片
    post = models.ForeignKey(Post)
    image = models.ImageField(blank = True,upload_to = 'house/',)
    image_height = models.IntegerField(blank = True,null = True)
    image_width = models.IntegerField(blank = True,null = True)
    thumbnail = models.ImageField(blank = True,upload_to = 'house/thumbs/')
    thumbnail_height = models.IntegerField(blank = True,null = True)
    thumbnail_width = models.IntegerField(blank = True,null = True)    

    def __unicode__(self):
        return self.post.title

    def save(self,force_update=False,force_insert=False,thumb_size=(180,300)):

        if not self.id:
            image = Image.open(self.image)

            if image.mode not in ('L','RGB'):
                image = image.convert('RGB')
            # save the original size
            self.image_width, self.image_height = image.size

            image.thumbnail(thumb_size,Image.ANTIALIAS)

            # save the thumbnail to memory
            temp_handle = StringIO()
            image.save(temp_handle,'png')
            temp_handle.seek(0)

            # save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                    temp_handle.read(),
                                    content_type='image/png')
            self.thumbnail.save(suf.name,suf,save=False)
            self.thumbnail_width, self.thumbnail_height = image.size

        # save the image object
        super(Rentpicture, self).save(force_update, force_insert)

    class Meta:
        verbose_name = u"帖子图片"
        verbose_name_plural = verbose_name


    def to_dict(self):
        return {
            'id': self.id,
            'image':self.image,
            'image_height': self.image_height,
            'image_width':self.image_width,
            'thumbnail':self.thumbnail,
            'thumbnail_height':self.thumbnail_height,
            'thumbnail_width':self.thumbnail_width,
            'post_id':self.post_id,
        }



class Rent2(Post):
    house_id = models.CharField(
        max_length=20,
        default='H1127',
    )
    rent_begins = models.DateField(
        default=timezone.now,
    )
    rent_ends = models.DateField(
        default=timezone.now
    )
    district = models.CharField(
        max_length=10, 
        null = True, 
        blank = True
    )
    district_other = models.CharField(
        max_length=10, 
        null = True, 
        blank = True
    )
    fee = models.IntegerField(
        default = 0,
    )
    occupy_limit = models.IntegerField(
        default=1
    )
    house_type = models.CharField(
        max_length=10, 
        default='other'
    )
    house_type_other = models.CharField(
        max_length=10, 
        null=True,
        blank=True
    )
    room_type = models.CharField(
        max_length=10, 
        default='other'
    )
    room_type_other = models.CharField(
        max_length=10, 
        null=True,
        blank=True
    )
    PET_CHOICE = (
        (u'允许',u'允许'),
        (u'不允许',u'不允许')
    )
    pet = models.CharField(
        max_length=10, 
        choices=PET_CHOICE,
        null=True,
        blank=True
    )
    SMOKE_TYPE_CHOICE = (
        (u'允许',u'允许'),
        (u'不允许',u'不允许')
    )
    smoke = models.CharField(
        max_length=10, 
        choices=SMOKE_TYPE_CHOICE, 
        null=True, 
        blank=True
    )
    PARKING_TYPE_CHOICE = (
        (u'有',u'有'),
        (u'无',u'无'),
        ('street parking','street parking')
    )
    parking = models.CharField(
        max_length=20, 
        choices=PARKING_TYPE_CHOICE, 
        null=True, 
        blank=True
    )
    GENDER_REQUIRE_CHOICE = (
        ('male_only','male_only'),
        ('female_only','female_only'),
        ('no_requirement','no_requirement')
    )
    gender_require = models.CharField(
        max_length=20, 
        choices=GENDER_REQUIRE_CHOICE, 
        default='no_requirement'
    )
    driving_time_toschool = models.IntegerField(
        default=0
    )
    transit_time_toschool = models.IntegerField(
        default=0
    )
    address = models.TextField(
        max_length=100, 
    )
    contactor = models.TextField(
        max_length=30, 
        default='admin'
    )
    contact_way = models.TextField(
        max_length=50, 
        default='87654321'
    )
     
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"合租"
        verbose_name_plural = verbose_name


# class Used(models.Model):
# 	Name=models.CharField(max_length=100,blank=True)
# 	Content=UEditorField(u'内容	',width=600, height=300, toolbars="mini", imagePath="product_img/%(basename)s_%(datetime)s.%(extname)s", filePath="product_file/%(basename)s_%(datetime)s.%(extname)s", upload_settings={"imageMaxSize":1204000},
#              settings={},command=None,blank=True)

class UsedGoodsTag(models.Model):
    tag=models.CharField(u'标签内容',max_length=128,default='')

    class Meta:
        verbose_name = u"二手标签"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tag

class UsedTag(models.Model):
    tag=models.CharField(verbose_name=u'标签内容',max_length=128,default=u'二手')

    class Meta:
        verbose_name = u"标签"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tag
class UsedGoods(Post):
    tags=models.ManyToManyField(UsedGoodsTag,verbose_name=u'标签',blank=True,null=True)
    used_id=models.CharField(u'商品号',max_length=32,default='')
    district = models.CharField(u'地区',max_length=10,blank=True,null=True)
    address = models.CharField(u"具体地址",max_length=250,null=True,blank = True)
    connect_name = models.CharField(u'联系人',max_length = 100,default = '')
    connect_phone = models.CharField(u'联系电话',max_length = 100,default = '')
    connect_wx = models.CharField(u'联系微信',max_length = 100,default = '')
    content_detail=UEditorField(u'详细内容',width=600, height=300, toolbars="mini", imagePath="product_img/%(basename)s_%(datetime)s.%(extname)s", filePath="product_file/%(basename)s_%(datetime)s.%(extname)s", upload_settings={"imageMaxSize":1204000},
             settings={},command=None,blank=True)

    class Meta:
        verbose_name = u"二手商品"
        verbose_name_plural = verbose_name
        ordering=['-post_date']

    @property
    def totle_price(self):
        totle_price=0
        for item in self.usedgoodsitem_set.all():
            totle_price+=item.price
        return totle_price
    def save(self, *args, **kwargs):
        super(UsedGoods, self).save(*args, **kwargs)
        if not self.used_id:
            self.used_id = "U" + str(10000 + self.id)
            self.save()

class Used(Post):
    tags=models.ManyToManyField(UsedTag,verbose_name=u'标签',blank=True,null=True,default=u'二手')
    used_id=models.CharField(u'二手编号',max_length=32,default='')
    district = models.CharField(u'地区',max_length=10,blank=True,null=True,default='')
    address = models.CharField(u"具体地址",max_length=250,null=True,blank = True,default='')
    connect_name = models.CharField(u'联系人',max_length = 100,default = '')
    connect_phone = models.CharField(u'联系电话',max_length = 100,default = '')
    connect_wx = models.CharField(u'联系微信',max_length = 100,default = '')
    content_detail=UEditorField(u'详细内容',width=600, height=300, toolbars="mini", imagePath="product_img/%(basename)s_%(datetime)s.%(extname)s", filePath="product_file/%(basename)s_%(datetime)s.%(extname)s", upload_settings={"imageMaxSize":1204000},
             settings={},command=None,blank=True,default='')

    class Meta:
        verbose_name = u"二手"
        verbose_name_plural = verbose_name
        ordering=['-post_date']

    @property
    def totle_price(self):
        totle_price=0
        for item in self.usedgoodsitem_set.all():
            totle_price+=item.price
        return totle_price
    def save(self, *args, **kwargs):
        super(Used, self).save(*args, **kwargs)
        if not self.used_id:
            self.used_id = "S" + str(10000 + self.id)
            self.save()

class UsedGoodsItem(models.Model):
    usedgoods=models.ForeignKey(UsedGoods,on_delete=models.CASCADE)
    name=models.CharField(u'商品名',max_length=64,default='')
    price=models.IntegerField(u'售价',default=0)

class UsedBook(Post):
    book_id=models.CharField(u'书号',max_length=32,default='')
    district = models.CharField(u'地区',max_length=10,blank=True,null=True)
    address = models.CharField(u"具体地址",max_length=250,null=True,blank = True)
    connect_name = models.CharField(u'联系人',max_length = 100,default = '')
    connect_phone = models.CharField(u'联系电话',max_length = 100,default = '')
    connect_wx = models.CharField(u'联系微信',max_length = 100,default = '')
    content_detail=UEditorField(u'详细内容',width=600, height=300, toolbars="mini", imagePath="product_img/%(basename)s_%(datetime)s.%(extname)s", filePath="product_file/%(basename)s_%(datetime)s.%(extname)s", upload_settings={"imageMaxSize":1204000},
             settings={},command=None,blank=True)

    class Meta:
        verbose_name = u"二手书"
        verbose_name_plural = verbose_name
        ordering=['-post_date']

    def save(self, *args, **kwargs):
        super(UsedBook, self).save(*args, **kwargs)
        if not self.book_id:
            self.book_id = "B" + str(10000 + self.id)
            self.save()





class UsedBookItem(models.Model):
    usedbook=models.ForeignKey(UsedBook,on_delete=models.CASCADE)
    name=models.CharField(u'书名',max_length=64,default='')
    price=models.IntegerField(u'售价',default=0)
    isbn=models.CharField(u'ISBN',max_length=32,default='')


class Exposure(Post):
    temp=models.CharField(u'无效字段',max_length=32,default='')
    def toJSON(self):
        # 对象转json格式
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    def to_dict(self):
        return {
            'id': self.id,
            'title':self.title,
            'belong_to': self.belong_to,
            'post_date':self.post_date,
            'expire_date':self.expire_date,
            'rentpicture_count':self.rentpicture_set.all().count(),
            'reply_num':self.reply_num,
            'content':self.content,
            'phone':self.phone,
            'weixin':self.weixin,
            'author_id':self.author_id,
            'active':self.active,
            'is_top':self.is_top,
            'is_notice':self.is_notice,
            'last_change_time':self.last_change_time,
            'is_sys':self.is_sys,
            'post_ptr_id':self.post_ptr_id,
            'temp':self.temp,

        }




def active_date(sender, comment, request, *args, **kwargs):
    post_id = comment.object_pk
    post = Post.objects.get(id=post_id)
    post.active = timezone.now()
    post.save()

comment_was_posted.connect(active_date)
