# coding=utf-8

import urlparse
import logging
import json
from django.shortcuts import render_to_response, resolve_url
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.http import base36_to_int, is_safe_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.middleware.csrf import rotate_token
from django.contrib.sites.shortcuts  import get_current_site
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from .forms import TicketAuthenticationForm
from .models import Ticket
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from SSO.forms import AccountSettingForm
from SSO.models import Ticket,TempTicket
from utils.base_utils import ErrorDic2str
from utils.json_utils import json_response
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@sensitive_post_parameters()
@never_cache
@csrf_exempt
def login(request, template_name='csinla_auth/home_signIn.html',
                    redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.POST.get(redirect_field_name,request.GET.get(redirect_field_name, '/'))
    error = ''
    if request.method == 'POST':
        form = TicketAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            #if not is_safe_url(url=redirect_to, host=request.get_host()):
                #redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            rotate_token(request)
            response = HttpResponseRedirect(redirect_to)
            response.set_cookie('ticket', form.cleaned_data['ticket'])
            return response
        else:
            error = u'请输入正确的用户名和密码'
    else:
        open_id=request.GET.get('open_id','')
        from csinla_accounts.models import WechatInfo
        try:
            wechatinfo=WechatInfo.objects.get(open_id=open_id)
            t=Ticket.objects.create_ticket(user=wechatinfo.userinfo)
            response = HttpResponseRedirect('/')
            response.set_cookie('ticket', t.ticket)
            return response
        except WechatInfo.DoesNotExist:
            pass

    # try:
    #     if request.session['old_url']  != '/accounts/myinfo/':
    #         request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
    # except:
    #     request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
    # return render(request, template_name, {})
    # current_site = get_current_site(request)
    context = {
        'error':error,
        # redirect_field_name: redirect_to,
        # 'site':current_site,
        # 'site_name':current_site.name,
    }
    if request.META['HTTP_USER_AGENT'].lower().find('mobile') > 0:
        return TemplateResponse(request, 'csinla_auth/home_signIn_pc.html', context)
    return TemplateResponse(request, template_name, context)
    # return HttpResponse(request,json.dumps(context),template_name)
def logout(request, next_page=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     current_app=None, extra_context=None):
    user = getattr(request, 'user', None)
    Ticket.objects.consume_tickets(request.user)
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    if next_page is not None:
        next_page = resolve_url(next_page)

    # if redirect_field_name in request.REQUEST:
    #     next_page = request.REQUEST[redirect_field_name]
    #     # Security check -- don't allow redirection to a different host.
    #     if not is_safe_url(url=next_page, host=request.get_host()):
    #         next_page = request.path

    return HttpResponseRedirect('/')

@require_POST
@csrf_exempt
def json_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.POST.get(redirect_field_name,request.GET.get(redirect_field_name, '/'))
    form = TicketAuthenticationForm(request, data=request.POST)
    if form.is_valid():
        #if not is_safe_url(url=redirect_to, host=request.get_host()):
            #redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        rotate_token(request)
        data={
            'code':0,
            'msg':u'成功',
            'ticket':form.cleaned_data['ticket'],
            'redirect_to':redirect_to,
        }
        return json_response(data)
        # response.set_cookie('ticket', form.cleaned_data['ticket'])
        # response = HttpResponseRedirect(redirect_to)
        # return response
    else:
        data={
            'code':1,
            'msg':ErrorDic2str(form.errors),
        }
        return json_response(data)
        # error = u'请输入正确的用户名和密码'

    # try:
    #     if request.session['old_url']  != '/accounts/myinfo/':
    #         request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
    # except:
    #     request.session['old_url'] = request.META.get('HTTP_REFERER', '/')
    # return render(request, template_name, {})
    # current_site = get_current_site(request)
    # context = {
    #     'error':error,
    #     # redirect_field_name: redirect_to,
    #     # 'site':current_site,
    #     # 'site_name':current_site.name,
    # }
    # return TemplateResponse(request, template_name, context)

@require_POST
def json_logout(request, next_page=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     current_app=None, extra_context=None):
    user = getattr(request, 'user', None)
    Ticket.objects.consume_tickets(request.user)
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    # if hasattr(user, 'is_authenticated') and not user.is_authenticated():
    #     user = None
    data={
        'code':0,
        'msg':msg,
        'redirect_to':next_page,
    }
    return json_response(data)
    # if next_page is not None:
    #     next_page = resolve_url(next_page)

    # if redirect_field_name in request.REQUEST:
    #     next_page = request.REQUEST[redirect_field_name]
    #     # Security check -- don't allow redirection to a different host.
    #     if not is_safe_url(url=next_page, host=request.get_host()):
    #         next_page = request.path

    # return HttpResponseRedirect('/login/')

def ticket_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.POST.get(redirect_field_name,request.GET.get(redirect_field_name, '/'))
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(redirect_to)
    if request.method=='POST':
        pass
    else:
        operate=request.GET.get('operate','')
        if operate=='login':
            if not request.user.is_authenticated():
                return HttpResponse(u'当前尚未登录')
            else:
                temp_ticket_str = request.GET.get('temp_ticket', '')
                if not temp_ticket_str:
                    return HttpResponse(u'缺失参数temp_ticket')
                try:
                    tempticket=TempTicket.objects.get(temp_ticket=temp_ticket_str)
                    ticket=Ticket.objects.filter(user=request.user).order_by('-id')[0]
                    tempticket.ticket=ticket
                    tempticket.save()
                    return HttpResponse(u'成功')
                except TempTicket.DoesNotExist:
                    return HttpResponse(u'参数temp_ticket无效')
        else:
            temp_ticket=request.COOKIES.get('temp_ticket', '')
            if not temp_ticket:
                tempticket=TempTicket.objects.create_ticket()
                temp_ticket=tempticket.temp_ticket
            else:
                tempticket=TempTicket.objects.get(temp_ticket=temp_ticket)
            response=HttpResponse(temp_ticket)
            response.set_cookie('temp_ticket',temp_ticket)
            return response

                

        # ticket=request.GET.get('qr_ticket','')
        # if ticket:
        #     try:
        #         ticket=Ticket.objects.get(ticket=ticket)
        #         tempticket.ticket=ticket
        #         tempticket.save()
        #         data={
        #             'code':0,
        #             'msg':u'成功',
        #         }
        #         response=json_response(data)
        #         response.set_cookie('temp_ticket',temp_ticket)
        #         return response
        #         # json_response(data)
        #     except TempTicket.DoesNotExist:
        #         data={
        #             'code':1,
        #             'msg':u'不存在temp_ticket',
        #         }
        #         return json_response(data)
        #     except Ticket.DoesNotExist:
        #         data={
        #             'code':1,
        #             'msg':u'无效的ticket',
        #         }
        #         return json_response(data)
        # else:
        #     data={
        #         'code':1,
        #         'msg':u'无ticket参数',
        #     }
        #     return json_response(data)


@csrf_exempt
def account_setting(request):
    if request.method == 'POST':
        cds = json.loads(request.body)
        p = request.user.account.personinfo
        if p:
            f = AccountSettingForm(cds,instance=p)
        else:
            f = AccountSettingForm(cds)
        if not f.is_valid():
            return json_response({'code':1,"msg":ErrorDic2str(f.errors)})
        p = f.save()
        request.user.account.personinfo = p
        request.user.account.save() 
        return json_response({"code":0,"msg":"成功修改个人信息"})
    else:
        person = request.user.account.personinfo
        POSITIONS = Person.POSITIONS
        return render_to_response('sso/account_settings.html',{'person':person,'POSITIONS':POSITIONS},context_instance=RequestContext(request))

@csrf_exempt     
def change_password(request):
    if request.method == 'POST':
        msg=u'修改密码成功'
        code=0
        print request.body
        cds = json.loads(request.body)
        print cds
        u = request.user
        old_pwd = cds.get('old_pwd', '')
        if u.check_password(old_pwd):
            pwd = cds.get('new_pwd', '')
            if len(pwd) < 6 or len(pwd) > 20:
                msg = u'密码长度应该为6到20位之间'
                code = 1
            if pwd == old_pwd:
                msg = u'新旧密码不能相同'
                code = 1
                
            pwd_rep = cds.get('new_pwd_rep','')
            if pwd != pwd_rep:
                msg = u'两次输入的密码不相同'
                code = 1              
        else:
            code = 1
            msg = u'原密码错误'
        if not code:
            u.set_password(pwd)
            u.save()
        return json_response({'code':code,'msg':msg})
    else:
        return render_to_response('sso/change_password.html',context_instance=RequestContext(request))
