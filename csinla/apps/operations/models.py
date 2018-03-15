#_*_ encoding: utf-8 _*_

from __future__ import unicode_literals
from datetime import datetime
from django.db.models.signals import post_save
from django.db import models
from django.db.models.signals import post_delete
from csinla_accounts.models import Profile, Unread
from csinla_posts.models import Car, Rent, Post
from django_comments.models import Comment
# Create your models here.

class CarComments(models.Model):
    user = models.ForeignKey(Profile, verbose_name=u"用户")
    car_post = models.ForeignKey(Car, verbose_name=u"车辆帖子")
    comments = models.CharField(max_length=200, verbose_name=u"评论")


class UserCarPost(models.Model):
    user = models.ForeignKey(Profile, verbose_name=u"用户")
    car_post = models.ForeignKey(Car, verbose_name=u"车辆帖子")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户发帖(车)"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(Profile, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据ID")
    fav_type = models.IntegerField(choices=((1, u"二手车"), (2, u"租房")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserRentPost(models.Model):
    user = models.ForeignKey(Profile, verbose_name=u"用户")
    rent_post = models.ForeignKey(Rent, verbose_name=u"租房帖子")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户发帖(房)"
        verbose_name_plural = verbose_name


class Warnings(models.Model):
    posts_type = models.CharField(max_length=15, default="", verbose_name=u"帖子类型")
    content = models.CharField(max_length=500, default="", verbose_name=u"警示语")

    def __unicode__(self):
        return self.posts_type + "_警示语"

    class Meta:
        verbose_name = u"警示语"
        verbose_name_plural = verbose_name


class Protocol(models.Model):
    types = models.CharField(max_length=15, default="", verbose_name=u"协议类型")
    content = models.TextField(verbose_name=u"协议内容")

    def __unicode__(self):
        return self.types

    class Meta:
        verbose_name = u"用户协议"
        verbose_name_plural = verbose_name


class Advertising(models.Model):
    belong_to = models.CharField('所属版块',max_length=15, default="")
    text=models.CharField(u'文案内容',max_length=128,default='')
    url = models.URLField(verbose_name=u"广告链接", blank=True, null=True)
    img = models.ImageField(blank = True, null=True, upload_to = 'ad/',verbose_name=u"广告图")

    def __unicode__(self):
        return  u'%s（id为：%s）' % (self.belong_to,self.id)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'belong_to':self.belong_to,
            'text':self.text,
            'url': self.url,
            'img':self.img.url,
        }

    class Meta:
        verbose_name = u"广告"
        verbose_name_plural = verbose_name
        ordering = ["belong_to"]


class EmailPic(models.Model):
    types = models.CharField(max_length=15, default="", verbose_name=u"类型")
    img = models.ImageField(blank = True, upload_to = 'ad/')

    def __unicode__(self):
        return u"图片 " + str(self.id)

    class Meta:
        verbose_name = u"发送邮件所带图片"
        verbose_name_plural = verbose_name


class FavoriteNotice(models.Model):
    fav_user = models.ForeignKey(Profile, on_delete = models.CASCADE)
    post_user_id = models.IntegerField()
    has_readed = models.BooleanField(default=False)
    post_title = models.CharField(max_length=50, default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    post_id = models.IntegerField()
    has_readed = models.BooleanField(default=False)

def far_notice(sender, instance, *args, **kwargs):
    posts  = Post.objects.get(id=instance.fav_id)
    notice = FavoriteNotice(fav_user=instance.user, post_user_id=posts.author.id, post_title=posts.title, add_time=instance.add_time, post_id=posts.id)
    notice.save()
    un = Unread()
    un.notice_id = notice.id
    un.user_id = posts.author.id
    un.save()

post_save.connect(far_notice, sender=UserFavorite)


def delet_posts(sender, instance, *args, **kwargs):
    if Comment.objects.filter(object_pk=instance.id).exists():
        Comment.objects.filter(object_pk=instance.id).delete()
    if FavoriteNotice.objects.filter(post_id=instance.id).exists():
        FavoriteNotice.objects.filter(post_id=instance.id).delete()


post_delete.connect(delet_posts, sender=Post)
