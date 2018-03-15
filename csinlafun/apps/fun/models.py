#_*_ encoding: utf-8 _*_
from django.db import models
import os
# import Image
# from csinlafun.settings import MEDIA_ROOT
# from django.db.models.fields.files import ImageFieldFile

import threading
import datetime
import random
from DjangoUeditor.models import UEditorField


class Hoster(models.Model):
    name=models.CharField(u'姓名',max_length=64)
    GENDERS = (
        ('MALE', u'先生'),
        ('FEMALE', u'女士'),
        ('ORGANIZATION', u'保密'),
    )
    gender = models.CharField(verbose_name=u'性别', max_length=20, choices=GENDERS)
    phone = models.CharField(u'联系电话',max_length=32)
    photo = models.ImageField(u'照片', upload_to='fun/hoster/photo/')
    email = models.EmailField(u'电子邮箱')
    desc=models.TextField(u'个人介绍',default='')
        
    class Meta:
        verbose_name = u"导游"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name




class Activity(models.Model):
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    hoster=models.ForeignKey(Hoster,verbose_name=u'导游')
    name=models.CharField(u'活动名',max_length=256)
    desc=models.TextField(u'活动描述',max_length=512,default='')
    pre_price=models.DecimalField(u'单价(美元)', max_digits=12, decimal_places=2, default=0.0)
    # max_count = models.IntegerField(u'最大参与人数',default=0)
    cover_image = models.ImageField(u'封面图', upload_to='fun/activity/cover_image/',blank=True,null=True)
    ticket_image = models.ImageField(u'门票图', upload_to='fun/activity/ticket_image/',blank=True,null=True)
    level=models.IntegerField(u'显示优先级',default=100)
    is_valid=models.BooleanField(u'是否有效',default=True)

    def go_editor(self):
        from django.utils.safestring import mark_safe
        return mark_safe('''<a href='http://www.csinla.com:5051/fun/activity/edit/%s'>编辑图片</a>''' % (self.id))
    go_editor.short_description = "编辑图片"
    class Meta:
        verbose_name = u"活动"
        verbose_name_plural = verbose_name

    @property
    def current_time_item(self):
        return self.activitytimeitem_set.filter(activity_time__gte=datetime.datetime.now())

    def __unicode__(self):
        return self.name



class Paragraph(models.Model):
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    activity=models.ForeignKey(Activity,verbose_name=u'对应活动')
    content_text=UEditorField(verbose_name=u'文案信息', width=600, height=300, imagePath="fun/paragraph/content_img/",
                                  null=True,blank=True,filePath="fun/paragraph/content_img/",default='')
    content_img=models.ImageField(u'图片信息',upload_to='fun/paragraph/content_img/',blank=True,null=True)

    class Meta:
        verbose_name = u"活动详情段落"
        verbose_name_plural = verbose_name
        ordering = ["create_time"]

    @property
    def current_time_item(self):
        return self.activitytimeitem_set.filter(activity_time__gte=datetime.datetime.now())

    def __unicode__(self):
        return str(self.id)

class ActivityTimeItem(models.Model):
    activity=models.ForeignKey(Activity,verbose_name=u'对应活动')
    activity_time=models.DateTimeField(u'活动时间')
    max_count=models.IntegerField(u'最大参与人数')

    class Meta:
        verbose_name = u"活动时间点"
        verbose_name_plural = verbose_name

    @property
    def join_count(self):
        join_count=0
        for order in self.activityorder_set.filter(order_status__in=['SENT','USED']):
            join_count+=order.join_count
        return join_count
    def __unicode__(self):
        return u'%s【%s】' % (self.activity,self.activity_time)

        
class ActivityOrder(models.Model):
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    customer_name=models.CharField(u'客户姓名',max_length=64,default='')
    customer_email=models.EmailField(u'客户邮箱')
    ORDER_STATUS_LIST = (
        ('NEED_PAY', u'待付款'),
        # ('CONFIRMED',u'待发放'),
        ('SENT', u'已发放'),
        ('USED', u'已使用'),
        ('FAILED', u'交易失效'),
    )
    order_status = models.CharField(
        u'订单状态', max_length=24, choices=ORDER_STATUS_LIST, default='NEED_PAY')
    activitytimeitem=models.ForeignKey(ActivityTimeItem,verbose_name=u'对应活动时间')
    join_count=models.IntegerField(u'参与客人数',default=0)
    remark = models.TextField(u'备注', blank=True, null=True)
    order_no = models.CharField(u'订单编号', max_length=8,default='')

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        is_paid_success=False
        if self.id:
            order=ActivityOrder.objects.get(id=self.id)
            if self.order_status=='SENT' and order.order_status=='NEED_PAY':
                is_paid_success=True
        else:
            if self.order_status=='SENT':
                is_paid_success=True
        super(ActivityOrder, self).save(*args, **kwargs)
        if not self.order_no:
            num_str = str(self.id)
            chars = '0123456789'
            self.order_no = '%s%s%s' % (len(num_str), ''.join(random.choice(chars) for x in range(7 - len(num_str))), num_str)
            self.save()
        if is_paid_success:
            from fun.functions import send_paid_email
            print '1111'
            result=send_paid_email(self)
            print result
            # t = threading.Thread(target=send_paid_email, args=(self))
            # t.start()


class ContactInfo(models.Model):
    email = models.EmailField(u"邮箱",max_length=50)
    message=models.TextField(u'留言内容',default='')   

    class Meta:
        verbose_name = u"用户留言"   
        verbose_name_plural = verbose_name

