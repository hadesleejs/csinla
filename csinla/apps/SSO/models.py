# coding=utf-8

from datetime import timedelta
import datetime
import logging
import time
import hashlib
import hmac
import random
import re
import qrcode

from PIL import Image

from cStringIO import StringIO

from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes

from csinla_accounts.models import Profile as User
# from django.contrib.auth.models import User
from SSO.exception import *

logger = logging.getLogger(__name__)

def salted_hmac(key_salt, value, secret):
  key = hashlib.sha1((key_salt + secret).encode('utf-8')).digest()
  return hmac.new(key, msg=force_bytes(value), digestmod=hashlib.sha1)

def get_random_string(length=16,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
  return ''.join([random.choice(allowed_chars) for i in range(length)])

class TicketManager(models.Manager):
  def create_ticket(self, ticket=None, **kwargs):
    if not ticket:
      ticket = self.create_ticket_str()
    if 'expires' not in kwargs:
      expires = now() + timedelta(seconds=self.model.TICKET_EXPIRE)
      kwargs['expires'] = expires
      t = self.create(ticket=ticket, **kwargs)
      logger.debug("Created %s %s" % (t.name, t.ticket))
      return t

  def create_ticket_str(self, prefix=None):
    if not prefix:
      prefix = self.model.TICKET_PREFIX
    return "%s-%d-%s" % (prefix, int(time.time()),
                             get_random_string(length=self.model.TICKET_RAND_LEN))

  def validate_ticket(self, ticket, renew=False):
    if not ticket:
      raise InvalidRequest("No ticket string provided")

    if not self.model.TICKET_RE.match(ticket):
      raise InvalidTicket("Ticket string %s is invalid" % ticket)

    try:
      t = self.get(ticket=ticket)
    except self.model.DoesNotExist:
      raise InvalidTicket("Ticket string %s is invalid" % ticket)

    if t.is_consumed():
      raise InvalidTicket("%s %s has already been used" %
                          (t.name, ticket))
    #t.consume()

    if t.is_expired():
      raise InvalidTicket("%s %s has expired" % (t.name, ticket))
    logger.debug("Validated %s %s" % (t.name, ticket))
    return t

  def delete_invalid_tickets(self):
    for ticket in self.filter(Q(consumed__isnull=False) |
                               Q(expires__lte=now())):
      try:
        ticket.delete()
      except models.ProtectedError:
        pass

  def consume_tickets(self, user):
    logger.info(user.id)
    for ticket in self.filter(user=user, consumed__isnull=True,
                               expires__gt=now()):
      logger.info(ticket)
      ticket.consume()

  def request_sign_out(self, user):
    for ticket in self.filter(user=user, consumed__gte=user.last_login):
      ticket.request_sign_out()

class Ticket(models.Model):
  TICKET_PREFIX = "TK"
  #TICKET_EXPIRE = getattr(settings, 'SESSION_COOKIE_AGE')
  TICKET_EXPIRE = 60 * 60 * 24 * 5
  TICKET_RAND_LEN = 32
  TICKET_RE = re.compile("^[A-Z]{2,3}-[0-9]{10,}-[a-zA-Z0-9]{%d}$" %TICKET_RAND_LEN)

  ticket = models.CharField(_('ticket'), max_length=255, unique=True)
  user = models.ForeignKey(User, verbose_name=_('user'))
  expires = models.DateTimeField(_('expires'))
  consumed = models.DateTimeField(_('consumed'), null=True)

  objects = TicketManager()

  def __str__(self):
    return self.ticket

  def consume(self):
    self.consumed = now()
    self.save()

  @property
  def name(self):
      return self._meta.verbose_name

  def is_consumed(self):
    if self.consumed:
      return True
    return False

  def is_expired(self):
    return self.expires <= now()

  def request_sign_out(self):
    pass

class TempTicketManager(models.Manager):
    def create_ticket(self, temp_ticket=None, **kwargs):
        if not temp_ticket:
            temp_ticket = self.create_ticket_str()
        if 'expires' not in kwargs:
            expires = now() + timedelta(seconds=self.model.TICKET_EXPIRE)
            kwargs['expires'] = expires
        t = self.create(temp_ticket=temp_ticket, **kwargs)
        logger.debug("Created %s %s" % (t.name, t.temp_ticket))
        return t

    def create_ticket_str(self, prefix=None):
        if not prefix:
            prefix = self.model.TICKET_PREFIX
        return "%s-%d-%s" % (prefix, int(time.time()),
                                 get_random_string(length=self.model.TICKET_RAND_LEN))

    def validate_ticket(self, temp_ticket, renew=False):
        if not temp_ticket:
          raise InvalidRequest("No temp_ticket string provided")

        if not self.model.TICKET_RE.match(temp_ticket):
          raise InvalidTicket("TempTicket string %s is invalid" % temp_ticket)

        try:
          t = self.get(temp_ticket=temp_ticket)
        except self.model.DoesNotExist:
          raise InvalidTicket("TempTicket string %s is invalid" % temp_ticket)

        if t.is_consumed():
          raise InvalidTicket("%s %s has already been used" %
                              (t.name, temp_ticket))
        #t.consume()

        if t.is_expired():
          raise InvalidTicket("%s %s has expired" % (t.name, temp_ticket))
        logger.debug("Validated %s %s" % (t.name, temp_ticket))
        return t

    def delete_invalid_tickets(self):
        for temp_ticket in self.filter(Q(consumed__isnull=False) |Q(expires__lte=now())):
            try:
                temp_ticket.delete()
            except models.ProtectedError:
                pass

    def consume_tickets(self, user):
        logger.info(user.id)
        for temp_ticket in self.filter(user=user, consumed__isnull=True,expires__gt=now()):
            logger.info(temp_ticket)
            temp_ticket.consume()

    def request_sign_out(self, user):
        for temp_ticket in self.filter(user=user, consumed__gte=user.last_login):
          temp_ticket.request_sign_out()

class TempTicket(models.Model):
    TICKET_PREFIX = "TTK"
    #TICKET_EXPIRE = getattr(settings, 'SESSION_COOKIE_AGE')
    TICKET_EXPIRE = 60 * 60 * 24 * 5
    TICKET_RAND_LEN = 32
    TICKET_RE = re.compile("^[A-Z]{2,3}-[0-9]{10,}-[a-zA-Z0-9]{%d}$" %TICKET_RAND_LEN)

    temp_ticket=models.CharField(_('temp_ticket'), max_length=255, unique=True)
    ticket=models.ForeignKey(Ticket,blank=True,null=True)
    expires = models.DateTimeField(_('expires'))
    consumed = models.DateTimeField(_('consumed'), null=True)
    qrcode_img = models.ImageField(u'二维码', upload_to='sso/tempticket/qrcode_img', blank=True, null=True)


    objects = TempTicketManager()

    def __str__(self):
        return self.temp_ticket

    def consume(self):
        self.consumed = now()
        self.save()

    @property
    def name(self):
        return self._meta.verbose_name

    def is_consumed(self):
        if self.consumed:
            return True
        return False

    def is_expired(self):
        return self.expires <= now()

    def request_sign_out(self):
        pass

    def save(self, *args, **kwargs):
        if not self.qrcode_img:
            img = qrcode.make(self.temp_ticket)
            buf = StringIO()
            img.save(buf)
            img_stream = buf.getvalue()
            img_name = '%s.png' % self.id
            self.qrcode_img = ContentFile(img_stream, img_name)
        super(TempTicket, self).save(*args, **kwargs)


class ViewItem(models.Model):
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name=u'用户',blank=True,null=True)
    link=models.URLField(u'访问地址')
    ip = models.GenericIPAddressField(u'登录IP')
    create_date=models.DateField(u'访问日期',blank=True,null=True)
    ip_view_type=models.CharField(u'ip访问类型',max_length=32,default='')

    def save(self, *args, **kwargs):
        need_result=False
        if not self.create_date:
            if not self.create_time:
                self.create_date=datetime.date.today()
            else:
                self.create_date=self.create_time.date()
        if not self.id:
            d = dict(IPViewResult.VIEW_TYPE_LIST)
            for (key, value) in d.items():
                if re.match(key,self.link):
                    if str(self.link).strip('/'):
                        need_result=True
                        if value!=u'帖子详情':
                            self.ip_view_type=value
                        else:
                            link_str=str(self.link).strip('/')
                            post_id=int(link_str.split('/')[-1])
                            from csinla_posts.models import Post
                            try:
                                self.ip_view_type=Post.objects.get(id=post_id).belong_to
                            except Post.DoesNotExist:
                                pass
        super(ViewItem, self).save(*args, **kwargs)
        if need_result:
            try:
                ipviewresult=IPViewResult.objects.get(create_date=self.create_date,view_type=self.ip_view_type)
            except IPViewResult.DoesNotExist:
                ipviewresult=IPViewResult.objects.create(create_date=self.create_date,view_type=self.ip_view_type)
            ipviewresult.view_count+=1
            ipviewresult.user_view_count+=1
            if not ViewItem.objects.filter(create_date=self.create_date,ip_view_type=self.ip_view_type,ip=self.ip).exclude(id=self.id).exists():
                ipviewresult.ip_count+=1
            if self.creator:
                ipviewresult.user_view_count+=1
                if not self.creator in ipviewresult.join_list.all():
                    ipviewresult.join_list.add(self.creator)
            ipviewresult.save()

class IPViewResult(models.Model):
    create_date=models.DateField(u'访问日期')
    view_count=models.IntegerField(u'IP访问次数',default=0)
    ip_count=models.IntegerField(u'访问IP量',default=0)
    VIEW_TYPE_LIST=(
        (r'^accounts/carfax/$',u'carfax'),
        (r'^accounts/airport/$',u'新生接机'),
        (r'^accounts/parking/$',u'免费停车1'),
        (r'^accounts/parking2/$',u'免费停车2'),
        (r'^posts/(?P<posts_id>[0-9]+)/$',u'帖子详情'),
    )
    view_type=models.CharField(u'访问类型',max_length=32,default='')
    user_view_count=models.IntegerField(u'用户访问次数',default=0)
    user_count=models.IntegerField(u'用户访问量',default=0)
    collect_count=models.IntegerField(u'用户收藏量',default=0)
    join_list=models.ManyToManyField(User,verbose_name=u'访问用户')
    last_change_time=models.DateTimeField(u'最后修改时间',auto_now=True)


    class Meta:
        verbose_name = u"IP浏览记录"
        verbose_name_plural = verbose_name
        ordering=['-create_date','view_type']

    @property
    def view_detail(self):
        totle_view_count=0
        totle_ip_array=[]
        totle_join_list=User.objects.none()
        totle_user_view_count=0
        totle_collect_count=0
        ipviewresult_list=IPViewResult.objects.filter(create_date__gte=self.create_date,view_type=self.view_type)
        for ipviewresult in ipviewresult_list:
            totle_view_count+=ipviewresult.view_count
            totle_user_view_count+=ipviewresult.user_view_count
            totle_collect_count+=ipviewresult.collect_count
            totle_join_list=totle_join_list|ipviewresult.join_list.all()
        totle_join_list=totle_join_list.distinct()
        viewitem_list=ViewItem.objects.filter(create_time__gte=str(self.create_date),ip_view_type=self.view_type)
        for viewitem in viewitem_list:
            if not viewitem.ip in totle_ip_array:
                totle_ip_array.append(viewitem.ip)
        return u'截至当前共%s个IP，%s次浏览（已登录用户共%s人%s人次浏览，%s次收藏）' % (len(totle_ip_array),totle_view_count,totle_join_list.count(),totle_user_view_count,totle_collect_count)

    def save(self, *args, **kwargs):
        if self.id:
            self.user_count=self.join_list.all().count()
        super(IPViewResult, self).save(*args, **kwargs)