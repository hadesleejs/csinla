# coding=utf-8
# author=lijiaoshou
# date='2017/9/1 10:19'
import exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core import mail
from csinla.settings import EMAIL_FROM


class WechatUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not request.jwt_user:
            msg = u'请先授权'
            raise exceptions.AuthenticationFailed(msg)
        return (request.jwt_user, request.jwt_user.uuid)



class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)



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
