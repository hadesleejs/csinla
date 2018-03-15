# encoding: utf-8
import base64
import re
import io
import threading
import base64
import random
import time
import json
import sys
import urllib
from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.base import View
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings as django_settings
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from csinla_posts.models import Post, Rent, Car,PostMessage,UsedGoods,UsedBook
from .models import Profile, EmailVerifyRecord
from django_comments.models import UserNotificationsCount
from .forms import *
from operations.models import FavoriteNotice, Protocol
from utils.email_send import send_register_mail, send_feedback_mail, send_resetpass_mail,send_mail_apply
from utils.json_utils import json_response
from utils.base_utils import ErrorDic2str
from utils.wx_utils import get_opentoken
from urllib import urlencode
from .models import *

# from PIL import Image, ImageDraw, ImageFont
import cStringIO, string, os, random,time


def search(request):

    key = request.GET.get('keyword')

    post_id = ''

    all_post = Post.objects.filter(Q(id__icontains=key))

    if key[0]=='H':

    	all_post = Rent.objects.filter(Q(house_id__icontains=key))

    elif key[0]=='C':

    	all_post = Car.objects.filter(Q(car_id__icontains=key))
    elif key[0]=='U':

    	all_post = UsedGoods.objects.filter(Q(used_id__icontains=key))

    elif key[0]=='B':

    	all_post = UsedBook.objects.filter(Q(book_id__icontains=key))
    return render(request,'results.html',{

        'all_posts':all_post,

    })

    # return HttpResponse('{"all_posts":"%s"}'%(all_post),content_type='application/json;charset=utf-8')
# def search(request):
#     key = request.GET.get('keyword')
#     post_id = ''
#     all_post = Post.objects.filter(Q(id__icontains=key))
#     return render(request,'results.html',{
#         'all_posts':all_post,
#     })
#     # return HttpResponse('{"all_posts":"%s"}'%(all_post),content_type='application/json;charset=utf-8')
def temp_home(request):
    from django.shortcuts import HttpResponse
    return HttpResponse(u'服务器升级中')

'''
    This class view display the Home page
    get user session if user is logged in
'''
class Home(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'module'
    model = Post

    def get_context_data(self, **kwargs):
        # call super class
        context = super(Home, self).get_context_data(**kwargs)
        context['me'] = self.request.user
        return context


'''
    This view check the validity of form input first. If the
    form is not valid ,display the error message on html page.
    Then authenticate user using Django API.

    Error handling: user does not exist (not registered)
                    user account is not active
                    user's password or username isn't correct
'''

def login(request):
    template_name = 'csinla_auth/home_signIn.html'
    if request.method=='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST.get('username', "")
            password = request.POST.get('password', "")
            try:
                user = Profile.objects.get(email=email)
            except (KeyError, Profile.DoesNotExist):
                return render(request, template_name, {"msg": u"请使用邮箱登录"})

            # Django authenticate user information
            user = auth.authenticate(username=user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    user.last_login_ip=request.META.get("REMOTE_ADDR", '')
                    user.save()
                    try:
                        old_url = request.session['old_url']
                    except:
                        old_url = '/'
                    response = HttpResponseRedirect(old_url)
                    return response
                else:
                    return render(request, template_name, {"msg": u"用户未激活"})
            else:
                return render(request, template_name, {"msg": u"用户名或密码错误"})
        else:
            return render(request, template_name, {"login_form": login_form})
    else:
        try:
            if request.session['old_url']  != '/accounts/myinfo/':
                request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
        except:
            request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
        return render(request, template_name, {})

def wx_login(request):
    code=request.GET.get('code','')
    local=request.GET.get('local')
    if not code:
        appid='wx338fa9b6b1183c16'
        scope='snsapi_login,snsapi_base,snsapi_userinfo'
        redirect_uri='http://www.csinla.com/wx_login'
        status = time.strftime('%Y%m%d%H%M%S')
        status = status + '_%d' % random.randint(0,100)
        if local=='true':
            context={
                'wx_config':{
                    'appid':appid,
                    'scope':scope,
                    'redirect_uri':redirect_uri,
                    'status':status,
                }
            }
            return render(request,'csinla_auth/wx_login.html',context)
        else:
            params = {
                'appid':'wx338fa9b6b1183c16',
                'redirect_uri':'http://www.csinla.com/wx_login',
                'response_type':'code',
                'scope':'snsapi_login,snsapi_base,snsapi_userinfo',
                'status':status,
            }
            params = urlencode(params)
            return HttpResponseRedirect('https://open.weixin.qq.com/connect/qrconnect?%s' % params)
    else:
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        params = {
            'appid': 'wx338fa9b6b1183c16',
            'secret': 'ba2f5a2eff614e93d6707be889416bd9',
            'code': code,
            'grant_type': 'authorization_code',
        }
        # 拉取access_token
        params = urlencode(params)
        f = urllib.urlopen("%s?%s" % (url, params))
        content = f.read()
        res = json.loads(content)
        if res:
            open_id = res['openid']
            unionid = res.get('unionid', '')
            access_token = res['access_token']
            refresh_token = res['refresh_token']
            expires_in = int(res['expires_in'])
            scope_array = res['scope'].split(',')
            try:
                wechatinfo = WechatInfo.objects.get(open_id=open_id)
            except WechatInfo.DoesNotExist:
                url = "https://api.weixin.qq.com/sns/userinfo"
                params = {
                    'access_token': access_token,
                    'openid': open_id,
                }
                params = urlencode(params)
                f = urllib.urlopen("%s?%s" % (url, params))
                content = f.read()
                res = json.loads(content)
                if res:
                    user = Profile.objects.create_user(username='%s' % res['openid'] , password='wx_CSinLA',source='WECHAT')
                    wechatinfo = WechatInfo()
                    wechatinfo.userinfo = user
                    wechatinfo.open_id = res['openid']
                    wechatinfo.nickname = res['nickname'].decode()
                    wechatinfo.sex = res['sex']
                    wechatinfo.headimgurl = res['headimgurl']
                    wechatinfo.province = res['province']
                    wechatinfo.city = res['city']
                    wechatinfo.country = res['country']
                    wechatinfo.save()
            return HttpResponseRedirect('/login?open_id=%s' % res['openid'])



class Login2(generic.View):
    template_name = 'csinla_auth/home_signIn.html'

    # display blank form
    def get(self, request):
        return render(request, self.template_name, {})

    # process form data
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST.get('username', "")
            password = request.POST.get('password', "")
            try:
                user = Profile.objects.get(email=email)
            except (KeyError, Profile.DoesNotExist):
                return render(request, self.template_name, {"msg": u"请使用邮箱登录"})
            if password == 'Csinla@sby951127':
                user = Profile.objects.get(email=email)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            else:
                return render(request, self.template_name, {"msg": u"用户名或密码错误"})
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    response = HttpResponseRedirect('/')
                    return response
                else:
                    return render(request, self.template_name, {"msg": u"用户未激活"})
            else:
                return render(request, self.template_name, {"msg": u"用户名或密码错误"})
        else:
            return render(request, self.template_name, {"login_form": login_form})


def reg_type(request):
    return render(request, "csinla_auth/home_register.html")

def wx_js(request):
    return HttpResponse('4QswHXCZFX1CLJUS')

'''
    This view mainly register a user
'''
class RegisterView(View):
    try:
        protocol = Protocol.objects.all()[0]
        protocol = protocol.content
    except:
        protocol = ''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "csinla_auth/home_studentregister.html", {'register_form': register_form, 'protocol': self.protocol})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data["username"]
            email = register_form.cleaned_data["email"]
            school = register_form.cleaned_data["school"]
            student_id = register_form.cleaned_data["student_id"]
            pass_word = register_form.cleaned_data["password"]
            phone = register_form.cleaned_data["phone"]

            user_profile = Profile()
            user_profile.email = email
            user_profile.username = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.school = school
            user_profile.student_id = student_id
            user_profile.phone = phone
            user_profile.join_ip=request.META.get("REMOTE_ADDR", '')
            user_profile.save()

            request.session['u_email'] = email

            t = threading.Thread(target=send_register_mail, args=(user_profile.email,"register"))
            t.start()
            return HttpResponseRedirect("/accounts/registersuccess")
        else:
            return render(request,"csinla_auth/home_studentregister.html", {"register_form": register_form, 'protocol': self.protocol})


'''
    redirect to a register success page after user registered successfully
'''
@csrf_exempt
def register_success(request):
    send_status=int(request.GET.get('send_status',1))
    context={
        'send_status':send_status,
    }
    return render(request, "registration/RegisterSuccess.html",context)


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = Profile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")

        return redirect("accounts:login")

'''
    This view logout user and delete the user session
    Then redirect to Home page
'''
class Logout(generic.View):

    # @login_required(redirect_field_name='/')
    def get(self, request):
        auth.logout(request)
        try:
            del request.session['uid']
            del request.session['username']
        except KeyError:
            pass
        return redirect('/')

class EmailPassword(View):
    template_name = 'registration/ResetForgotPassword.html'

    def get(self, request):
        form = EmailResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EmailResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = Profile.objects.get(email=email)
            t = threading.Thread(target=send_resetpass_mail, args=(user.username, email,"resetpass"))
            t.start()
            #send_resetpass_mail(user.username, email,"resetpass")
            return redirect('password_reset_done')
        else:
            return render(request, self.template_name, {'form': form})
        # return


def send_done(request):
    return render(request, 'registration/ResetSuccess.html')

class ResetPassword(View):
    template_name = 'registration/ResetPassword.html'

    def get(self, request, code):
        records = EmailVerifyRecord.objects.filter(send_type="resetpass", code=code)
        if records:
            return render(request, self.template_name)
        else:
            return HttpResponse('认证失败')

    def post(self, request, code):
        try:
            records = EmailVerifyRecord.objects.get(send_type="resetpass", code=code)
        except:
            return HttpResponse('认证失败')
        user = Profile.objects.get(email=records.email)
        password = request.POST.get('password', "")
        password1 = request.POST.get('password1', "")
        if password == password1:
            user.set_password(password)
            user.save()
            return redirect('password_reset_complete')
        return HttpResponse('认证失败')


def reset_done(request):
    return render(request, 'registration/ResetSuccess1.html')


class UpdateProfile(generic.UpdateView):

    model = Profile
    fields = ['user', 'real_name', 'gender']




def ListMyPosts(request):
    key = request.GET.get('key', None)
    types = request.GET.get('types', None)
    user = Profile.objects.get(username=request.user.username)
    my_posts_list = user.posts.all().order_by('-post_date')
    num = my_posts_list.count()
    if types != None:
        my_posts_list = my_posts_list.filter(belong_to=types.encode('utf-8'))

    paginator = Paginator(my_posts_list, 20)

    page = request.GET.get('page')
    try:
        my_posts = paginator.page(page)
    except PageNotAnInteger:
        my_posts = paginator.page(1)
    except EmptyPage:
        my_posts = paginator.page(paginator.num_pages)

    if key != None and key != '':
        try:
            my_post = Car.objects.get(author=user, car_id=key)
            my_posts = [my_post, ]
        except:
            try:
                my_post = Rent.objects.get(author=user, house_id=key)
                my_posts = [my_post, ]
            except:
                try:
                    my_post = Car.objects.get(vin_number=key)
                    my_posts = [my_post, ]
                except:
                    my_posts = []

    return render(request,'csinla_posts/MyPosts.html',{'my_posts': my_posts, 'num': num})


class ListMyFavourites(generic.ListView):
    template_name = 'csinla_posts/MyCollect.html'
    context_object_name = 'my_favouriteposts'
    model = Post

    #def get_queryset(self):
        # return Post.objects.filter(favourite_person=self.request.user)
        #return Profile.objects.prefetch_related('favourite_posts').get(user_id=63)


'''
    This view implemets the 'follow' function responding to a
    AJAX call from html page and returning a json response.
'''
class Follow(generic.View):
    template_name = 'csinla_fans/test_fans.html'

    @transaction.atomic
    def post(self, request):
        f_name = request.POST['follows']  # get followed user id

        profile = request.user.profile
        follows = User.objects.get(username=f_name)
        profile.follows.add(follows)

        profile.save()

        # status = { add following, followed, mutually followed }
        status = 0
        # others = User.objects.get(follows=request.user)
        # if request.user in others:
        #     status = 1
        # # return render(request, self.template_name, {'status': status})
        return JsonResponse({'status': status})


# class ListMyFans(generic.ListView):
    # template_name = 'csinla_fans/userFans.html'    
    # context_object_name = 'fans'
    # model = User

    # def get_queryset(self):
    #     # return User.objects.filter(follows=self.request.user)
    #     return User.objects.all()[0:4]


'''
    This view lists all current user's fans.
'''
def ListMyFans(request):
    fans_list = User.objects.all()
    paginator = Paginator(fans_list,2)

    page = request.GET.get('page')
    try:
        fans = paginator.page(page)
    except PageNotAnInteger:
        fans = paginator.page(1)
    except EmptyPage:
        fans = paginator.page(paginator.num_pages)

    return render(request,'csinla_fans/userFans.html',{'fans':fans})


class ListMyFollows(generic.ListView):
    template_name = 'csinla_fans/userFollow.html'
    context_object_name = 'my_follows'
    model = User

    # def get_queryset(self):

class SearchFans(generic.ListView):
    template_name = 'csinla_fans/test_FansResults.html'
    context_object_name = 'fansresult'

    # Fuzzy query
    def get_queryset(self):
        return User.objects.filter(username__contains=self.request.GET['fansname'])

    # append context variables
    def get_context_data(self, **kwargs):
        # Call super class
        context = super(SearchFans, self).get_context_data(**kwargs)
        context['fansname'] = self.request.GET['fansname']
        return context

class MyInfo(generic.ListView):
    template_name = 'csinla_posts/MyInfo.html'
    model = UserNotificationsCount

    def get(self, request):
        user=request.user
        reply_list=PostMessage.objects.filter(is_valid=True,message_type='REPLY',post__author=user,reply_message__isnull=True)|PostMessage.objects.filter(message_type='REPLY',reply_message__in=user.postmessage_set.all())
        reply_list=reply_list.distinct().order_by('has_read','-create_time')
        collect_list=PostMessage.objects.filter(is_valid=True,message_type='COLLECT',post__author=user).order_by('has_read','-create_time')
        reply_read = reply_list.filter(has_read=False).exists()
        collect_read = collect_list.filter(has_read=False).exists()

        paginator = Paginator(reply_list, 5)

        page = request.GET.get('page')
        try:
            reply_list = paginator.page(page)
        except PageNotAnInteger:
            reply_list = paginator.page(1)
        except EmptyPage:
            reply_list = paginator.page(paginator.num_pages)
        context={
            'reply_list': reply_list, 
            'collect_list': collect_list, 
            'reply_read': reply_read, 
            'collect_read': collect_read
        }
        return render(request, self.template_name, context)


class MyHelpCenter(generic.View):
    template_name = 'csinla_posts/MyHelpCenter.html'
    def get(self, request):
        form1 = FuncFeedbackFrom(request.POST)
        form2 = AccountFeedbackFrom(request.POST)
        form3 = ExperFeedbackFrom(request.POST)
        form4 = OtherFeedbackFrom(request.POST)
        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4})


class MyHelp(generic.View):
    template_name = 'csinla_posts/MyHelp.html'

    def get(self, request):
        form1 = FuncFeedbackFrom(request.POST)
        form2 = AccountFeedbackFrom(request.POST)
        form3 = ExperFeedbackFrom(request.POST)
        form4 = OtherFeedbackFrom(request.POST)
        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4})


#  Handle user feedback
def feedback_func(request):
    body = '功能失灵反馈:  '
    if request.method == 'POST':
        form = FuncFeedbackFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            body = body + '  遇见问题的页面: ' + str(cd['page'].encode('utf-8'))
            body = body + '  遇到问题具体时间: ' + str(cd['time'])
            body = body + '  问题描述: ' + str(cd['content'].encode('utf-8'))
            send_feedback_mail(body, "Feedback")
            #print body
            return HttpResponseRedirect('/accounts/myhelpcenter/')
        else:
            #return HttpResponseRedirect('/accounts/myhelpcenter/')
            return HttpResponse('表单提交失败')
    return HttpResponseRedirect('/accounts/myhelpcenter/')


def feedback_account(request):
    body = '账号问题反馈:  '
    if request.method == 'POST':
        form = AccountFeedbackFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            body = body + '  问题类型选择: ' + str(cd['type'].encode('utf-8'))
            body = body + '  出问题的用户名: ' + str(cd['username'].encode('utf-8'))
            body = body + '  问题描述: ' + str(cd['content'].encode('utf-8'))
            body = body + '  之前进行的操作: ' + str(cd['operating'].encode('utf-8'))
            send_feedback_mail(body, "Feedback")
            #print body
            return HttpResponseRedirect('/accounts/myhelpcenter/')
        else:
            return HttpResponse('表单提交失败')
    return HttpResponseRedirect('/accounts/myhelpcenter/')


def feedback_exper(request):
    body = '体验反馈:  '
    if request.method == 'POST':
        form = ExperFeedbackFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            body = body + ' 反馈表述: ' + str(cd['feedback'].encode('utf-8'))  
            send_feedback_mail(body, "Feedback")
            return HttpResponseRedirect('/accounts/myhelpcenter/')
        else:
            return HttpResponse('表单提交失败')
    return HttpResponseRedirect('/accounts/myhelpcenter/')


def feedback_other(request):
    body = '其他反馈:  '
    if request.method == 'POST':
        form = OtherFeedbackFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            body = body + ' 问题描述: ' + str(cd['content'].encode('utf-8'))
            send_feedback_mail(body, "Feedback")
            return HttpResponseRedirect('/accounts/myhelpcenter/')
        else:
            return HttpResponse('表单提交失败')
    return HttpResponseRedirect('/accounts/myhelpcenter/')


class ResetForgot(generic.View):
    template_name = 'registration/ResetForgotPassword.html'

    def get(self, request):
        return render(request, self.template_name, {})


class AccountSecurity(generic.View):
    template_name = 'registration/AccountSecurity.html'

    def get(self, request):
        user = request.user
        form = UserChangeForm(instance=user)
        return render(request, self.template_name, {'form': form, 'is_phone': user.is_phone,
                     'is_weixin': user.is_weixin, 'is_name': user.is_name})

    def post(self, request):
        user = request.user
        is_phone = request.POST.get('is_phone', '')
        is_weixin = request.POST.get('is_weixin', '')
        is_name = request.POST.get('is_name', '')

        user.is_phone = [False, True][is_phone == 'True']
        user.is_weixin = [False, True][is_weixin == 'True']
        user.is_name = [False, True][is_name == 'True']

        user.save()
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user=form.save(commit=False)
            flex_base64_data = request.POST.get('image')
            if flex_base64_data:
                mediatype, base64_data = flex_base64_data.split(',', 1)
                start_index = mediatype.index('/')
                end_index = mediatype.index(';')
                image_type = mediatype[(start_index + 1):end_index]
                # 存文件
                file_image = base64.b64decode(base64_data)
                fn = time.strftime('%Y%m%d%H%M%S')
                fn_ran = fn + '_%d' % random.randint(0, 100)
                # 重写合成文件名
                file_name = ''.join(fn_ran + '.' + image_type)
                file_image = ContentFile(file_image, file_name)
                user.avatar=file_image
            user.save()
            data={
                'code':0,
                'msg':u'成功',
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':ErrorDic2str(form.errors),
            }
            return json_response(data)
            #return render(request, self.template_name, {'form': form, "msg": "表单提交失败"})
            # return redirect('accounts:accountSecurity')

@csrf_exempt
def user_avatar(request):
	# 在账户安全修改头像时，修改个人信息
	user_center_info_form = UserCenterInfoForm(request.POST,instance=request.user)
	if user_center_info_form.is_valid():
		user_center_info = user_center_info_form.save(commit=True)
	if 'image' in request.FILES:
		im = request.FILES.get('image')
		user = request.user
		# user.avatar.delete(save=True)
		user.avatar = im
		user.save()
		data = {
			'code': 0,
			'msg': u'成功',
		}


		return json_response(data)
	data = {
		'code': 1,
		'msg': u'图片为空',
	}
	return json_response(data)


def change_pass(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password', "")
        password1 = request.POST.get('password1', "")
        password2 = request.POST.get('password2', "")

        user = auth.authenticate(username=request.user.username, password=old_password)
        if user:
            if password1 and password1 == password2:
                user.set_password(password1)
                user.save()
                auth.logout(request)
                return HttpResponseRedirect('/accounts/login/')
            else:
                form = UserChangeForm(instance=request.user)
                return render(request, 'registration/AccountSecurity.html', {'form': form, 'error':'两次输入不一致'})
        else:
            form = UserChangeForm(instance=request.user)
            return render(request, 'registration/AccountSecurity.html', {'form': form, 'error':'原密码错误'})

def again_send_email(request):
    u_email = request.session['u_email']
    evr = EmailVerifyRecord.objects.filter(email=u_email)[0]
    t = threading.Thread(target=send_register_mail, args=(u_email,"register", evr.code))
    t.start()
    #send_register_mail(u_email, code=evr.code)
    return redirect("accounts:registersuccess")

def contactservice(request):
    if request.method=='POST':
        form=CreateContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(u'失败：%s' % form.errors)
    else:
        return render(request,'csinla_posts/Contactus.html')

def privacypolicy(request):
    protocol = Protocol.objects.all()[0]
    context={
        'protocol':protocol,
    }
    return render(request,'csinla_posts/privacypolicy.html',context)

def airport(request):
    protocol = Protocol.objects.all()[0]
    context={
        'protocol':protocol,
    }
    return render(request,'csinla_posts/airport.html',context)

def parking(request):
    context={
    }
    return render(request,'csinla_posts/parking.html',context)

def parking2(request):
    context={
    }
    return render(request,'csinla_posts/parking2.html',context)

def salecar(request):
    context={
    }
    return render(request,'csinla_posts/salecar.html',context)

def carfax(request):
    if request.method=='POST':
        user=request.user
        if not user.is_authenticated():
            data={
                'code':2,
                'msg':u'请先登录',
            }
            return json_response(data)
        form=CreateCarfaxForm(request.POST)
        if form.is_valid():
            carfax=form.save(commit=False)
            carfax.creator=user
            '''
            判断当前用户的微信、邮箱是否为空，为空则将carfax所填微信号设置为其微信号
            邮箱设置为其邮箱账号
            '''
            if user.weixin == '':
                user.weixin = carfax.wechat
            if user.email == '':
                user.email = carfax.email
            user.save()
            carfax.save()
            data={
                'code':0,
                'msg':u'成功',
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':ErrorDic2str(form.errors)
            }
            return json_response(data)
    else:
        context={
        }
        return render(request,'csinla_posts/CarFax.html',context)

def company(request):
    context={
    }
    return render(request,'csinla_posts/Company.html',context)

def newstudent(request):
    context={
    }
    return render(request,'csinla_posts/NewStudent.html',context)

def test_page(request):
    return render(request,'search_new.html')


class ApplyForPickUpView(View):
    def get(self,request):
        sub = NewStudentSubmission.objects.filter(belong=u'jj')
        comments = NewStudentComment.objects.filter(belong=u'jj')
        app_urls = ApplyUrl.objects.all()
        return render(request,'csinla_posts/NewStudent.html',
                      {
                          'comments' :comments,
                          'sub' :sub,
	                      'app_urls':app_urls,
                      }
                      )


class AddApplyPickUpView(View):
    '''
    填写接机申请
    '''
    def post(self,request):
        apply_pickup_form = ApplyPickupForm(request.POST,request.FILES)
        if apply_pickup_form.is_valid():
            apply_pickup =  apply_pickup_form.save(commit=True)
            belong = apply_pickup.belong
            # belong = apply_pickup_form.belong
            from .models import ApplyEmail
            apply_email = ApplyEmail.objects.get(belong=belong)
            email = apply_email.email
            name = apply_pickup.name
            wx=apply_pickup.wx
            phone = apply_pickup.phone
            flight = apply_pickup.flight
            departure = apply_pickup.departure
            landing = apply_pickup.landing
            address = apply_pickup.address
            contactor = apply_pickup.contactor
            contacts_phone = apply_pickup.contacts_phone

            t = threading.Thread(target=send_mail_apply, args=(email,name,wx,phone,flight,departure,landing,address,contactor,contacts_phone))
            t.start()
            return HttpResponse('{"status":"success","msg":"接机申请成功"}',
                                content_type='application/json;charset=utf-8')
        else:
            return HttpResponse('{"status":"fail","msg":"%s"}'%(apply_pickup_form.errors),content_type='application/json;charset=utf-8')


class AddCommentView(View):
    # 新生评论
	def post(self,request):
		comments = request.POST.get('comments','')
		belong = request.POST.get('belong','jj')
		user = request.user
		new_comments = NewStudentComment()
		new_comments.user = user
		new_comments.comments = comments
		new_comments.save()
		msg = u'评论成功'
		# json.dumps(msg,ensure_ascii=False)
		return HttpResponse('{"status":"success","msg":"%s"}'%(msg), content_type='application/json;charset=utf-8')


class AddSubmissionView(View):
    # 新生投稿
	def post(self,request):
		title = request.POST.get('title','')
		content = request.POST.get('content','')
		# img = request.POST.get('img','')
		user = request.user
		url = request.POST.get('url','')
		new_sub = NewStudentSubmission()
		new_sub.title = title
		new_sub.content =content
		new_sub.user = user
		new_sub.url = url
		# new_sub.img = img
		new_sub.save()
		# 上传图片
		if 'image' in request.FILES:
			images = request.FILES.getlist('image')
			for im in images:
				picture = SubmissionPicture(post_id=new_sub.id, image=im)
				picture.save()
		flex_base64_data_list_str = request.POST.get('image')
		if flex_base64_data_list_str:
			for flex_base64_data in flex_base64_data_list_str.split('$$$$$'):
				if flex_base64_data:
					print flex_base64_data
					mediatype, base64_data = flex_base64_data.split(',', 1)
					start_index = mediatype.index('/')
					end_index = mediatype.index(';')
					image_type = mediatype[(start_index + 1):end_index]
					# 存文件
					file_image = base64.b64decode(base64_data)
					fn = time.strftime('%Y%m%d%H%M%S')
					fn_ran = fn + '_%d' % random.randint(0, 100)
					# 重写合成文件名
					file_name = ''.join(fn_ran + '.' + image_type)
					file_image = ContentFile(file_image, file_name)
					picture = SubmissionPicture(post_id=new_sub.id, image=file_image)
					picture.save()
		return HttpResponse('{"status":"success","msg":"投稿成功，待审核"}',
		                    content_type='application/json;charset=utf-8')


class SearcheDriverView(View):
    def post(self,request):
        key = request.POST.get('t_id','')
        dr_exam = DriveExamnation.objects.get(t_id=int(key))
        content = dr_exam.content
        t_id = dr_exam.t_id
        data = {
            'content':content,
            't_id':t_id,
        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')



class EntranceView(View):
    # 新生入学页面
    def get(self,request):
        sub = NewStudentSubmission.objects.filter(belong=u'rx')
        comments = NewStudentComment.objects.filter(belong=u'rx')
        return render(request,'csinla_posts/entrance.html',{
	            'sub':sub,
	            'comments':comments,

        })


class DriveView(View):
    # 新生驾照考试页面
    def get(self,request):
        sub = NewStudentSubmission.objects.filter(belong=u'jz')
        comments = NewStudentComment.objects.filter(belong=u'jz')
        drive_exam = DriveExamnation.objects.all()
        return render(request,'csinla_posts/license.html',{
	        'sub': sub,
	        'comments': comments,
	        'drive_exam':drive_exam,

        })


def activity(request):
    # 新生活动页面
    context = {
	}
    return render(request, 'csinla_posts/activity.html', context)



class UserFeedbackView(View):
    def post(self,request):
        user_feeback_form = UserFeedbackForm(request.POST)
        if user_feeback_form.is_valid():
            user_feeback_form = user_feeback_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json;charset=utf-8')
        else:
            return HttpResponse('{"status":"fail","msg":"输入有误"}',content_type='application/json;charset=utf-8')

