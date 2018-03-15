# coding=utf-8
import datetime
import threading
import base64
import json

from django.apps import apps
import django.utils.timezone as timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View

from fun.models import *
from fun.forms import *
# from utils.email_send import send_feedback_mail

def home(request):
    context={

    }
    return render(request,'fun/index.html',context)

def fun_home(request):
    activity_list=Activity.objects.all()
    context={

    }
    if activity_list:
        context.update({
            'activity':activity_list[0],
        })
    return render(request,'fun/fun.html',context)

def activity_view(request):
    activity_list=Activity.objects.all()
    context={
        'activity_list':activity_list,
    }
    template=request.GET.get('template','fun/activity/activity_view.html')
    return render(request,template,context)

def activity_detail(request,aid):
    activity=Activity.objects.get(id=aid)
    context={
        'activity':activity,
    }
    template=request.GET.get('template','fun/activity/activity_detail.html')
    return render(request,template,context)

def activity_add(request):
    if request.method=='POST':
        form=CreateActivityForm(request.POST)
        if form.is_valid():
            activity=form.save()
            return HttpResponseRedirect('/fun/activity/edit/%s' % activity.id)
    else:
        form=CreateActivityForm()
    context={
        'form':form,
    }
    template=request.GET.get('template','fun/activity/activity_add.html')
    return render(request,template,context)

class ActivityEditView(View):
    def post(self,request,aid):
        activity=Activity.objects.get(id=aid)
        if 'image1' in request.FILES:
            cover_image = request.FILES.get('image1')
            activity.cover_image = cover_image
            activity.save()
            data={
                'code':0,
                'msg':u'封面保存成功',
            }
        if 'image2' in request.FILES:
            activity=Activity.objects.get(id=aid)
            ticket_image = request.FILES.get('image2')
            activity.ticket_image = ticket_image
            activity.save()
            data={
                'code':0,
                'msg':u'门票保存成功',
            }
        return HttpResponse(json.dumps(data), content_type='application/json')
    def get(self,request,aid):
        activity=Activity.objects.get(id=aid)
        cover_image = activity.cover_image
        ticket_image = activity.ticket_image
        context={
            'activity':activity,
            'cover_image':cover_image,
            'ticket_image':ticket_image,
        }
        template=request.GET.get('template','fun/activity/activity_edit.html')
        return render(request,template,context)

@csrf_exempt
def cover_image_edit(request,aid):
    activity=Activity.objects.get(id=aid)
    if 'image' in request.FILES:
        cover_image = request.FILES.get('image')
        activity.cover_image = cover_image
        activity.save()
        data={
            'code':0,
            'msg':u'封面保存成功',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    data={
            'code':1,
            'msg':u'图片为空',
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def ticket_image_edit(request,aid):
    if 'image' in request.FILES:
        activity=Activity.objects.get(id=aid)
        ticket_image = request.FILES.get('image')
        activity.ticket_image = ticket_image
        activity.save()
        data={
            'code':0,
            'msg':u'门票保存成功',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    data={
            'code':1,
            'msg':u'图片为空',
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

def contact(request):
    if request.method=='POST':
        form=CreateContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(u'失败：%s' % form.errors)
    else:
        return render(request,'fun/contact.html')

def activity_pay(request,atid):
    activitytimeitem=ActivityTimeItem.objects.get(id=atid)
    cds=request.POST.dict()
    customer_email=cds.get('email',u'张三')
    customer_name=cds.get('name','84742334@qq.com')
    join_count=int(cds.get('join_count',1))
    remark=cds.get('remark','')
    totle_join=0
    for order in activitytimeitem.activityorder_set.filter(order_status='SENT'):
        totle_join+=order.join_count
    if totle_join+join_count>activitytimeitem.totel_count:
        left_count=activitytimeitem.totel_count - totle_join
        return HttpResponse(u'当前剩余名额%s个，您报名人数过多' % left_count)
    order=ActivityOrder.objects.create(customer_name=customer_name,customer_email=customer_email,order_status='SENT',join_count=join_count,remark=remark,activitytimeitem=activitytimeitem)
    return HttpResponseRedirect('/fun/paid_success/%s/' % order.id)


def paid_success(request,aoid):
    activityorder=ActivityOrder.objects.get(id=aoid)
    context={
        'activityorder':activityorder,
    }
    template=request.GET.get('template','fun/paid_success.html')
    return render(request,template,context)

@csrf_exempt
def image_process(request):
    cds=request.GET.dict()
    app_name=cds.get('app','fun')
    model_name=cds.get('model','Activity')
    obj_id=cds.get('obj_id',3)
    obj_id=int(obj_id)
    field_name=cds.get('field','cover_image')
    if not app_name or not model_name or not field_name or not obj_id:
        return HttpResponse(u'参数不足')
    modelobj=apps.get_model(app_name,model_name)
    obj=modelobj.objects.get(id=obj_id)
    if request.method=='GET':
        image=getattr(obj,  field_name, None)
        context={
            'image':image,
        }
        return render(request,'fun/image_process.html',context)
    else:
        file_image=request.FILES.get('image',None)
        if file_image:
            setattr(obj, field_name, file_image)
            obj.save()
            data={
                'code':0,
                'msg':u'成功',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # flex_base64_data = request.POST.get('image')
        # if flex_base64_data:
        #     mediatype, base64_data = flex_base64_data.split(',', 1)
        #     start_index = mediatype.index('/')
        #     end_index = mediatype.index(';')
        #     image_type = mediatype[(start_index + 1):end_index]
        #     # 存文件
        #     file_image = base64.b64decode(base64_data)
        #     fn = time.strftime('%Y%m%d%H%M%S')
        #     fn_ran = fn + '_%d' % random.randint(0, 100)
        #     # 重写合成文件名
        #     file_name = ''.join(fn_ran + '.' + image_type)
        #     file_image = ContentFile(file_image, file_name)
        #     setattr(obj, field_name, file_image)
        #     obj.save()
        #     data={
        #         'code':0,
        #         'msg':u'成功',
        #     }
        #     return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data={
                'code':1,
                'msg':u'内容缺失',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
