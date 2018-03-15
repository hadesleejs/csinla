# _*_ coding: utf-8 _*_
from random import Random
import os
from email.mime.image import MIMEImage
from django.core import mail
from django.core.mail import send_mail
from email.mime.image import MIMEImage
from csinlafun.settings import EMAIL_FROM

def send_paid_email(order):
    title=u'支付成功通知'
    html = '''
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
         <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
         <title>email</title>

        </head>
        <body>
        <div>
          <p>%s您好：</p>
             <p style="text-indent:2em">新用户提醒</p>
             <p style="text-indent:2em">序列号：%s</p>
             <p style="text-indent:2em">票面价值/人数：$%s/%s人</p>
             <p style="text-indent:2em">时间：%s</p>
             <p style="text-indent:2em">活动名称：%s</p>
             <p style="text-indent:2em">用户称呼：%s</p>
             <p style="text-indent:2em">用户邮箱：%s</p>
             <p>CSinLA Team</p>
             </div>
        </body>
        </html>
        ''' % (order.activitytimeitem.activity.hoster.name.encode('utf-8'),
                order.order_no.encode('utf-8'),
                order.activitytimeitem.activity.pre_price*order.join_count,
                order.join_count,order.activitytimeitem.activity_time,
                order.activitytimeitem.activity.name.encode('utf-8'),
                order.customer_name,order.customer_email
            )
    msg = mail.EmailMessage(title.encode('utf-8'), html, EMAIL_FROM, [order.customer_email])
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    #image = add_img(path+str(im.img.url), 'test_cid')
    #msg.attach(image)
    if msg.send():
        return True
    else:
        return False
