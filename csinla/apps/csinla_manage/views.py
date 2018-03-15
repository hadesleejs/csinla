#_*_coding:utf-8_*_
import datetime
import threading

import django.utils.timezone as timezone
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from utils.json_utils import json_response
from utils.base_utils import ErrorDic2str

from csinla_accounts.models import *
from csinla_posts.models import *
from csinla_manage.forms import *
from utils.base_utils import ErrorDic2str

# accounts
def carfax_view(request):
    user=request.user
    if not user.is_carfax_manager:  
        return HttpResponse(u'当前用户无权进行此操作')
    carfax_status=request.GET.get('status','ACTIVE')
    carfax_list=Carfax.objects.filter(carfax_status=carfax_status)
    context={
        'carfax_list':carfax_list,
        'carfax_status':carfax_status,
    }
    return render(request,'csinla_manage/carfax_view.html',context)

@csrf_exempt
def carfax_reply_change(request,cfid):
    user=request.user
    if not user.is_carfax_manager:
        return HttpResponse(u'当前用户无权进行此操作')
    carfax=Carfax.objects.get(id=cfid)
    if carfax.is_reply:
        carfax.is_reply=False
    else:
        carfax.is_reply=True
    carfax.save()
    return HttpResponseRedirect('/manage/carfax/view/')

@csrf_exempt
def carfax_status_change(request,cfid):
    user=request.user
    if not user.is_carfax_manager:
        return HttpResponse(u'当前用户无权进行此操作')
    carfax=Carfax.objects.get(id=cfid)
    if carfax.carfax_status=='ACTIVE':
        carfax.carfax_status='BACKUP'
        carfax.save()
        return HttpResponseRedirect('/manage/carfax/view/')
    elif carfax.carfax_status=='BACKUP':
        carfax.carfax_status='ACTIVE'
        carfax.save()
        return HttpResponseRedirect('/manage/carfax/view?status=BACKUP')
    else:
        return HttpResponse(u'carfax状态有误')
