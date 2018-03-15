# coding=utf-8
import datetime
import threading
import json
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import rotate_token
from django.template.response import TemplateResponse
from django.views.generic.base import View
from csinla_accounts.forms import CreateCarfaxForm
# from utils.json_utils import json_response
# from utils.base_utils import ErrorDic2str
from django_jwt_session_auth import jwt_login
from SSO.forms import TicketAuthenticationForm
from csinla_accounts.models import *
from csinla_posts.models import *
from operations.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ExposureListSerializer,Rent2Serializer,RentSerializer,EntireRentSerializer,CarSerializer,UsedBookSerializer,UsedGoodsSerializer
from .serializers import UsedSerializer,WechatInfoSerializer,PostSerializer,PostMessageSerializer
from SSO.models import Ticket,TempTicket
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from .utils import LoginRequiredMixin
import urllib
from .utils import send_mail_apply,WechatUserAuthentication
from csinla_accounts.forms import ApplyPickupForm
from .serializers import NewStudentSubmissionSerializer,NewStudentCommentSerializer,ApplyUrlSerializer
from rest_framework.authentication import BaseAuthentication


class Login(View,WechatUserAuthentication):
    def get(self,request):
        # 小程序授权登陆
        code = request.GET.get('code', '')
        encrypted_data = request.GET.get('encryptedData', '')
        encrypted_data = urllib.unquote(encrypted_data)
        iv = request.GET.get('iv', '')

        api = WXAPPAPI(appid='wx065c265e43cc87ce',
                       app_secret='5cf21a1c7f853b0dcc9fd2895775599f')
        session_info = api.exchange_code_for_session_key(code=code)

        # 获取session_info 后

        session_key = session_info.get('session_key')
        crypt = WXBizDataCrypt('wx065c265e43cc87ce', session_key)

        # encrypted_data 包括敏感数据在内的完整用户信息的加密数据
        # iv 加密算法的初始向量
        # 这两个参数需要js获取
        user_info = crypt.decrypt(encrypted_data, iv)
        try:
            we_chat_info = WechatInfo.objects.get(open_id=user_info['openId'])
            serializer = WechatInfoSerializer(we_chat_info)
            t = Ticket.objects.create_ticket(user=we_chat_info.userinfo)
            token = jwt_login(we_chat_info.userinfo,request)
            context = {
                'status': 'ok',
                'msg': u'成功',
                'data': serializer.data,
                'session_key': session_key,
                'session':t.ticket,
                'token':token
            }
            return HttpResponse(json.dumps(context), content_type='application/json;charset=utf-8')

        except WechatInfo.DoesNotExist:
            try:
                user = Profile.objects.create_user(username='%s' % user_info['openId'], password='wx_CSinLA',
                                                   source='WECHAT')
            except Exception:
                name = user_info['openId']
                name = name + '1'
                user = Profile.objects.create_user(username=name, password='wx_CSinLA', source='WECHAT')
            wechatinfo = WechatInfo()
            wechatinfo.userinfo = user
            wechatinfo.open_id = user_info['openId']
            wechatinfo.nickname = user_info['nickName']
            wechatinfo.sex = user_info['gender']
            wechatinfo.headimgurl = user_info['avatarUrl']
            wechatinfo.province = user_info['province']
            wechatinfo.city = user_info['city']
            wechatinfo.country = user_info['country']
            wechatinfo.save()
            serializer = WechatInfoSerializer(wechatinfo)
            t = Ticket.objects.create_ticket(user=wechatinfo.userinfo)
            token = jwt_login(wechatinfo.userinfo,request)
            context = {
                'status': 'ok',
                'msg': u'成功',
                'data': serializer.data,
                'session_key':session_key,
                '3rd_session':t.ticket,
                'token':token

            }
            return HttpResponse(json.dumps(context), content_type='application/json;charset=utf-8')


class MyFavView(View,LoginRequiredMixin):
    def get(self,request):
        user = request.user
        favorite_list = UserFavorite.objects.filter(user=user)
        favorites = []
        for fav in favorite_list:
            try:
                posts = Post.objects.get(id=fav.fav_id)
            except:
                continue
            favorites.append(posts)
        num = len(favorites)
        posts = Post.objects.all()[0]
        serializer = PostSerializer(posts)
        # serializer = PostSerializer(favorites, many=True)
        context = {
            'status': 0,
            'msg': u'成功',
            'num': num,
            'data': serializer.data,
        }
        return HttpResponse(json.dumps(context), content_type='application/json;charset=utf-8')
class MyPostsView(View):
    def get(self,request):
        ticket = request.GET.get('session','')
        t = Ticket.objects.get(ticket=ticket)
        if not t.user:
            data = {
                'code': 2,
                'msg': u'请先授权',
            }
            return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
        user = Profile.objects.get(username=t.user.username)
        my_posts_list = user.posts.all().order_by('-post_date')
        num = my_posts_list.count()
        # 开始假数据测试
        serializer = PostSerializer(Post.objects.all()[:2],many=True)
        data = {
            'code': 0,
            'msg': u'成功',
            'my_posts': serializer.data,
            'num': num,

        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')

class MyCommentsView(View):
    def get(self,request):
        ticket = request.GET.get('session','')
        t = Ticket.objects.get(ticket=ticket)
        user = t.user
        if not t.user:
            data = {
                'code': 2,
                'msg': u'请先授权',
            }
            return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
        reply_list = PostMessage.objects.filter(is_valid=True, message_type='REPLY', post__author=user,
                                                reply_message__isnull=True) | PostMessage.objects.filter(
            message_type='REPLY', reply_message__in=user.postmessage_set.all())
        reply_list = reply_list.distinct().order_by('has_read', '-create_time')
        collect_list = PostMessage.objects.filter(is_valid=True, message_type='COLLECT', post__author=user).order_by(
            'has_read', '-create_time')
        reply_read = reply_list.filter(has_read=False).exists()
        collect_read = collect_list.filter(has_read=False).exists()
        serializer_reply_list = PostMessageSerializer(PostMessage.objects.all()[:2],many=True)
        serializer_collect_list = PostMessageSerializer(PostMessage.objects.all()[:2],many=True)
        context = {
            'status': 'ok',
            'msg': u'成功',
            'reply_list': serializer_reply_list.data,
            'collect_list': serializer_collect_list.data,
            'reply_read': reply_read,
            'collect_read': collect_read,
        }
        return HttpResponse(json.dumps(context), content_type='application/json;charset=utf-8')

class NewStudentView(View):
    def get(self):
        subs = NewStudentSubmission.objects.filter(belong=u'jj')
        comments = NewStudentComment.objects.filter(belong=u'jj')
        app_urls = ApplyUrl.objects.filter(belong=u'jj')
        serializer_sub = NewStudentSubmissionSerializer(subs,many=True)
        serializer_com = NewStudentCommentSerializer(comments,many=True)
        serializer_app = ApplyUrlSerializer(app_urls,many=True)
        context =       {
                          'comments': serializer_com.data,
                          'sub': serializer_sub.data,
                          'app_urls': serializer_app.data,
                      }

        return HttpResponse(json.dumps(context),content_type='application/json;charset=utf-8')

class ApplyPickUpView(View):
    def post(self,request):
        apply_pickup_form = ApplyPickupForm(request.POST,request.FILES)
        if apply_pickup_form.is_valid():
            apply_pickup =  apply_pickup_form.save(commit=True)
            belong = apply_pickup.belong
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
            context = {
                "status": "ok",
                "msg": u"接机申请成功"

            }
            return HttpResponse(json.dumps(context),content_type='application/json;charset=utf-8')
        else:
            return HttpResponse('{"status":"error","msg":"%s"}'%(apply_pickup_form.errors),content_type='application/json;charset=utf-8')

    pass

class CarFaxView(View):
    def get(self,request):
        ticket = request.GET.get('session','')
        t = Ticket.objects.get(ticket=ticket)
        if not t.user:
            data = {
                'code': 2,
                'msg': u'请先授权',
            }
            return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
        vin = request.GET.get('vin','')
        name = request.GET.get('name','')
        email = request.GET.get('email','')
        wechat = request.GET.get('wechat','')
        carfax = Carfax()
        carfax.vin = vin
        carfax.name = name
        carfax.email = email
        carfax.wechat = wechat
        carfax.creator = t.user
        carfax.save()
        data = {
            'code': 0,
            'msg': u'成功',
        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')

class MyInfo(View):
    def get(self,request):
        ticket = request.GET.get('session','')
        t = Ticket.objects.get(ticket=ticket)
        user = t.user
        username = request.GET.get('name','')
        gender = request.GET.get('gender','')
        student_id = request.GET.get('student_id','')
        school = request.GET.get('school','')
        phone = request.GET.get('phone','')
        email = request.GET.get('email','')
        is_phone = request.POST.get('is_phone', '')
        is_weixin = request.POST.get('is_weixin', '')
        is_name = request.POST.get('is_name', '')
        user.is_phone = [False, True][is_phone == 'True']
        user.is_weixin = [False, True][is_weixin == 'True']
        user.is_name = [False, True][is_name == 'True']
        user.gender = gender
        user.username = username
        user.student_id = student_id
        user.school = school
        user.phone = phone
        user.email= email
        user.save()
        data = {
            'status':'ok',
            'msg':u'保存成功'
        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
def home(request):
    # user_dic=request.user.    to_dict
    data={
        'code':0,
        'msg':u'成功',
        # 'user':user_dic,
    }
    return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
class FeedbackView(View):
    def get(self,request):
        title = request.GET.get('title','')
        content = request.GET.get('content','')
        wx = request.GET.get('wx','')
        feedback = Feedback()
        feedback.title = title
        feedback.content = content
        feedback.phone = wx
        feedback.save()
        return HttpResponse('{"status":"success"}',content_type='application/json;charset=utf-8')

def registerview(request):
    error_str=''
    protocol_content=''
    if Protocol.objects.all().exists():
        protocol_content=Protocol.objects.all()[0].content
    if request.method=='POST':
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
            data={
                'code':0,
                'msg':u'成功'
            }
            return json_response(data)
        else:
            error_str=ErrorDic2str(form.errors)
    data={
        'code':0,
        'msg':u'成功',
        'protocol':protocol_content,
        'error_str':error_str,
    }
    return json_response(data)

def activeuserview(request,active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = Profile.objects.get(email=email)
            user.is_active = True
            user.save()
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)
    else:
        data={
            'code':1,
            'msg':u'无效激活码',
        }
        return json_response(data)

def emailpassword(request):
    if request.method=='POST':
        form = EmailResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = Profile.objects.get(email=email)
            t = threading.Thread(target=send_resetpass_mail, args=(user.username, email,"resetpass"))
            t.start()
            data={
                'code':0,
                'msg':u'成功',
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':u'失败！信息【%s】' % ErrorDic2str(form.errors)
            }
    else:
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)
        

def resetpassword(request,code):
    if request.method=='POST':
        cds=request.POST.dict()
        code=cds.get('code')
        try:
            records = EmailVerifyRecord.objects.get(send_type="resetpass", code=code)
        except:
            data={
                'code':1,
                'msg':u'认证失败',
            }
            return json_response(data)
        user = Profile.objects.get(email=records.email)
        password = cds.get('password', "")
        password1 = cds.get('password1', "")
        if password == password1:
            user.set_password(password)
            user.save()
            data={
                'code':0,
                'msg':u'成功',
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':u'认证失败',
            }
            return json_response(data)


# class UpdateProfile(generic.UpdateView):

#     model = Profile
#     fields = ['user', 'real_name', 'gender']







def myinfo(request):
    user=request.user
    if not user.is_authenticated():
        data={
            'code':2,
            'msg':u'请先登录',
        }
        return json_response(data)
    reply_list=PostMessage.objects.filter(is_valid=True,message_type='REPLY',post__author=user,reply_message__isnull=True)|PostMessage.objects.filter(message_type='REPLY',reply_message__in=user.postmessage_set.all())
    reply_list=reply_list.distinct().order_by('has_read','-create_time')
    collect_list=PostMessage.objects.filter(is_valid=True,message_type='COLLECT',post__author=user).order_by('has_read','-create_time')
    
    reply_read = reply_list.filter(has_read=False).exists()
    collect_read = collect_list.filter(has_read=False).exists()

    reply_count=reply_list.count()
    collect_count=collect_list.count()

    paginator = Paginator(reply_list, 5)

    page = request.GET.get('page')
    try:
        reply_list = paginator.page(page)
    except PageNotAnInteger:
        reply_list = paginator.page(1)
    except EmptyPage:
        reply_list = paginator.page(paginator.num_pages)
    reply_array=[]
    for reply in reply_list:
        reply_array.append(reply.to_dict)
    collect_array=[]
    for collect in collect_list:
        collect_array.append(collect.to_dict)
    data={
        'code':0,
        'msg':u'成功',
        'reply_array': reply_array, 
        'collect_array': collect_array, 
        'reply_read': reply_read, 
        'collect_read': collect_read,
        'reply_count':reply_count,
        'collect_count':collect_count,
    }
    return json_response(data)

#  Handle user feedback
@require_POST
def feedback_func(request):
    body = u'功能失灵反馈:  '
    form = FuncFeedbackFrom(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        cd = form.cleaned_data
        body = body + '  遇见问题的页面: ' + str(cd['page'].encode('utf-8'))
        body = body + '  遇到问题具体时间: ' + str(cd['time'])
        body = body + '  问题描述: ' + str(cd['content'].encode('utf-8'))
        send_feedback_mail(body, "Feedback")
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

@require_POST
def feedback_account(request):
    body = u'账号问题反馈:  '
    form = AccountFeedbackFrom(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        cd = form.cleaned_data
        body = body + '  问题类型选择: ' + str(cd['type'].encode('utf-8'))
        body = body + '  出问题的用户名: ' + str(cd['username'].encode('utf-8'))
        body = body + '  问题描述: ' + str(cd['content'].encode('utf-8'))
        body = body + '  之前进行的操作: ' + str(cd['operating'].encode('utf-8'))
        send_feedback_mail(body, "Feedback")
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


@require_POST
def feedback_exper(request):
    body = u'体验反馈:  '
    form = ExperFeedbackFrom(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        cd = form.cleaned_data
        body = body + u' 反馈表述: ' + str(cd['feedback'].encode('utf-8'))
        send_feedback_mail(body, "Feedback")
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

@require_POST
def feedback_other(request):
    body = u'其他反馈:  '
    form = OtherFeedbackFrom(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        cd = form.cleaned_data
        body = body + u' 问题描述: ' + str(cd['content'].encode('utf-8'))
        send_feedback_mail(body, "Feedback")
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

@require_POST
def accountsecurity(request):
    user=request.user
    if not user.is_authenticated:
        data={
            'code':2,
            'msg':u'请先登录',
        }
        return json_response(data)
    is_phone = request.POST.get('is_phone', '')
    is_weixin = request.POST.get('is_weixin', '')
    is_name = request.POST.get('is_name', '')

    user.is_phone = [False, True][is_phone == 'True']
    user.is_weixin = [False, True][is_weixin == 'True']
    user.is_name = [False, True][is_name == 'True']

    user.save() 
    form = UserChangeForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
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

@require_POST
def user_avatar(request):
    user=request.user
    if not user.is_authenticated:
        data={
            'code':2,
            'msg':u'请先登录',
        }
        return json_response(data)
    if 'image' in request.FILES:
        im = request.FILES.get('image')
        #user.avatar.delete(save=True)
        user.avatar = im
        user.save()
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)
    data={
        'code':1,
        'msg':u'图片为空',
    }
    return json_response(data)

@require_POST
def change_pass(request):
    old_password = request.POST.get('old_password', "")
    password1 = request.POST.get('password1', "")
    password2 = request.POST.get('password2', "")
    if not request.user.is_authenticated:
        data={
            'code':2,
            'msg':u'请先登录',
        }
        return json_response(data)
    user = auth.authenticate(username=request.user.username, password=old_password)
    if user:
        if password1 and password1 == password2:
            user.set_password(password1)
            user.save()
            auth.logout(request)
            data={
                'code':0,
                'msg':u'成功',
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':u'两次密码输入不一致',
            }
            return json_response(data)
        

def again_send_email(request):
    u_email = request.session['u_email']
    evr = EmailVerifyRecord.objects.filter(email=u_email)[0]
    t = threading.Thread(target=send_register_mail, args=(u_email,"register", evr.code))
    t.start()
    data={
        'code':0,
        'msg':u'已成功',
    }
    return json_response(data)

def contactservice(request):
    form=CreateContactInfoForm(request.POST)
    if form.is_valid():
        form.save()
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

def protocol_get(request):
    protocol = Protocol.objects.all()[0]
    data={
        'code':0,
        'msg':u'成功',
        'protocol':protocol.to_dict,
    }
    return json_response(data)


# curricular
def curricular(request):
    curricular_list=Curricular.objects.all()
    
    if request.method=='GET':
        department_array=[]
        subject_array=[]
        year_list=curricular_list.values('year').annotate(count=Count('year')).order_by('year')
        department_list=curricular_list.values('department').annotate(count=Count('department')).order_by('department')
        if request.GET.get('export','')=='true':
            for department_dic in department_list:
                department_str=department_dic['department']
                for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(count=Count('subject')).order_by('subject'):
                    subject_array.append({
                        'department':department_str,
                        'subject':subject_dic['subject'],
                        'subject_number':subject_dic['subject'].split()[-1],
                    })

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=subject.csv'
            import csv
            writer = csv.writer(response)
            for item in subject_array:
                li=[item['department'],item['subject']]
                print li
                writer.writerow(li)
            return response

        for department_dic in department_list:
            department_str=department_dic['department']
            department_array.append(department_str)
            for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(count=Count('subject')).order_by('subject'):
                subject_array.append({
                    'department':''.join(department_str.split()),
                    'subject':subject_dic['subject'],
                    'subject_number':subject_dic['subject'].split()[-1],
                })
        subject_array.sort(key=operator.itemgetter('subject_number'),reverse=False)
        context = {
            'code':0,
            'msg':u'成功',
            'department_array':department_array,
            'subject_array':subject_array,
            'year_list':year_list,
        }
        for i in range(1,6):
            web_belong_to= u'选课C%s' % i
            wap_belong_to= u'选课D%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_C%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_D%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return json_response(context)
    else:
        cds=request.POST.dict()
        if request.user.is_authenticated():
            SearchRecord.objects.create(creator=request.user,search_str=str(cds))

        page =int(cds.pop('page',1))
        if not cds.has_key('department'):
            data={
                'code':1,
                'msg':u'缺少department参数',
            }
            return json_response(data)
        if not cds.has_key('subject'):
            data={
                'code':1,
                'msg':u'缺少subject参数',
            }
            return json_response(data)
        if not cds.has_key('year_start'):
            data={
                'code':1,
                'msg':u'缺少year_start参数',
            }
            return json_response(data)
        if not cds.has_key('year_end'):
            data={
                'code':1,
                'msg':u'缺少year_end参数',
            }
            return json_response(data)
        if not cds.has_key('semester'):
            data={
                'code':1,
                'msg':u'缺少semester参数',
            }
            return json_response(data)
        
        # clase_total_count1=curricular_list1.count(),
        # A_count1=curricular_list1.aggregate(Sum("sign_a"))['sign_a__sum']
        # B_count1=curricular_list1.aggregate(Sum("sign_b"))['sign_b__sum']
        # AB_count1=A_count1+B_count1
        # total_count1=curricular_list1.aggregate(Sum("sign_total"))['sign_total__sum']
        # A_scale1=int(A_count1*100/total_count1)
        # B_scale1=int(B_count1*100/total_count1)
        # AB_scale1=A_scale1+B_scale1

        curricular_list=curricular_list.filter(department=cds['department'],subject=cds['subject'],year__gte=int(cds['year_start']),year__lte=int(cds['year_end']),semester__in=cds['semester'].split())
        instructor_detail_array=[]
        for item in  curricular_list.values('instructor').annotate(count=Count('instructor')).order_by('instructor'):
            instructor=item['instructor']
            instructor_class_count=item['count']
            instructor_curricular_list=curricular_list.filter(instructor=instructor)
            print instructor_curricular_list.aggregate(Sum("sign_a"))
            A_count=instructor_curricular_list.aggregate(Sum("sign_a"))['sign_a__sum']
            B_count=instructor_curricular_list.aggregate(Sum("sign_b"))['sign_b__sum']
            C_count=instructor_curricular_list.aggregate(Sum("sign_c"))['sign_c__sum']
            D_count=instructor_curricular_list.aggregate(Sum("sign_d"))['sign_d__sum']
            F_count=instructor_curricular_list.aggregate(Sum("sign_f"))['sign_f__sum']
            P_count=instructor_curricular_list.aggregate(Sum("sign_p"))['sign_p__sum']
            NP_count=instructor_curricular_list.aggregate(Sum("sign_np"))['sign_np__sum']
            total_count=instructor_curricular_list.aggregate(Sum("sign_total"))['sign_total__sum']

            A_scale=int(A_count*100/total_count)
            B_scale=int(B_count*100/total_count)
            C_scale=int(C_count*100/total_count)
            D_scale=int(D_count*100/total_count)
            F_scale=int(F_count*100/total_count)
            P_scale=int(P_count*100/total_count)
            NP_scale=int(NP_count*100/total_count)
            instructor_curricular_array=[]
            for instructor_curricular in instructor_curricular_list:
                sign_a=instructor_curricular.sign_a
                sign_b=instructor_curricular.sign_b
                sign_c=instructor_curricular.sign_c
                sign_d=instructor_curricular.sign_d
                sign_f=instructor_curricular.sign_f
                sign_p=instructor_curricular.sign_p
                sign_np=instructor_curricular.sign_np
                sign_total=instructor_curricular.sign_total

                sign_a_scale=int(sign_a*100/sign_total)
                sign_b_scale=int(sign_b*100/sign_total)
                sign_c_scale=int(sign_c*100/sign_total)
                sign_d_scale=int(sign_d*100/sign_total)
                sign_f_scale=int(sign_f*100/sign_total)
                sign_p_scale=int(sign_p*100/sign_total)
                sign_np_scale=int(sign_np*100/sign_total)
                instructor_curricular_array.append({
                    'subject':instructor_curricular.subject,
                    'sign_a':sign_a,
                    'sign_b':sign_b,
                    'sign_c':sign_c,
                    'sign_d':sign_d,
                    'sign_f':sign_f,
                    'sign_p':sign_p,
                    'sign_np':sign_np,
                    'sign_total':sign_total,
                    'sign_a_scale':sign_a_scale,
                    'sign_b_scale':sign_b_scale,
                    'sign_c_scale':sign_c_scale,
                    'sign_d_scale':sign_d_scale,
                    'sign_f_scale':sign_f_scale,
                    'sign_p_scale':sign_p_scale,
                    'sign_np_scale':sign_np_scale,
                })
            instructor_curricular_array.sort(key=operator.itemgetter('sign_a_scale'),reverse=True)
            instructor_info={
                'instructor_class_total':instructor_class_count,
                'instructor':instructor,
                'A_count':A_count,
                'B_count':B_count,
                'C_count':C_count,
                'D_count':D_count,
                'F_count':F_count,
                'P_count':P_count,
                'NP_count':NP_count,
                'total_count':total_count,
                'A_scale':A_scale,
                'B_scale':B_scale,
                'C_scale':C_scale,
                'D_scale':D_scale,
                'F_scale':F_scale,
                'P_scale':P_scale,
                'NP_scale':NP_scale,
                'instructor_curricular_array':instructor_curricular_array,
            }
            instructor_detail_array.append(instructor_info)

        instructor_detail_array.sort(key=operator.itemgetter('A_scale'),reverse=True)
        instructor_detail_array_length=len(instructor_detail_array)
        start_index=(page-1)*40
        end_index=page*40
        if instructor_detail_array_length <= start_index:
            data={
                'code':2,
                'msg':u'数据已取完',
            }
            return json_response(data)
        elif instructor_detail_array_length<end_index:
            data={
                'code':0,
                'msg':u'成功',
                'instructor_detail_array':instructor_detail_array[start_index:],
            }
            return json_response(data)
        else:
            data={
                'code':0,
                'msg':u'成功',
                'instructor_detail_array':instructor_detail_array[start_index:end_index],
            }
            return json_response(data)

def subjects_compare(request):
    if request.method=='POST':
        if not request.user.is_authenticated(): 
            data={
                'code':3,
                'msg':u'请先登录',
            }
            return json_response(data)
        cds=request.POST.dict()
        if not cds.has_key('department1'):
            data={
                'code':1,
                'msg':u'缺少第一个department参数',
            }
            return json_response(data)
        if not cds.has_key('department2'):
            data={
                'code':1,
                'msg':u'缺少第二个department参数',
            }
            return json_response(data)
        if not cds.has_key('subject1'):
            data={
                'code':1,
                'msg':u'缺少第一个subject参数',
            }
            return json_response(data)
        if not cds.has_key('subject2'):
            data={
                'code':1,
                'msg':u'缺少第二个subject参数',
            }
            return json_response(data)
        if not cds.has_key('year_start'):
            data={
                'code':1,
                'msg':u'缺少最早年份参数',
            }
            return json_response(data)
        if not cds.has_key('year_end'):
            data={
                'code':1,
                'msg':u'缺少最晚年份参数',
            }
            return json_response(data)
        if not cds.has_key('semester'):
            data={
                'code':1,
                'msg':u'缺少semester参数',
            }
            return json_response(data)
        curricular_list=Curricular.objects.filter(year__gte=int(cds['year_start']),year__lte=int(cds['year_end']),semester_in=cds['semester'].split())
        

        curricular_list1=curricular_list.filter(department=cds['department1'],subject=cds['subject1'])
        clase_total_count1=curricular_list1.count(),
        A_count1=curricular_list1.aggregate(Sum("sign_a"))['sign_a__sum']
        B_count1=curricular_list1.aggregate(Sum("sign_b"))['sign_b__sum']
        AB_count1=A_count1+B_count1
        total_count1=curricular_list1.aggregate(Sum("sign_total"))['sign_total__sum']
        A_scale1=int(A_count1*100/total_count1)
        B_scale1=int(B_count1*100/total_count1)
        AB_scale1=A_scale1+B_scale1

        instructor_detail1_array=[]
        for item in  curricular_list1.values('instructor').annotate(count=Count('instructor')).order_by('instructor'):
            instructor=item['instructor']
            instructor_class_count=item['count']
            instructor_curricular_list=curricular_list1.filter(instructor=instructor)
            print instructor_curricular_list.aggregate(Sum("sign_a"))
            A_count=instructor_curricular_list.aggregate(Sum("sign_a"))['sign_a__sum']
            B_count=instructor_curricular_list.aggregate(Sum("sign_b"))['sign_b__sum']
            C_count=instructor_curricular_list.aggregate(Sum("sign_c"))['sign_c__sum']
            D_count=instructor_curricular_list.aggregate(Sum("sign_d"))['sign_d__sum']
            F_count=instructor_curricular_list.aggregate(Sum("sign_f"))['sign_f__sum']
            P_count=instructor_curricular_list.aggregate(Sum("sign_p"))['sign_p__sum']
            NP_count=instructor_curricular_list.aggregate(Sum("sign_np"))['sign_np__sum']
            total_count=instructor_curricular_list.aggregate(Sum("sign_total"))['sign_total__sum']

            A_scale=int(A_count*100/total_count)
            B_scale=int(B_count*100/total_count)
            C_scale=int(C_count*100/total_count)
            D_scale=int(D_count*100/total_count)
            F_scale=int(F_count*100/total_count)
            P_scale=int(P_count*100/total_count)
            NP_scale=int(NP_count*100/total_count)
            instructor_curricular_array=[]
            for instructor_curricular in instructor_curricular_list:
                sign_a=instructor_curricular.sign_a
                sign_b=instructor_curricular.sign_b
                sign_c=instructor_curricular.sign_c
                sign_d=instructor_curricular.sign_d
                sign_f=instructor_curricular.sign_f
                sign_p=instructor_curricular.sign_p
                sign_np=instructor_curricular.sign_np
                sign_total=instructor_curricular.sign_total

                sign_a_scale=int(sign_a*100/sign_total)
                sign_b_scale=int(sign_b*100/sign_total)
                sign_c_scale=int(sign_c*100/sign_total)
                sign_d_scale=int(sign_d*100/sign_total)
                sign_f_scale=int(sign_f*100/sign_total)
                sign_p_scale=int(sign_p*100/sign_total)
                sign_np_scale=int(sign_np*100/sign_total)
                instructor_curricular_array.append({ 
                    'subject':instructor_curricular.subject,    
                    'sign_a':sign_a,
                    'sign_b':sign_b,
                    'sign_c':sign_c,
                    'sign_d':sign_d,
                    'sign_f':sign_f,
                    'sign_p':sign_p,
                    'sign_np':sign_np,
                    'sign_total':sign_total,
                    'sign_a_scale':sign_a_scale,
                    'sign_b_scale':sign_b_scale,
                    'sign_c_scale':sign_c_scale,
                    'sign_d_scale':sign_d_scale,
                    'sign_f_scale':sign_f_scale,
                    'sign_p_scale':sign_p_scale,
                    'sign_np_scale':sign_np_scale,
                })
            instructor_curricular_array.sort(key=operator.itemgetter('sign_a_scale'),reverse=True)
            instructor_info={
                'instructor_class_total':instructor_class_count,
                'instructor':instructor,
                'A_count':A_count,
                'B_count':B_count,
                'C_count':C_count,
                'D_count':D_count,
                'F_count':F_count,
                'P_count':P_count,
                'NP_count':NP_count,
                'total_count':total_count,
                'A_scale':A_scale,
                'B_scale':B_scale,
                'C_scale':C_scale,
                'D_scale':D_scale,
                'F_scale':F_scale,
                'P_scale':P_scale,
                'NP_scale':NP_scale,
                'instructor_curricular_array':instructor_curricular_array,
            }
            instructor_detail1_array.append(instructor_info)

        subject1_info={
            'class_total_count':clase_total_count1,
            'A_count':A_count1,
            'B_count':B_count1,
            'AB_count':AB_count1,
            'total_count':total_count1,
            'A_scale':A_scale1,
            'B_scale':B_scale1,
            'AB_scale':AB_scale1,
            'instructor_detail_array':instructor_detail1_array,
        }
        curricular_list2=curricular_list.filter(department=cds['department2'],subject=cds['subject2'])
        clase_total_count2=curricular_list2.count(),
        A_count2=curricular_list2.aggregate(Sum("sign_a"))['sign_a__sum']
        B_count2=curricular_list2.aggregate(Sum("sign_b"))['sign_b__sum']
        AB_count2=A_count2+B_count2
        total_count2=curricular_list2.aggregate(Sum("sign_total"))['sign_total__sum']
        A_scale2=int(A_count2*100/total_count2)
        B_scale2=int(B_count2*100/total_count2)
        AB_scale2=A_scale2+B_scale2

        instructor_detail2_array=[]
        for item in  curricular_list2.values('instructor').annotate(count=Count('instructor')).order_by('instructor'):
            instructor=item['instructor']
            instructor_class_count=item['count']
            instructor_curricular_list=curricular_list1.filter(instructor=instructor)
            print instructor_curricular_list.aggregate(Sum("sign_a"))
            A_count=instructor_curricular_list.aggregate(Sum("sign_a"))['sign_a__sum']
            B_count=instructor_curricular_list.aggregate(Sum("sign_b"))['sign_b__sum']
            C_count=instructor_curricular_list.aggregate(Sum("sign_c"))['sign_c__sum']
            D_count=instructor_curricular_list.aggregate(Sum("sign_d"))['sign_d__sum']
            F_count=instructor_curricular_list.aggregate(Sum("sign_f"))['sign_f__sum']
            P_count=instructor_curricular_list.aggregate(Sum("sign_p"))['sign_p__sum']
            NP_count=instructor_curricular_list.aggregate(Sum("sign_np"))['sign_np__sum']
            total_count=instructor_curricular_list.aggregate(Sum("sign_total"))['sign_total__sum']

            A_scale=int(A_count*100/total_count)
            B_scale=int(B_count*100/total_count)
            C_scale=int(C_count*100/total_count)
            D_scale=int(D_count*100/total_count)
            F_scale=int(F_count*100/total_count)
            P_scale=int(P_count*100/total_count)
            NP_scale=int(NP_count*100/total_count)
            instructor_curricular_array=[]
            for instructor_curricular in instructor_curricular_list:
                sign_a=instructor_curricular.sign_a
                sign_b=instructor_curricular.sign_b
                sign_c=instructor_curricular.sign_c
                sign_d=instructor_curricular.sign_d
                sign_f=instructor_curricular.sign_f
                sign_p=instructor_curricular.sign_p
                sign_np=instructor_curricular.sign_np
                sign_total=instructor_curricular.sign_total

                sign_a_scale=int(sign_a*100/sign_total)
                sign_b_scale=int(sign_b*100/sign_total)
                sign_c_scale=int(sign_c*100/sign_total)
                sign_d_scale=int(sign_d*100/sign_total)
                sign_f_scale=int(sign_f*100/sign_total)
                sign_p_scale=int(sign_p*100/sign_total)
                sign_np_scale=int(sign_np*100/sign_total)
                instructor_curricular_array.append({
                    'subject':instructor_curricular.subject,
                    'sign_a':sign_a,
                    'sign_b':sign_b,
                    'sign_c':sign_c,
                    'sign_d':sign_d,
                    'sign_f':sign_f,
                    'sign_p':sign_p,
                    'sign_np':sign_np,
                    'sign_total':sign_total,
                    'sign_a_scale':sign_a_scale,
                    'sign_b_scale':sign_b_scale,
                    'sign_c_scale':sign_c_scale,
                    'sign_d_scale':sign_d_scale,
                    'sign_f_scale':sign_f_scale,
                    'sign_p_scale':sign_p_scale,
                    'sign_np_scale':sign_np_scale,
                })
            instructor_curricular_array.sort(key=operator.itemgetter('sign_a_scale'),reverse=True)
            instructor_info={
                'instructor_class_total':instructor_class_count,
                'instructor':instructor,
                'A_count':A_count,
                'B_count':B_count,
                'C_count':C_count,
                'D_count':D_count,
                'F_count':F_count,
                'P_count':P_count,
                'NP_count':NP_count,
                'total_count':total_count,
                'A_scale':A_scale,
                'B_scale':B_scale,
                'C_scale':C_scale,
                'D_scale':D_scale,
                'F_scale':F_scale,
                'P_scale':P_scale,
                'NP_scale':NP_scale,
                'instructor_curricular_array':instructor_curricular_array,
            }
            instructor_detail2_array.append(instructor_info)


        subject2_info={
            'class_total_count':clase_total_count2,
            'A_count':A_count2,
            'B_count':B_count2,
            'AB_count':AB_count2,
            'total_count':total_count2,
            'A_scale':A_scale2,
            'B_scale':B_scale2,
            'AB_scale':AB_scale2,
            'instructor_detail_array':instructor_detail2_array,
        }
        data={
            'code':0,
            'msg':u'成功',
            'subject1_info':subject1_info,
            'subject2_info':subject2_info,
        }
        return json_response(data)
    else:
        curricular_list=Curricular.objects.all()
        department_array=[]
        subject_array=[]
        department_list=curricular_list.values('department').annotate(count=Count('department')).order_by('department')
        for department_dic in department_list:
            department_str=department_dic['department']
            department_array.append(department_str)
            subject_item_list=[]
            for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(count=Count('subject')).order_by('subject'):
                subject_array.append({
                    'department':department_str,
                    'subject':subject_dic['subject'],
                })
        context = {
            'code':0,
            'msg':u'成功',
            'department_array':department_array,
            'subject_array':subject_array,
        }
        return json_response(context)

# posts
def search(request):
    key = request.GET.get('keyword')
    posts = None
    try:
        posts = Car.objects.get(car_id=key)
    except:
        try:
            posts = Rent.objects.get(house_id=key)
        except:
            try:
                posts = Car.objects.get(vin_number=key)
            except:
                try:
                    posts = UsedGoods.objects.get(used_id=key)
                except:
                    try:
                        posts = UsedBook.objects.get(book_id=key)
                    except:
                        pass
    if posts:
        data={
            'code':0,
            'msg':u'成功',
            'post':posts.to_dict,
        }
        return json_response(data)
    else:
        data={
            'code':1,
            'msg':u'无符合条件的结果'
        }
        return json_response(data)

def listrent(request):
    if request.method=='POST':
        rents = Rent.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top','-active')
        locat = request.POST.get('locat')
        type = request.POST.get('type')
        price = request.POST.get('price')

        if type == None or locat == None or price == None:
            rents = Rent.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top','-active')
        if type != u'全部' and type != None:
            rents = rents.filter(share = type).order_by('-active')
        if locat != u'全部' and locat != None:
            rents = rents.filter( district = locat).order_by('-active')
        if price != u'全部' and price != None and price != 'other':
            if price == 'other':
                rents = rents.filter(fee__gte = 1500).order_by('-active')
            else:
                price_up = int(price) - int(500)
                rents = rents.filter( fee__lte = price , fee__gte = price_up).order_by('-active')
        serializer = RentSerializer(rents,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'rent_array':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        rents = Rent.objects.filter(expire_date__gte = timezone.now())
        cds=request.GET.dict()
        locat = cds.get('locat','')
        # type = cds.get('type','')
        price = cds.get('price',0)
        if not price:
            price=0

        if  locat == '' and price == 0:
            rents = Rent.objects.filter(expire_date__gte = timezone.now())
        else:
            if locat != u'全部' and locat !='':
                rents = rents.filter( district = locat)
            if price != u'全部' and price != '':
                if price == 'other':
                    rents = rents.filter(fee__gte = 1500)
                else:
                    price_up = int(price) - int(500)
                    rents = rents.filter( fee__lte = price , fee__gte = price_up)
        rents=rents.order_by('-is_top','-active')

        # paginator = Paginator(rents,15)
        # try:
        #     rents_p = paginator.page(page)
        # except PageNotAnInteger:
        #     rents_p = paginator.page(1)
        # except EmptyPage:
        #     rents_p = paginator.page(paginator.num_pages)
        serializer = RentSerializer(rents[:15],many=True)
        context={
            'code':0,
            'msg':u'成功',
            'rent_array':serializer.data,
        }
        for i in range(1,8):
            web_belong_to=u'租房A%s' % i
            wap_belong_to=u'租房B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')

def second_hand(request):
    useds = Used.objects.all()
    cds = request.POST.dict()
    locat = cds.get('locat', '')
    tag = cds.get('type', '')
    if locat != '全部' and tag != '' :
        useds = useds.filter(district=locat)
    if tag != '全部' and tag != '':
        useds = useds.filter(tags__tag=tag)
    serializer = UsedSerializer(useds[:15],many=True)
    context ={
        'code':0,
        'msg':u'成功',
        'data':serializer.data,
    }
    return  HttpResponse(json.dumps(context),content_type='application/json;charset=utf-8')

def listerent(request):
    if request.method=='POST':
        rents = EntireRent.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top','-active')
        locat = request.POST.get('locat')
        type = request.POST.get('type')
        price = request.POST.get('price')

        if type == None or locat == None or price == None:
            rents = EntireRent.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top','-active')
        if type != u'全部' and type != None:
            rents = rents.filter(share = type).order_by('-active')
        if locat != u'全部' and locat != None:
            rents = rents.filter( district = locat).order_by('-active')
        if price != u'全部' and price != None and price != 'other':
            if price == 'other':
                rents = rents.filter(fee__gte = 1500).order_by('-active')
            else:
                price_up = int(price) - int(500)
                rents = rents.filter( fee__lte = price , fee__gte = price_up).order_by('-active')
        serializer = EntireRentSerializer(rents,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'erent_array':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        rents = EntireRent.objects.filter(expire_date__gte = timezone.now())
        cds=request.GET.dict()
        # page=int(cds.pop('page',1))
        locat = cds.get('locat','')
        # type = cds.get('type','')
        price = cds.get('price',0)
        if not price:
            price=0

        if locat == '' and price == 0:
            rents = EntireRent.objects.filter(expire_date__gte = timezone.now())
        else:
            if locat != u'全部'  and locat != '':
                rents = rents.filter( district = locat)
            if price != u'全部'  and price !='':
                if price == 'other':
                    rents = rents.filter(fee__gte = 1500)
                else:
                    price_up = int(price) - int(500)
                    rents = rents.filter( fee__lte = price , fee__gte = price_up)
        rents=rents.order_by('-is_top','-active')

        serializer = EntireRentSerializer(rents[:15],many=True)
        context={
            'code':0,
            'msg':u'成功',
            'erent_array':serializer.data,
        }
        for i in range(1,8):
            web_belong_to=u'整租A%s' % i
            wap_belong_to=u'整租B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')

def roommate(request):
    rents = Rent2.objects.filter(expire_date__gte = timezone.now()).order_by('-post_date')
    locat = request.GET.get('locat')
    type = request.GET.get('type')
    price = request.GET.get('price')

    if type == None or locat == None or price == None:
        rents = Rent2.objects.filter(expire_date__gte = timezone.now()).order_by('-post_date')
    elif type == 'alltype' and locat == 'allloc' and price == 'allprice':
        rents = Rent2.objects.all().order_by('-post_date')
    elif type == 'alltype' and locat == 'allloc':
        price_up = int(price) - int(500)
        rents = Rent2.objects.filter( fee__lte = price , fee__gte = price_up)
    elif type == 'alltype' and price == 'allprice':
        rents = Rent2.objects.filter( district = locat)
    elif locat == 'allloc' and price == 'allprice':
        rents = Rent2.objects.filter(share = type)
    elif type == 'alltype':
        price_up = int(price) - int(500)
        rents = Rent2.objects.filter( district = locat , fee__lte = price , fee__gte = price_up)
    elif locat == 'allloc':
        price_up = int(price) - int(500)
        rents = Rent2.objects.filter( share = type , fee__lte = price , fee__gte = price_up)
    elif price == 'allprice':
        rents = Rent2.objects.filter(share = type , district = locat )   
    else:
        price_up = int(price) - int(500)
        rents = Rent2.objects.filter(share = type , district = locat , fee__lte = price , fee__gte = price_up)

    # paginator = Paginator(rents, 15)
    # page = request.GET.get('page')
    # try:
    #     rents_p = paginator.page(page)
    # except PageNotAnInteger:
    #     rents_p = paginator.page(1)
    # except EmptyPage:
    #     rents_p = paginator.page(paginator.num_pages)
    # rent_array=[]
    # for rent in rents_p:
    #     rent_array.append(rent.to_dict)
    serializer = Rent2Serializer(rents,many=True)
    context={
        'code':0,
        'msg':u'成功',
        'rent_array':serializer.data,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


def listcar(request):
    if request.method=='POST':
        cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('is_top', '-active')
        level = request.POST.get('level', None)
        type = request.POST.get('type', None)
        transmission = request.POST.get('transmission', None)
        price = request.POST.get('price', None)

        if type == None or level == None or transmission == None:
            cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('is_top', '-active')
        if type != u'全部' and type != None:
            cars = cars.filter(car_type = type).order_by('-active')
        if level != u'全部' and level != None:
            cars = cars.filter( level_type = level).order_by('-active')
        if transmission != u'全部' and transmission != None:
            cars = cars.filter(transmission_type = transmission).order_by('-active')
        if price != u'全部' and price != None and price != 'other':
            if int(price) == 10000:
                cars = cars.filter(fee__lte = 10000).order_by('-active')
            else:
                price_up = int(price) - int(5000)
                cars = cars.filter(fee__lte = price , fee__gte = price_up).order_by('-active')
        if price == 'other':
            cars = cars.filter(fee__gte = 40000).order_by('-active')

        serializer = CarSerializer(cars,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'car_array':serializer.data,
            # 'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'汽车A%s' % i
            wap_belong_to=u'汽车B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('is_top', '-active')
        cds=request.GET.dict()
        # page=int(cds.pop('page',1))
        level = cds.get('level','')
        type = cds.get('type','')
        # transmission = cds.get('transmission','')
        if type == '' and level == '' :
            cars = Car.objects.filter(expire_date__gte = timezone.now())
        else:
            if type != u'全部' and type !='':
                cars = cars.filter(car_type = type)
            if level != u'全部' and type !='':
                cars = cars.filter( level_type = level)
            # if transmission != u'全部' and type !='':
            #     cars = cars.filter(transmission_type = transmission)
            # if price != u'全部' and price != None and price != 'other':
            #     if int(price) == 10000:
            #         cars = cars.filter(fee__lte = 10000).order_by('-active')
            #     else:
            #         price_up = int(price) - int(5000)
            #         cars = cars.filter(fee__lte = price , fee__gte = price_up).order_by('-active')
            # if price == 'other':
            #     cars = cars.filter(fee__gte = 40000).order_by('-active')
        cars=cars.order_by('-is_top','-active')
        # paginator = Paginator(cars,16)
        # try:
        #     cars_p = paginator.page(page)
        # except PageNotAnInteger:
        #     cars_p = paginator.page(1)
        # except EmptyPage:
        #     cars_p = paginator.page(paginator.num_pages)
        serializer = CarSerializer(cars[:15],many=True)
        context={
            'code':0,
            'msg':u'成功',
            'car_array':serializer.data,
            'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'汽车A%s' % i
            wap_belong_to=u'汽车B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')

def listusedgoods(request):
    if request.method=='POST':  
        usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        cds=request.POST.dict()
        locat=cds.get('locat',None)
        level = cds.get('level', None)
        type = cds.get('type', None)
        transmission = cds.get('transmission', None)
        price = cds.get('price', None)

        if type == None or locat == None or level == None or transmission == None:
            usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        if locat != u'全部' and locat != None and locat!='OTHER':
            usedgoods_list = usedgoods_list.filter(district = locat)
        if locat == 'OTHER':
            usedgoods_list = usedgoods_list.exclude(district__in = ['USC','SMC UCLA','UCSB','UCSD','UCI','ELAC','PCC'])
        if type != u'全部' and type != None:
            usedgoods_list = usedgoods_list.filter(car_type = type)
        if level != u'全部' and level != None:
            usedgoods_list = usedgoods_list.filter( level_type = level)
        if transmission != u'全部' and transmission != None:
            usedgoods_list = usedgoods_list.filter(transmission_type = transmission)
        if price != u'全部' and price != None and price != 'other':
            if int(price) == 10000:
                usedgoods_list = usedgoods_list.filter(fee__lte = 10000)
            else:
                price_up = int(price) - int(5000)
                usedgoods_list = usedgoods_list.filter(fee__lte = price , fee__gte = price_up)
        if price == 'other':
            usedgoods_list = usedgoods_list.filter(fee__gte = 40000)
        usedgoods_list=usedgoods_list.order_by('-is_top','-last_change_time')
        # paginator = Paginator(usedgoods_list,15)
        # page = cds.pop('page',1)
        # try:
        #     usedgoods_p = paginator.page(page)
        # except PageNotAnInteger:
        #     usedgoods_p = paginator.page(1)
        # except EmptyPage:
        #     usedgoods_p = paginator.page(paginator.num_pages)
        # usedgoods_arry=[]
        # for usedgoods in usedgoods_p:
        #     usedgoods_arry.append(usedgoods.to_dict)
        serializer = UsedGoodsSerializer(usedgoods_list,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'usedgoods_arry':serializer.data,
            # 'filter_dic':filter_dic,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        cds=request.GET.dict()
        locat=cds.get('locat','')
        level = cds.get('level', None)
        type = cds.get('type', None)
        transmission = cds.get('transmission', None)
        price = cds.get('price', None)

        if type == None or locat == '' or level == None or transmission == None:
            usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        if locat != u'全部' and locat != '' and locat!='OTHER':
            usedgoods_list = usedgoods_list.filter(district = locat)
        if locat == 'OTHER':
            usedgoods_list = usedgoods_list.exclude(district__in = ['USC','SMC UCLA','UCSB','UCSD','UCI','ELAC','PCC'])
        if type != u'全部' and type != None:
            usedgoods_list = usedgoods_list.filter(car_type = type)
        if level != u'全部' and level != None:
            usedgoods_list = usedgoods_list.filter( level_type = level)
        if transmission != u'全部' and transmission != None:
            usedgoods_list = usedgoods_list.filter(transmission_type = transmission)
        if price != u'全部' and price != None and price != 'other':
            if int(price) == 10000:
                usedgoods_list = usedgoods_list.filter(fee__lte = 10000)
            else:
                price_up = int(price) - int(5000)
                usedgoods_list = usedgoods_list.filter(fee__lte = price , fee__gte = price_up)
        if price == 'other':
            usedgoods_list = usedgoods_list.filter(fee__gte = 40000)
        usedgoods_list=usedgoods_list.order_by('-is_top','-last_change_time')
        # paginator = Paginator(usedgoods_list,16)
        # page = request.GET.get('page')
        # try:
        #     usedgoods_p = paginator.page(page)
        # except PageNotAnInteger:
        #     usedgoods_p = paginator.page(1)
        # except EmptyPage:
        #     usedgoods_p = paginator.page(paginator.num_pages)
        # usedgoods_arry=[]
        # for usedgoods in usedgoods_p:
        #     usedgoods_arry.append(usedgoods.to_dict)
        serializer = UsedGoodsSerializer(usedgoods_list,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'usedgoods_arry': serializer.data,
        }
        for i in range(1,8):
            web_belong_to=u'二手商品A%s' % i
            wap_belong_to=u'二手商品B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')

@csrf_exempt
def usedgoods_add(request):
    tag_list=UsedGoodsTag.objects.all()
    if request.method=='POST':
        form = UsedGoodsForm(request.POST)
        cds=request.POST.dict()
        print cds
        goods_detail_str=request.POST.get('goods_detail_str','')
        # print goods_detail_str
        if form.is_valid():
            usedgoods = form.save(commit=False)
            usedgoods.author=request.user
            usedgoods.expire_time=datetime.datetime.now()+datetime.timedelta(days=30)
            usedgoods.post_date=datetime.datetime.now()
            usedgoods.active=datetime.datetime.now()
            usedgoods.belong_to=u'二手商品'
            usedgoodsitem_array=[]
            for goods_str in goods_detail_str.split('~#~'):
                if goods_str:
                    item_array=goods_str.split('~*~')[:2]
                    if not set(['','undefined'])&set(item_array):
                        item_name=item_array[0]
                        item_price=item_array[1]
                        if item_price.isdigit():
                            usedgoodsitem=UsedGoodsItem(usedgoods=usedgoods,name=item_name,price=int(item_price))
                            usedgoodsitem_array.append(usedgoodsitem)
                        else:
                            data={
                                'code':1,
                                'msg':u'商品【%s】的价格格式不合法' % item_name,
                            }
                            return json_response(data)
                usedgoods.save()
                form.save_m2m()
                if usedgoodsitem_array:
                    for usedgoodsitem in usedgoodsitem_array:
                        usedgoodsitem.usedgoods=usedgoods
                        usedgoodsitem.save()
                if 'image' in request.FILES:
                    images = request.FILES.getlist('image')
                    for im in images:
                        picture = Rentpicture(post_id=usedgoods.id, image=im)
                        picture.save()
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return json_response(data)
    else:
        tag_array=[]
        for tag in tag_list:
            tag_array.append(tag.to_dict)
        data={
            'code':0,
            'msg':u'成功',
            'tag_array':tag_array,
        }
        return json_response(data)

def listusedbook(request):
    if request.method=='GET':
        usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        cds=request.POST.dict()
        locat = cds.get('locat', None)
        level = cds.get('level', None)
        type = cds.get('type', None)
        transmission = cds.get('transmission', None)
        price = cds.get('price', None)

        if type == None or locat == None or level == None or transmission == None:
            usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        if locat != u'全部' and locat != None and locat!='OTHER':
            usedbook_list = usedbook_list.filter(district__in = locat.split())
        if locat == 'OTHER':
            usedbook_list = usedbook_list.exclude(district__in = ['USC','SMC','UCLA','UCSB','UCSD','UCI','ELAC','PCC'])
        if type != u'全部' and type != None:
            usedbook_list = usedbook_list.filter(car_type = type)
        if level != u'全部' and level != None:
            usedbook_list = usedbook_list.filter( level_type = level)
        if transmission != u'全部' and transmission != None:
            usedbook_list = usedbook_list.filter(transmission_type = transmission)
        if price != u'全部' and price != None and price != 'other':
            if int(price) == 10000:
                usedbook_list = usedbook_list.filter(fee__lte = 10000)
            else:
                price_up = int(price) - int(5000)
                usedbook_list = usedbook_list.filter(fee__lte = price , fee__gte = price_up)
        if price == 'other':
            usedbook_list = usedbook_list.filter(fee__gte = 40000)
        usedbook_list=usedbook_list.order_by('-is_top','-last_change_time')
        # paginator = Paginator(usedbook_list,16)
        # page = request.GET.get('page')
        # try:
        #     usedbook_p = paginator.page(page)
        # except PageNotAnInteger:
        #     usedbook_p = paginator.page(1)
        # except EmptyPage:
        #     usedbook_p = paginator.page(paginator.num_pages)
        # usedbook_array=[]
        # for usedbook in usedbook_p:
        #     usedbook_array.append(usedbook.to_dict)
        serializer = UsedBookSerializer(usedbook_list,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'usedbook_array': serializer.data,
        }
        for i in range(1,8):
            web_belong_to=u'二手书A%s' % i
            wap_belong_to=u'二手书B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0].to_dict
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0].to_dict
                })
        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        cds=request.POST.dict()
        locat = cds.get('locat', None)
        level = cds.get('level', None)
        type = cds.get('type', None)
        transmission = cds.get('transmission', None)
        price = cds.get('price', None)

        if type == None or locat == None or level == None or transmission == None:
            usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        if locat != u'全部' and locat != None and locat!='OTHER':
            usedbook_list = usedbook_list.filter(district__in = locat.split())
        if locat == 'OTHER':
            usedbook_list = usedbook_list.exclude(district__in = ['USC','SMC','UCLA','UCSB','UCSD','UCI','ELAC','PCC'])
        if type != u'全部' and type != None:
            usedbook_list = usedbook_list.filter(car_type = type)
        if level != u'全部' and level != None:
            usedbook_list = usedbook_list.filter( level_type = level)
        if transmission != u'全部' and transmission != None:
            usedbook_list = usedbook_list.filter(transmission_type = transmission)
        if price != u'全部' and price != None and price != 'other':
            if int(price) == 10000:
                usedbook_list = usedbook_list.filter(fee__lte = 10000)
            else:
                price_up = int(price) - int(5000)
                usedbook_list = usedbook_list.filter(fee__lte = price , fee__gte = price_up)
        if price == 'other':
            usedbook_list = usedbook_list.filter(fee__gte = 40000)
        usedbook_list=usedbook_list.order_by('-is_top','-last_change_time')
        # paginator = Paginator(usedbook_list,15)
        # page = cds.pop('page',1)
        # try:
        #     usedbook_p = paginator.page(page)
        # except PageNotAnInteger:
        #     usedbook_p = paginator.page(1)
        # except EmptyPage:
        #     usedbook_p = paginator.page(paginator.num_pages)
        # usedbook_array=[]
        # for usedbook in usedbook_p:
        #     usedbook_array.append(usedbook.to_dict)
        serializer = UsedBookSerializer(usedbook_list,many=True)
        context={
            'code':0,
            'msg':u'成功',
            'usedbook_array':serializer.data,
            'filter_dic':cds,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')

def usedbook_add(request):
    errors=[]
    if request.method=='POST':
        form = UsedBookForm(request.POST)
        print request.POST.dict()
        book_detail_str=request.POST.get('book_detail_str','')
        if form.is_valid():
            usedbook = form.save(commit=False)
            usedbook.author=request.user
            usedbook.expire_time=datetime.datetime.now()+datetime.timedelta(days=30)
            usedbook.post_date=datetime.datetime.now()
            usedbook.active=datetime.datetime.now()
            usedbook.belong_to=u'二手书'
            usedbookitem_array=[]
            for book_str in book_detail_str.split('~#~'):
                # print book_str
                if book_str:
                    item_array=book_str.split('~*~')[:4]
                    if not set(['','undefined'])&set([item_array[0],item_array[1],item_array[3]]):
                        item_name=item_array[0]
                        item_price=item_array[1]
                        item_isbn=item_array[2]
                        if item_price.isdigit():
                            usedbookitem=UsedBookItem(name=item_name,price=int(item_price),isbn=item_isbn)
                            usedbookitem_array.append(usedbookitem)
                        else:
                            data={
                                'code':1,
                                'msg':u'二手书【%s】价格格式有误' % item_name,
                            }
                            return json_response(data)
            usedbook.save()
            for usedbookitem in usedbookitem_array:
                usedbookitem.usedbook=usedbook
                usedbookitem.save()
                print usedbookitem
            if 'image' in request.FILES:
                images = request.FILES.getlist('image')
                for im in images:
                    picture = Rentpicture(post_id=usedbook.id, image=im)
                    picture.save()
            data={
                'code':0,
                'msg':u'成功',
                'id':usedbook.id,
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':ErrorDic2str(form.errors),
            }
            return json_response(data)

@api_view(['GET'])
def listexposure(request):
    if request.method=='GET':
        # exposure_list = Exposure.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
        exposures = Exposure.objects.all().order_by('-is_top','-active')
        serializer = ExposureListSerializer(exposures,many=True)
        data = {
            'code': 0,
            'msg': u'成功',
            'exposure_array': serializer.data,
        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
    else:
        exposures = Exposure.objects.all().order_by('-is_top','-active')
        serializer = ExposureListSerializer(exposures[:15],many=True)
        data = {
            'code': 0,
            'msg': u'成功',
            'exposure_array': serializer.data,
        }
        return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')
    
def exposure_add(request):
    if request.method=='POST':
        form = CreateExposureForm(request.POST)
        if form.is_valid():
            exposure=form.save(commit=False)
            exposure.author=request.user
            exposure.expire_time=datetime.datetime.now()+datetime.timedelta(days=30)
            exposure.post_date=datetime.datetime.now()
            exposure.active=datetime.datetime.now()
            exposure.belong_to=u'朋友圈'
            exposure.save()
            tag_str=request.POST.get('tag_str','')
            if tag_str:
                tag_id_array=[int(tag_id) for tag_id in tag_str.split(':')]
                for tag in ExposureTag.objects.filter(id__in=tag_id_array):
                    exposure.tags.add(tag)
            if 'image' in request.FILES:
                images = request.FILES.getlist('image')
                for im in images:
                    picture = Rentpicture(post_id=exposure.id, image=im)
                    picture.save()
            data={
                'code':0,
                'msg':u'成功',
                'id':exposure.id,
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':ErrorDic2str(form.errors),
            }
            return json_response(data)

def view_posts(request, posts_id):
    posts = Post.objects.get(id=posts_id)
    view_message=request.GET.get('view_message','')
    if view_message:
        view_message=int(view_message)
        message=posts.postmessage_set.get(id=view_message)
        if not message.has_read:
            message.has_read=True
            message.save()
        data={
            'code':0,
            'msg':u'成功',
            'post_id':posts.id,
        }
        return json_response(data)
    collect_message=request.GET.get('collect_message','')
    if collect_message:
        collect_message=int(collect_message)
        message=posts.postmessage_set.get(id=collect_message,message_type='COLLECT')
        if not message.has_read:
            message.has_read=True
            message.save()
    picture = Rentpicture.objects.filter(post__id=posts_id)
    is_favor = UserFavorite.objects.filter(user__id=request.user.id, fav_id=posts.id).exists()
    reply_message_list=posts.postmessage_set.filter(message_type='REPLY',reply_message__isnull=True).order_by('create_time')
    reply_message_array=[]
    for reply_message in reply_message_list:
        reply_message_array.append(reply_message.to_dict)
    is_collect=False
    try:
        PostMessage.objects.get(message_type='COLLECT',post=posts,creator=request.user,is_valid=True)
        is_collect=True
    except:
        pass
    if picture.exists():
            picurl = 'http://www.csinla.com' + picture[0].image.url
    else:
            picurl = 'http://www.csinla.com/media/wxlogo.jpg'
    if posts.belong_to == u"个人转租":
        try:
            war = Warnings.objects.get(posts_type=u"个人转租")
            war = war.content
        except:
            war = u"未设置"
        serializer = RentSerializer(posts.rent)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"二手车":
        try:
            war = Warnings.objects.get(posts_type=u"二手车")
            war = war.content
        except:
            war = ""
        serializer = CarSerializer(posts.rent2)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"合租":
        try:
            war = Warnings.objects.get(posts_type=u"合租")
            war = war.content
        except:
            war = u"未设置"
        serializer = Rent2Serializer(posts.rent2)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"二手商品":
        try:
            war = Warnings.objects.get(posts_type=u"二手商品")
            war = war.content
        except:
            war = u"未设置"
        serializer = UsedGoodsSerializer(posts.usedgood)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"二手书":
        try:
            war = Warnings.objects.get(posts_type=u"二手书")
            war = war.content
        except:
            war = u"未设置"
        serializer = UsedBookSerializer(posts.usedbook)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"朋友圈":
        try:
            war = Warnings.objects.get(posts_type=u"朋友圈")
            war = war.content
        except:
            war = u"未设置"
        # post = Post.objects.get(id=posts_id)
        # serializer = ExposureListSerializer(post)
        # return Response(serializer.data)
        serializer = ExposureListSerializer(posts.exposure)
        # exposure = serializers.serialize('json',Post.objects.all())
        print (serializer.data)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')
    elif posts.belong_to == u"整租":
        try:
            war = Warnings.objects.get(posts_type=u"整租")
            war = war.content
        except:
            war = ""
        serializer = EntireRentSerializer(posts.entirerent)
        context={
            'code':0,
            'msg':u'成功',
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'reply_message_array':reply_message_array,
            'data':serializer.data,
        }
        return HttpResponse(json.dumps(context),content_type='application/json')

def post_delete(request,pid):
    if not request.user.is_superuser:
        data={
            'code':1,
            'msg':u'非管理员用户无法直接删除帖子'
        }
        return json_response(data)
    post=Post.objects.get(id=pid)
    post.delete()
    data={
        'code':0,
        'msg':u'成功',
    }
    return json_response(data)

def posts_create(request,types):
    if request.method=='POST':
        if types == 'rent':
            belong = '个人转租'
            postsForm = CreateRentForm(request.POST)
            #pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif types == 'shared':
            belong = '合租'
            postsForm = CreateShareForm(request.POST)
            pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif types == 'car':
            belong = '二手车'
            postsForm = CreateCarForm(request.POST)
            pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        posts = postsForm.save(commit=False)
        
        posts.belong_to = belong
        posts.author = request.user  
        posts.content = posts.content          
        posts.save()
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for im in images:
                picture = Rentpicture(post_id=posts.id, image=im)
                picture.save()
        user = request.user
        if user.phone == '' or user.phone == None:
            user.phone = posts.phone
            user.save()
        if user.weixin == '' or user.weixin == None:
            user.weixin = posts.weixin
            user.save()
        data={
            'code':0,
            'msg':1,
            'post_id':posts.id,
        }
        return json_response(data)

def carinspect(request,ciid):
    inspect = CarInspection.objects.get(id=ciid)
    if request.method=='GET':
        data={
            'code':0,
            'msg':u'成功',
            'inspect':inspect.to_dict,
        }
        return json_response(data)
    else:
        form = InspectForm(request.POST, instance=inspect)
        if form.is_valid():
            form.save()
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

def buy_car(request):
    template_name = 'csinla_posts/CarMessage.html'
    if request.method=='POST':
        form = CustomizedCarForm(request.POST)
        form.author = request.user.username
        if form.is_valid():
            body = '汽车定制表单:  '
            cd = form.cleaned_data
            body = body + '类别:  ' + str(cd['car_type'].encode('utf-8'))
            body = body + '品牌:  ' + str(cd['brand'].encode('utf-8'))
            body = body + '车龄:  ' + str(cd['vehicle_age']).encode('utf-8')
            body = body + '里程:  ' + str(cd['vehicle_miles']).encode('utf-8')
            body = body + '级别:  ' + str(cd['level_type'].encode('utf-8'))
            body = body + '变速器:  ' + str(cd['transmission'].encode('utf-8'))
            body = body + '驱动:  ' + str(cd['drive_type'].encode('utf-8'))
            body = body + '颜色:  ' + str(cd['color'].encode('utf-8'))
            body = body + '燃油类型:  ' + str(cd['oil_type'].encode('utf-8'))
            body = body + '涡轮增压:  ' + str(cd['turbo'].encode('utf-8'))
            body = body + '联系人:  ' + str(cd['contactor'].encode('utf-8'))
            body = body + '其他要求:  ' + str(cd['claim'].encode('utf-8'))
            car = form.save()
            #send_feedback_mail(body, "buycar")
            t = threading.Thread(target=send_feedback_mail, args=(body, "buycar"))
            t.start()
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

def deletepost(request,pk):
    post=Post.objects.get(id=pk)
    post.delete()
    data={
        'code':0,
        'msg':u'成功',
    }
    return HttpResponse(json.dumps(data),content_type='application/json;charset=utf-8')


def changepost(request,posts_id):
    if request.method=='GET':
        posts = Post.objects.get(id=posts_id)
        picture_list = Rentpicture.objects.filter(post__id=posts_id)
        picture_array=[]
        for picture in picture_list:
            picture_array.append(picture.to_dict)
        if posts.belong_to == u"个人转租":
            data={
                'code':0,
                'msg':u'成功',
                'rent':posts.rent.to_dict,
                'picture_array':picture_array,
            }
            return json_response(data)
        elif posts.belong_to == u"合租":
            data={
                'code':0,
                'msg':u'成功',
                'rent2':posts.rent2.to_dict,
                'picture_array':picture_array,
            }
            return json_response(data)
        elif posts.belong_to == u"二手车":
            data={
                'code':0,
                'msg':u'成功',
                'car':posts.car.to_dict,
                'picture_array':picture_array,
            }
            return json_response(data)
        elif posts.belong_to == u"二手商品":
            usedgoodsForm = CreateUsedGoodsForm(instance=posts.usedgoods)
            usedgoods=posts.usedgoods
            tag_list=UsedGoodsTag.objects.all()
            tag_array=[]
            for tag in tag_list:
                tag_array.append(tag.to_dict)
            select_tag_id_array=[]
            for tag in usedgoods.tags.all():
                select_tag_id_array.append(tag.id)
            context={
                'code':0,
                'msg':u'成功',
                'usedgoods': usedgoods.to_dict,
                'picture_array': picture_array,
                'select_tag_id_array':select_tag_id_array,
                'tag_array':tag_array,
            }
            item_count=usedgoods.usedgoodsitem_set.all().count()
            if item_count>0:
                context.update({
                    'first_item':usedgoods.usedgoodsitem_set.all().order_by('id')[0],    
                })
            if item_count>1:
                i=1
                item_list=[]
                for usedgoodsitem in usedgoods.usedgoodsitem_set.all().order_by('id')[1:]:
                    item_list.append({
                        'item_index':i,
                        'item_value':usedgoodsitem.to_dict,
                    })
                    i+=1
                context.update({
                    'item_list':item_list,    
                })
            return json_response(context)
        elif posts.belong_to == u"二手书":
            usedbookForm = CreateUsedBookForm(instance=posts.usedbook)
            usedbook=posts.usedbook
            context={
                'code':0,
                'msg':u'成功',
                'usedbook':usedbook.to_dict,
                'picture_array':picture_array,
            }
            item_count=usedbook.usedbookitem_set.all().count()
            if item_count>0:
                context.update({
                    'first_item':usedbook.usedbookitem_set.all().order_by('id')[0].to_dict,    
                })
            if item_count>1:
                i=1
                item_list=[]
                for usedbookitem in usedbook.usedbookitem_set.all().order_by('id')[1:]:
                    item_list.append({
                        'item_index':i,
                        'item_value':usedbookitem.to_dict,    
                    })
                    i+=1
                context.update({
                    'item_list':item_list,    
                })
            return json_response(context)
        elif posts.belong_to == u"朋友圈":
            data={
                'code':0,
                'msg':u'成功',
                'exposure':posts.exposure.to_dict,
                'picture_array':picture_array,
            }
            return json_response(data)
    else:
        posts = Post.objects.get(id=posts_id)
        if posts.belong_to == u"个人转租":
            postsForm = CreateRentForm(request.POST, instance=posts.rent)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif posts.belong_to == u"合租":
            postsForm = CreateShareForm(request.POST, instance=posts.rent2)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif posts.belong_to == u"二手车":
            postsForm = CreateCarForm(request.POST, instance=posts.car)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif posts.belong_to==u'二手商品':
            postsForm = CreateUsedGoodsForm(request.POST, instance=posts.usedgoods)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
            else:
                goods_detail_str=request.POST.get('goods_detail_str','')
                back_id_list=[]
                for goods_str in goods_detail_str.split('~#~'):
                    if goods_str:
                        item_array=goods_str.split('~*~')[:3]
                        if not set(['','undefined'])&set(item_array):
                            ugiid=int(item_array[2])
                            if ugiid!=0:
                                back_id_list.append(ugiid)
                                usedgoodsitem=UsedGoodsItem.objects.get(id=ugiid)
                                usedgoodsitem.name=item_array[0]
                                usedgoodsitem.price=int(item_array[1])
                                usedgoodsitem.save()
                            else:
                                usedgoodsitem=UsedGoodsItem.objects.create(usedgoods=posts.usedgoods,name=item_array[0],price=int(item_array[1]))
                                back_id_list.append(usedgoodsitem.id)
                for usedgoodsitem in posts.usedgoods.usedgoodsitem_set.all():
                    if not usedgoodsitem.id in back_id_list:
                        usedgoodsitem.delete()
        elif posts.belong_to==u'二手书':
            postsForm = CreateUsedBookForm(request.POST, instance=posts.usedbook)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
            else:
                book_detail_str=request.POST.get('book_detail_str','')
                back_id_list=[]
                for book_str in book_detail_str.split('~#~'):
                    if book_str:
                        item_array=book_str.split('~*~')[:4]
                        if not set(['','undefined'])&set([item_array[0],item_array[1],item_array[3]]):
                            ubiid=int(item_array[3])
                            if ubiid!=0:
                                back_id_list.append(ubiid)
                                usedbookitem=UsedBookItem.objects.get(id=ubiid)
                                usedbookitem.name=item_array[0]
                                usedbookitem.price=int(item_array[1])
                                usedbookitem.isbn=item_array[2]
                                usedbookitem.save()
                            else:
                                usedbookitem=UsedBookItem.objects.create(usedbook=posts.usedbook,name=item_array[0],price=int(item_array[1]),isbn=item_array[2])
                                back_id_list.append(usedbookitem.id)
                for usedbookitem in posts.usedbook.usedbookitem_set.all():
                    if not usedbookitem.id in back_id_list:
                        usedbookitem.delete()
        elif posts.belong_to == u"朋友圈":
            postsForm = CreateExposureForm(request.POST, instance=posts.exposure)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        posts = postsForm.save(commit=False)
        if 'image' in request.FILES:
            Rentpicture.objects.filter(post__id=posts_id).delete()
            images = request.FILES.getlist('image')
            for im in images:
                picture = Rentpicture(post_id=posts.id, image=im)
                picture.save()
        posts.author = request.user
        posts.active = timezone.now()
        posts.save()
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)

def set_top(request, posts_id):
    posts = Post.objects.get(id=posts_id)
    if posts.is_top:
        posts.is_top = False
    else:
        posts.is_top = True
    posts.save()
    data={
        'code':0,
        'msg':u'成功',
    }
    return json_response(data)


def postmessage_leave(request):
    if request.method=='POST':
        user = request.user
        if not request.user.is_authenticated(): 
            data={
                'code':2,
                'msg':u'请先登录',
            }
            return json_response(data)
        operate_type = request.POST.get('operate', '')
        if request.method == 'POST':
            cds=request.POST.dict()
            if operate_type=='reply':
                post_id = int(cds.get('post', 0) or 0)
                post=Post.objects.get(id=post_id)
                content=cds.get('content','')
                reply_message_id=int(cds.get('reply_message', 0) or 0)
                postmessage=PostMessage(creator=user,message_type='REPLY',post=post,content_text=content)
                if reply_message_id:
                    postmessage.reply_message_id=reply_message_id
                postmessage.save()
                flex_base64_data = request.POST.get('content_image')
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
                    MessageImageItem.objects.create(postmessage=postmessage, content_image=file_image)
                    # if 'image' in request.FILES:
                    #     images = request.FILES.getlist('image')
                    #     for im in images:
                    #         messageimageitem = MessageImageItem(postmessage=postmessage, content_image=im)
                    #         messageimageitem.save()
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return json_response(data)
            elif operate_type=='collect':
                post_id = int(cds.get('post', 0) or 0)
                post=Post.objects.get(id=post_id)
                try:
                    postmessage=PostMessage.objects.get(message_type='COLLECT',creator=user,post=post)
                    if postmessage.is_valid==False:
                        postmessage.is_valid=True
                        postmessage.save()
                    else:
                        data={
                            'code':1,
                            'msg':u'您已经收藏过，无法继续收藏',
                        }
                        return json_response(data)
                except PostMessage.DoesNotExist:
                    PostMessage.objects.create(message_type='COLLECT',creator=user,post=post)
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return json_response(data)
            elif operate_type=='collect_cancel':
                post_id = int(cds.get('post', 0) or 0)
                post=Post.objects.get(id=post_id)
                try:
                    postmessage=PostMessage.objects.get(message_type='COLLECT',creator=user,post=post)
                    if postmessage.is_valid==True:
                        postmessage.is_valid=False
                        postmessage.save()
                        data={
                            'code':0,
                            'msg':u'成功',
                        }
                        return json_response(data)
                except PostMessage.DoesNotExist:
                    pass
                data={
                    'code':1,
                    'msg':u'您尚未收藏',
                }
                return json_response(data)
            elif operate_type=='collect_read':
                pmid=int(request.POST.get('pmid',0))
                if not pmid:
                    data={
                        'code':1,
                        'msg':u'参数缺失',
                    }
                    return json_response(data)
                postmessage=PostMessage.objects.get(id=pmid)
                if postmessage.message_type=='COLLECT' and postmessage.is_valid:
                    postmessage.has_read=True
                    postmessage.save()
                    data={
                        'code':0,
                        'msg':u'成功',
                    }
                    return json_response(data)
                else:
                    data={
                        'code':1,
                        'msg':u'当前消息并非有效的收藏信息',
                    }
                    return json_response(data)
            elif operate_type=='delete':
                if not user.is_superuser:
                    data={
                        'code':1,
                        'msg':u'只有超级用户才可以删除评论',
                    }
                    return json_response(data)
                pmid=int(request.POST.get('pmid',0))
                if not pmid:
                    data={
                        'code':1,
                        'msg':u'参数缺失',
                    }
                    return json_response(data)
                postmessage=PostMessage.objects.get(id=pmid)
                postmessage.delete()
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return json_response(data)
            else:
                data={
                    'code':1,
                    'msg':u'无效操作',
                }
                return json_response(data)

    else:
        return HttpResponse(u'当前操作不接受get请求')


def postmessage_listview(request,pmid):
    if request.method=='POST':
        cds=request.POST.dict()
        postmessage=PostMessage.objects.get(id=pmid)
        message_list=postmessage.reply_message_list
        start_index=cds.get('start',0)
        start_index=int(start_index)
        end_index=cds.get('end',message_list.count())
        end_index=int(end_index)
        message_array=[]
        if start_index<message_list.count():
            for message in message_list[start_index:end_index]:
                message_array.append(message.to_dict)
        data={
            'code':0,
            'msg':u'成功',
            'message_list':message_array,
        }
        return json_response(data)
    else:
        data={
            'code':1,
            'msg':u'当前操作不接受get请求',
        }
        return json_response(data)

# operations
def off_posts(request, posts_id, code):
    records = EmailVerifyRecord.objects.filter(send_type='off_posts', code=code)
    if records:
        posts = Post.objects.get(id=posts_id)
        posts.expire_date = datetime.date.today() - datetime.timedelta(seconds=1)
        posts.save()
        PostHistory.objects.create(post=posts,operator=posts.author,remark=u'用户【%s】下架本帖子，本帖过期' % posts.author)
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)
    else:
        data={
            'code':1,
            'msg':u'无效code',
        }
        return json_response(data)


def stop_posts(request, posts_id, code):
    records = EmailVerifyRecord.objects.filter(send_type='off_posts', code=code)
    if records:
        posts = Post.objects.get(id=posts_id)
        posts.is_notice = False
        posts.save()
        PostHistory.objects.create(post=posts,operator=posts.author,remark=u'用户【%s】取消本帖的消息通知' % posts.author)
        data={
            'code':0,
            'msg':u'成功',
        }
        return json_response(data)
    else:
        data={
            'code':1,
            'msg':u'无效code',
        }
        return json_response(data)
