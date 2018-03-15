# encoding: utf-8

from __future__ import unicode_literals
from datetime import datetime
import django.utils.timezone as timezone
from DjangoUeditor.models import UEditorField

from django.db import models
from django.contrib.auth.models import AbstractUser
# from csinla_posts.models import Post
# from django.utils import timezone
from django.db.models.signals import post_save
# from django_comments.models import UserNotificationsCount
from django.db.models import signals
from django.utils import timezone
import threading
from PIL import Image
from decimal import Decimal
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
class Profile(AbstractUser):
    reg_type = models.CharField(u'注册类型',max_length=10, choices=(("STU", u"学生"), ("COM", u"商家")), default='STU')
    real_name = models.CharField(u"真实姓名",max_length=50, null=True, blank=True)
    gender = models.CharField(u'性别',max_length=6, choices=(("male", u"男"), ("female", u"女"), ("null", "保密")), default="null")
    birth_date = models.DateField(u"生日", null=True, blank=True)
    school = models.CharField(u'学校',max_length=200, default=u'')
    student_id = models.CharField(u'学生ID',max_length=20, default='0')
    avatar = models.ImageField(u'头像',upload_to='avatars/%Y/%m', default='avatars/moon.jpg', max_length=100)
    personal_level = models.IntegerField(default=0)
    academic_rank = models.IntegerField(default=0)
    self_intro = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"自我介绍")
    reply_total = models.IntegerField(default=0, verbose_name=u"回帖数")
    reg_time = models.DateTimeField(u"注册日期",default=timezone.now)
    phone = models.CharField(max_length=15,default="", null=True, blank=True, verbose_name=u"手机")
    weixin = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name=u"微信")
    is_phone = models.BooleanField(default=False)
    is_weixin = models.BooleanField(default=False)
    is_name = models.BooleanField(default=False)
    join_ip=models.CharField(u'注册时ip',max_length=32,default='')
    last_login_ip = models.GenericIPAddressField(u'登录IP',blank=True,null=True)
    is_carfax_manager = models.BooleanField(u'carfax管理权限',default=False)
    SOURCE_LIST=(
        ('NORMAL',u'普通用户'),
        ('WECHAT',u'微信用户'),
    )
    source = models.CharField(u'来源',max_length=16,choices=SOURCE_LIST,default='NORMAL')


    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name
    # favourite_posts = models.ManyToManyField(
    #     Post,
    #     related_name = 'favourite_posts'
    # )

    # follows = models.ManyToManyField(
    #     User,
    #     related_name='follows',
    #     symmetrical = False,
    # )


    # reg_time = models.DateTimeField(
    #     #auto_now_add = True,
    #     default = timezone.now,
    # )

    duoshuo_id = models.IntegerField(
            default = 0
    )
    def get_age(self):
        delta = timezone.now() - self.reg_time
 
        if delta.days >= 365:
            return '%d年' % (delta.days / 365)
        elif delta.days >= 30:
            return '%d个月' % (delta.days / 30)
        elif delta.days > 0:
            return '%d天' % delta.days
        elif delta.seconds < 60:
            return "%d秒" % delta.seconds
        elif delta.seconds < 60 * 60:
            return "%d分钟" % (delta.seconds / 60)
        else:
            return "%d小时" % (delta.seconds / 60 / 60) 

    def unread_message(self):
        from csinla_posts.models import PostMessage
        unread_list=PostMessage.objects.filter(message_type='REPLY',reply_message__in=self.postmessage_set.all(),has_read=False)|PostMessage.objects.filter(post__in=self.posts.all(),reply_message__isnull=True,has_read=False)
        num = unread_list.count()
        return num

    @property
    def avatar_url(self):
        if str(self.avatar)=='avatars/moon.jpg':
            try:
                wechat=WechatInfo.objects.get(userinfo=self)
                return wechat.headimgurl
            except WechatInfo.DoesNotExist:
                return self.avatar.url
        else:
            return self.avatar.url

    def __unicode__(self):
        if self.real_name:
            return self.real_name
        return self.username

    def save(self, *args, **kwargs):
        if self.id:
            from csinla_posts.models import Post
            if self.first_name==u'系统用户':
                Post.objects.filter(author=self,is_sys=False).update(is_sys=True)
            else:
                Post.objects.filter(author=self,is_sys=True).update(is_sys=False)
        super(Profile, self).save(*args, **kwargs)
    def images(self):
        return self.avatar.url

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(u"验证码类型",choices=(('register', u'注册'), ('forget', u'忘记密码'),('off_posts', u'帖子审核')), max_length=10)
    send_time = models.DateTimeField(u"发送时间",auto_now_add=True)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

# signal
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)

class CustomizedCar(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'Customized_author', null = True, blank = True)
    car_type = models.CharField(u'车类型',max_length=10, default='other', null=True, blank=True)
    car_type_other = models.CharField(max_length=10, null=True, blank=True)
    brand = models.TextField(max_length=20, null=True, blank=True)
    vehicle_age = models.CharField(max_length=10, default=0, null=True, blank=True)
    vehicle_miles = models.CharField(max_length=10, default=0, null=True, blank=True)

    level_type = models.CharField(max_length=10, default='other', null=True, blank=True)
    level_type_other = models.CharField(max_length=10,  null=True, blank=True)

    TRANSMISSION_TYPE_CHOICE = (
        (u'自动',u'自动'),
        (u'手动',u'手动')
    )
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_TYPE_CHOICE, default='auto', null=True, blank=True)

    DRIVE_TYPE_CHOICE = (
        (u'前驱',u'前驱'),
        (u'后驱',u'后驱'),
        (u'四驱',u'四驱')
    )
    drive_type = models.CharField(max_length=15, choices=DRIVE_TYPE_CHOICE, null=True, blank=True)
    color = models.TextField(max_length=50, null=True, blank=True)

    OIL_TYPE_CHOICE = (
        (u'汽油',u'汽油'),
        (u'柴油',u'柴油'),
        (u'油电混合',u'油电混合'),
        (u'电力',u'电力')
    )
    oil_type = models.CharField(max_length=10, choices=OIL_TYPE_CHOICE, null=True, blank=True)

    TURBO_TYPE_CHOICE = (
        ('yes','yes'),
        ('no','no')
    )
    turbo = models.CharField(max_length=10, choices=TURBO_TYPE_CHOICE, null=True, blank=True)
    contactor = models.TextField(max_length=100, default='admin')
    phone = models.CharField(
        max_length=11, 
        default='0', 
        verbose_name=u"联系电话"
    )
    weixin = models.CharField(
        max_length=20, 
        default='0', 
        verbose_name=u"联系微信"
    )
    claim = models.TextField(max_length=400, null = True, blank = True)

    class Meta:
        verbose_name = u"汽车定制"
        verbose_name_plural = verbose_name


class FuncFeedback(models.Model):
    page = models.CharField(max_length=10)
    time = models.DateField(verbose_name=u"遇到问题时间", null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    feedback_img = models.ImageField(upload_to='feedback/%Y/%m', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = u"功能失灵"
        verbose_name_plural = verbose_name


class AccountFeedback(models.Model):
    type = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    content = models.CharField(max_length=200, null=True, blank=True)
    operating = models.CharField(max_length=200, null=True, blank=True)
    feedback_img = models.ImageField(upload_to='feedback/%Y/%m', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = u"账号问题"
        verbose_name_plural = verbose_name


class ExperFeedback(models.Model):
    feedback = models.CharField(max_length=200)

    class Meta:
        verbose_name = u"联系我们"
        verbose_name_plural = verbose_name


class OtherFeedback(models.Model):
    content = models.CharField(max_length=200)
    feedback_img = models.ImageField(upload_to='feedback/%Y/%m', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = u"其他问题"
        verbose_name_plural = verbose_name

class WxToken(models.Model):
    token = models.CharField(max_length=200)
    lifetime = models.DateTimeField(
        default=0
    )
    def get_date(self):
        delta = timezone.now() - self.lifetime
        if delta.seconds < 6000:
            return True
        else:
            return False

class JsToken(models.Model):
    token = models.CharField(max_length=200)
    lifetime = models.DateTimeField(
        default=0
    )
    def get_date(self):
        delta = timezone.now() - self.lifetime
        if delta.seconds < 6000:
            return True
        else:
            return False

class Unread(models.Model):
    user_id = models.IntegerField()
    notice_id = models.IntegerField()


class BuyCarNotice(models.Model):
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = u"买车通知邮件"
        verbose_name_plural = verbose_name


class ContactInfo(models.Model):
    email = models.EmailField(u"邮箱",max_length=50)
    message=models.TextField(u'留言内容',default='')   

    class Meta:
        verbose_name = u"用户留言"   
        verbose_name_plural = verbose_name


class Carfax(models.Model):
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    creator=models.ForeignKey(Profile,verbose_name=u'创建者')
    vin=models.CharField(u'VIN',max_length=17)
    name=models.CharField(u'名字',max_length=64)
    email = models.EmailField(u"邮箱",max_length=50)
    wechat=models.CharField(u'微信号',max_length=64)
    is_reply=models.BooleanField(u'是否已回复',default=False)
    unreply_time=models.DateTimeField(u'取消回复时间',blank=True,null=True)
    CARFAX_STATUS_LIST=(
        ('ACTIVE',u'活跃'),
        ('BACKUP',u'已归档'),
    )
    carfax_status=models.CharField(u'状态',max_length=16,choices=CARFAX_STATUS_LIST,default='ACTIVE')

    class Meta:
        verbose_name = u"carfax"   
        verbose_name_plural = verbose_name

    def un_reply_str(self):
        if not self.is_reply:
            unreply_time=self.create_time
            if self.unreply_time:
                unreply_time=self.unreply_time
            delta = timezone.now() - unreply_time
            if delta.days >= 365:
                return '%d年' % (delta.days / 365)
            elif delta.days >= 30:
                return '%d个月' % (delta.days / 30)
            elif delta.days > 0:
                return '%d天' % delta.days
            elif delta.seconds < 60:
                return "%d秒" % delta.seconds
            elif delta.seconds < 60 * 60:
                return "%d分钟" % (delta.seconds / 60)
            else:
                return "%d小时" % (delta.seconds / 60 / 60)
        return ''

    def save(self, *args, **kwargs):
        is_first=False
        if self.id:
            carfax=Carfax.objects.get(id=self.id)
            if self.is_reply!=carfax.is_reply and not self.is_reply:
                self.unreply_time=timezone.now()
        if not self.id:
            is_first=True
        super(Carfax, self).save(*args, **kwargs)
        if is_first:
            if not self.creator.weixin:
                user=self.creator
                user.weixin=self.wechat
                user.save()
    # @property
    # def is_reply(self):
    #     try:
    #         CarfaxReply.objects.get(carfax=self)
    #         return True
    #     except CarfaxReply.DoesNotExist:
    #         return False


class WechatInfo(models.Model):
    userinfo = models.OneToOneField(Profile, verbose_name=u'对应的账号', blank=True, null=True)
    open_id = models.CharField(u'微信的唯一识别码', max_length=199)
    unionid=models.CharField(u'微信开放平台唯一识别码',max_length=199,blank=True,null=True)
    scene_id = models.IntegerField(u'微信永久场景id', null=True, blank=True)
    nickname = models.CharField(u'昵称', max_length=199, null=False, blank=True)
    headimgurl = models.CharField(u'头像', max_length=1000, null=False, blank=True)
    GENDERS = (
        (1, u'男'),
        (2, u'女'),
        (3, u'未知'),
    )
    sex = models.IntegerField(u'性别', choices=GENDERS, default=3)
    province = models.CharField(u'省份', max_length=199, null=False, blank=True)
    city = models.CharField(u'城市', max_length=199, null=False, blank=True)
    country = models.CharField(u'国家', max_length=199, null=False, blank=True)
    
    class Meta:
        verbose_name = u"微信信息"
        verbose_name_plural = verbose_name

    @property
    def sex_verbose(self):
        d = dict(self.GENDERS)
        return d[self.sex] if self.sex in d else ''

    def save(self, *args, **kwargs):
        super(WechatInfo, self).save(*args, **kwargs)
        user=self.userinfo
        if not user.username.startswith(self.nickname):
            username=self.nickname
            i=1
            while Profile.objects.filter(username=username).exists():
                username='%s%s' % (self.nickname,i)
                i+=1
            user.username=username
            if user.gender=='null':
                if self.sex==1:
                    user.gender='male'
                elif self.sex=='2':
                    user.gender='female'
            user.save()



class WechatOpenToken(models.Model):
    account=models.OneToOneField(Profile,verbose_name=u'对应账号',blank=True,null=True)
    open_id = models.CharField(u'微信的唯一识别码', max_length=199)
    access_token=models.CharField(u'凭据字符',max_length=512)
    refresh_token=models.CharField(u'刷新凭据',max_length=512)
    expire_time=models.IntegerField(u'到期时间戳')
    class Meta:
        ordering = ["-expire_time"]


# class CarfaxReply(models.Model):
#     carfax=models.OneToOneField(Carfax,verbose_name=u'对应回复')
#     reply_text=models.CharField(u'回复文本',max_length=512)
#     reply_file=models.FileField(u'附件',upload_to='csinla_accounts/carfaxreply/reply_file/',blank=True,null=True)

#     class Meta:
#         verbose_name = u"carfax回复"   
#         verbose_name_plural = verbose_name

#     @property
#     def reply_file_url(self):
#         if self.reply_file:
#             return self.reply_file.url
#         else:
#             return ''

#     def save(self, *args, **kwargs):
#         is_first=False
#         if not self.id:
#             is_first=True
#         super(CarfaxReply, self).save(*args, **kwargs)
#         if is_first:
#             from utils.email_send import send_mail_carfax
#             t = threading.Thread(target=send_mail_carfax, args=(self.carfax.name,self.carfax.vin,self.reply_text,self.carfax.email))
#             t.start()

class ApplyForPickup(models.Model):

    # 接机申请资料
    name = models.CharField(verbose_name=u'接机姓名', default=u'',max_length=10)
    sex = models.CharField(verbose_name=u'性别',default=u'', max_length=6,null=True)
    wx = models.CharField(verbose_name=u'微信号', default=u'',max_length=20,null=True)
    phone = models.CharField(verbose_name=u'手机号', default=u'',max_length=20,null=True)
    major = models.CharField(verbose_name=u'就读专业',default=u'', max_length=20,null=True)
    email = models.EmailField(verbose_name=u'邮箱', max_length=20,null=True)
    baggage = models.CharField(verbose_name=u'行李数量', default=u'',max_length=10,null=True)
    flight = models.CharField(verbose_name=u'航班航班号', default=u'',max_length=20,null=True)
    departure = models.CharField(verbose_name=u'起飞时间',max_length=50,default=u'',null=True)
    departure_type = models.CharField(verbose_name=u'起飞时间时区',max_length=50,default=u'',null=True)
    landing_type = models.CharField(verbose_name=u'落地时间时区',max_length=50,default=u'',null=True)
    landing = models.CharField(verbose_name=u'落地时间',max_length=50,default=u'',null=True)
    address = models.CharField(verbose_name=u'地址',default=u'',max_length=100)
    contactor = models.CharField(verbose_name=u'联系人',default=u'', max_length=20,null=True)
    contacts_phone = models.CharField(verbose_name=u'联系人联系方式',default=u'', max_length=20,null=True)
    relation = models.CharField(verbose_name=u'关系', max_length=10,default=u'')
    img1 = models.ImageField(verbose_name=u'照片1', default=u'',upload_to='ad/')
    remark = models.CharField(verbose_name=u'备注', max_length=200,default=u'')
    zipcode = models.CharField(verbose_name=u'邮编',max_length=20,default=u'',null=True)
    img2 = models.ImageField(verbose_name=u'照片2', default=u'',upload_to='ad/',null=True,blank=True)
    belong = models.CharField(choices=(('USC',u'USC'),('UCLA', u'UCLA'), ('SMC', u'SMC'),('UCSB', u'UCSB')),
                              verbose_name=u'所属学校',max_length=50,default=u'')

    class Meta:
        verbose_name = u'接机申请资料'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name




class NewStudentComment(models.Model):
    user = models.ForeignKey(Profile, verbose_name=u'用户')
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    fav_nums = models.IntegerField(verbose_name=u'点赞数', default=0)
    belong = models.CharField(choices=(('hd', u'LA饮食娱乐咨询'), ('jj', u'入学与选课指南'), ('rx', u'新闻资讯'),
                                       ('jz', u'驾照与交通')), max_length=8, verbose_name=u'所属模块', default='jj')

    class Meta:
        verbose_name = u'新生评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self._meta.verbose_name


class DriveExamnation(models.Model):
    t_id = models.IntegerField(verbose_name=u'题号')
    content = models.CharField(verbose_name=u'内容',max_length=500)
    bingo = models.CharField(verbose_name=u'答案',max_length=200)
    answer_a = models.CharField(verbose_name=u'A',max_length=200,default=u'')
    answer_b = models.CharField(verbose_name=u'B',max_length=200,default=u'')
    answer_c = models.CharField(verbose_name=u'C',max_length=200,default=u'')
    img_content = models.URLField(verbose_name=u'选项图片',default=u'',null=True)
    img = models.URLField(verbose_name=u'题目的图片',default=u'',null=True)

    class Meta:
        verbose_name = u'驾照考试'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self._meta.verbose_name


class NewStudentSubmission(models.Model):
    """
    投稿
    """

    title = models.CharField(verbose_name=u'题目', max_length=50)
    content = models.TextField(verbose_name=u'内容', max_length=150,default='')
    content_detail = UEditorField(verbose_name=u'详细内容', width=600, height=300, imagePath="ad/ ",
                                  null=True,blank=True,filePath="ad/",default='')
    img = models.ImageField(verbose_name=u'图片', upload_to='ad/',default=u'',null=True,blank=True)
    url = models.URLField(verbose_name=u'文章链接', max_length=1000,default=u'',null=True,blank=True)
    user = models.ForeignKey(Profile, verbose_name=u'用户')
    belong = models.CharField(choices=(('hd', u'LA饮食娱乐咨询'), ('jj', u'入学与选课指南'), ('rx', u'新闻资讯'),
                                       ('jz', u'驾照与交通')), max_length=8, verbose_name=u'所属模块', default='jj')
    is_valid=models.BooleanField(verbose_name=u'是否有效',default=False)

    class Meta:
        verbose_name = u'新生投稿'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class SubmissionPicture(models.Model):
    post = models.ForeignKey(NewStudentSubmission,verbose_name=u'所属投稿')
    image = models.ImageField(blank = True,upload_to = 'house/%Y/%m',verbose_name=u'图片')

    class Meta:
        verbose_name = u"投稿图片"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self._meta.verbose_name

class ApplyEmail(models.Model):
    # 新生接机邮件
    belong = models.CharField(verbose_name=u'所属学校',max_length=50)
    email = models.EmailField(verbose_name=u'邮箱')
    name = models.CharField(verbose_name=u'联系人',max_length=50)

    class Meta:
        verbose_name = u"接机学校邮件"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.belong

class ApplyUrl(models.Model):
    # 接机URL填写
    url = models.URLField(verbose_name=u'链接',max_length=1000)
    belong = models.CharField(verbose_name=u'所属学校',max_length=20,choices=(('USC',u'USC'),('UCLA', u'UCLA'), ('UCSB', u'UCSB'), ('UCI', u'UCI')),default=u'USC')
    name = models.CharField(verbose_name=u'名称',max_length=100,default=u'')
    class Meta:
        verbose_name = u"接机提醒URL"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.belong

class Feedback(models.Model):
    title =  models.CharField(verbose_name=u'标题',max_length=200)
    content = models.CharField(verbose_name=u'内容',max_length=500)
    phone = models.CharField(verbose_name=u'手机号',max_length=20)
    content_detail = models.CharField(verbose_name=u'详细内容',max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name = u"首页反馈"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.title