# _*_ coding: utf-8 _*_
__author__ = 'JK'
__date__ = '17/2/18 下午1:15'
from random import Random
import os
from email.mime.image import MIMEImage
from django.core import mail
from django.core.mail import send_mail
from email.mime.image import MIMEImage
from csinla_accounts.models import EmailVerifyRecord, BuyCarNotice
from csinla.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in xrange(randomlength):
        str += chars[random.randint(0, length)]

    return str

def send_user_remove_mail(email, send_type="user_remove"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = 'user_rm'
    email_record.save()
    title=u'账号注销通知'
    connect_url = 'http://www.csinla.com/contactservice/'
    regist_url = 'http://www.csinla.com/accounts/registerstu/'
    html = '''
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
         <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
         <title>email</title>

        </head>
        <body>
        <div>
          <p>尊敬的用户您好</p>
             <p style="text-indent:2em">因为您长时间未激活注册邮箱，您所注册的账号和相关信息已被删除。对此带来的不便，我们深感抱歉。</p>
             <p style="text-indent:2em">对于注册未激活的通常原因为: 填写的邮件地址无效，验证邮件在您的垃圾邮箱
如果您遇到其他相关注册问题，请<a href="%s">联系我们客服</a>。您也可以尝试<a href="%s">再次注册</a>。</p>
             <p style="text-indent:2em">谢谢您的耐心阅读和支持</p>
             <p>CSinLA Team</p>
             </div>
        </body>
        </html>
        ''' % (connect_url,regist_url)
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    #image = add_img(path+str(im.img.url), 'test_cid')
    #msg.attach(image)
    if msg.send():
        return True
    else:
        return False

def send_register_mail(email, send_type="register", code=0):
    if not code:
        email_record = EmailVerifyRecord()
        code = random_str(16)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "欢迎注册CSinLA"
        email_body = "请点击下面的链接激活你的账号: http://www.csinla.com/active/{0}".format(code)

        return send_mail(email_title, email_body, EMAIL_FROM, [email])
    return None


def send_resetpass_mail(name, email, send_type="resetpass"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "resetpass":
        email_title = "找回密码"
        email_body = u"亲爱的%s, 您在CSinLA提交了找回密码请求。请点击下面的链接重置密码:  http://www.csinla.com/reset/%s"%(name, code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def send_feedback_mail(body, send_type="Feedback"):     
    email = 'csinla.corp@gmail.com'
    if send_type == "Feedback":
        email_title = 'Feedback'
        email_body = body
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == "buycar":
        try:
            email_list = BuyCarNotice.objects.all()
            email = []
            for e in email_list:
                email.append(e.email)
        except:
            email = ['csinla.corp@gmail.com']
        email_title = 'buycar'
        email_body = body
        send_status = send_mail(email_title, email_body, EMAIL_FROM, email)


def add_img(src, img_id):
    fp = open(src, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header('Content-ID', '<'+img_id+'>')
    return msg_image


def send_util(im, name, belong_to, title, user_email, posts_id,creator_name):
    path = '/var/www/csinla/csinla' #os.getcwd()
    #path_use = path.replace('\\', '/')
    email = user_email
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = user_email
    email_record.send_type = 'off_posts'
    email_record.save()
    off_url = 'http://www.csinla.com/accounts/off/' + str(posts_id) + '/' + str(code)
    stop_url = 'http://www.csinla.com/accounts/stop/' + str(posts_id) + '/' + str(code)
    html = '''
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
         <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
         <title>email</title>

        </head>
        <body>
        <div>
          <p>尊敬的 %s</p>
             <p style="text-indent:2em">您在 %s 模块发的（%s）被用户%s收藏了！！！</p>
             <p style="text-indent:2em">您可以<a href="www.csinla.com/accounts/login">登陆</a>您的账号查看他的联系方式呦，快快和他取得联系吧~</p>
             <p style="text-indent:2em">点击<a href="%s">这里</a>下架（%s），并停止收到该帖相关通知</p>
             <p style="text-indent:2em">点击<a href="%s">这里</a>停止收到该帖相关通知</p>
        	 <p> CSinLA Team</p>
             <img src="cid:test_cid">
             </div>
        </body>
        </html>
        ''' % (name.encode('utf-8'), belong_to.encode('utf-8'), title.encode('utf-8'),creator_name.encode('utf-8'), off_url, title.encode('utf-8'), stop_url)
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [user_email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    # image = add_img(path+str(im.img.url), 'test_cid')
    # msg.attach(image)
    if msg.send():
        return True
    else:
        return False


def send_util2(im, name, belong_to, title, user_email, posts_id,content):
    path = '/var/www/csinla/csinla' #os.getcwd()
    #path_use = path.replace('\\', '/')
    email = user_email
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = user_email
    email_record.send_type = 'off_posts'
    email_record.save()
    off_url = 'http://www.csinla.com/accounts/off/' + str(posts_id) + '/' + str(code)
    stop_url = 'http://www.csinla.com/accounts/stop/' + str(posts_id) + '/' + str(code)
    html = '''
   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
     <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
     <title>email</title>

    </head>
    <body>
    <div>
      <p>尊敬的 %s</p>
         <p style="text-indent:2em">您在 %s 模块发的（%s）收到新的评论：“%s”</p>
         <p style="text-indent:2em">您可以<a href="www.csinla.com/accounts/login">登陆</a>您的账号查看他的联系方式呦，快快和他取得联系吧~</p>
         <p style="text-indent:2em">点击<a href="%s">这里</a>下架（%s），并停止收到该帖相关通知</p>
         <p style="text-indent:2em">点击<a href="%s">这里</a>停止收到该帖相关通知</p>
         <p>CSinLA Team</p>
         <img src="cid:test_cid">
         </div>
    </body>
    </html>
    ''' % (name.encode('utf-8'), belong_to.encode('utf-8'), title.encode('utf-8'),content.encode('utf-8'), off_url, title.encode('utf-8'), stop_url)
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [user_email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    # image = add_img(path+str(im.img.url), 'test_cid')
    # msg.attach(image)
    if msg.send():
        return True
    else:
        return False


def send_mail_carfax(name,vin,reply_text,email):
    html = '''
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
         <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
         <title>email</title>

        </head>
        <body>
        <div>
          <p>%s 您好：</p>
             <p style="text-indent:2em">我们已经查看了您所留的Vin number/Plate number（%s），您需要查询的Carfax report我们已经附在此邮件中。如有任何问题，您可以致电 (626) 662-3809联系我们的客服。也可以直接扫码添加微信好友，与我们客服人员一对一咨询~</p>
             <p style="text-indent:2em">”%s”。</p>
             <p style="text-indent:2.5em;font-size:12px">感谢您的咨询，期待您的再次使用！</p>
             <img src="http://csinla.com/static/images/carfax_qr.png">
             </div>
        </body>
        </html>
        ''' % (name.encode('utf-8'),vin.encode('utf-8'),reply_text.encode('utf-8'))
    title ='Carfax report'
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    # image = add_img(path+str(im.img.url), 'test_cid')
    # msg.attach(image)
    if msg.send():

        return True
    else:
        return False





def send_mail_apply(email, name='',sex='',wx='',phone=''
                    ,flight='',departure='',landing='',address='',contactor='',contacts_phone=''):
    # 新生接机申请，发送邮件给负责人

    html = '''
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
         <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
         <title>email</title>

        </head>
        <body>
        <div>
          <p>您好</p>
             <p style="text-indent:2em">有人在CSINLA，申请了接机，请注意查收~</p>
             <p style="text-indent:2em">学生姓名：%s</p>
             <p style="text-indent:2em">性别：%s</p>
             <p style="text-indent:2em">微信：%s</p>
             <p style="text-indent:2em">电话：%s</p>
             <p style="text-indent:2em">航班：%s</p>
             <p style="text-indent:2em">起飞时间：%s</p>
             <p style="text-indent:2em">落地时间：%s</p>
             <p style="text-indent:2em">地址：%s</p>
             <p style="text-indent:2em">联系人：%s</p>
             <p style="text-indent:2em">联系人电话：%s</p>

             </div>
        </body>
        </html>
        '''% (name.encode('utf-8'),sex.encode('utf-8'),wx.encode('utf-8'),phone.encode('utf-8'),
              flight.encode('utf-8'),departure.encode('utf-8'),landing.encode('utf-8'),address.encode('utf-8'),
              contactor.encode('utf-8'),contacts_phone.encode('utf-8'),)
    title ='新生接机'
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    # image = add_img(path+str(im.img.url), 'test_cid')
    # msg.attach(image)
    if msg.send():

        return True
    else:
        return False
