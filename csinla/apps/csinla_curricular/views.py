# _*_ encoding: utf-8 _*_

import operator
from django.views.generic.base import View
import math
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST, require_GET
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from csinla_curricular.models import Curricular,SearchRecord
from operations.models import Advertising

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
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_D%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request,'csinla_curricular/Classes.html',context)
    else:
        cds=request.POST.dict()
        if request.user.is_authenticated():
            SearchRecord.objects.create(creator=request.user,search_str=str(cds))

        page =int(cds.pop('page',1))
        if not cds.has_key('subject'):
            data={
                'code':1,
                'msg':u'缺少subject参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_start'):
            data={
                'code':1,
                'msg':u'缺少year_start参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_end'):
            data={
                'code':1,
                'msg':u'缺少year_end参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('semester'):
            data={
                'code':1,
                'msg':u'缺少semester参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        
        # clase_total_count1=curricular_list1.count(),
        # A_count1=curricular_list1.aggregate(Sum("sign_a"))['sign_a__sum']
        # B_count1=curricular_list1.aggregate(Sum("sign_b"))['sign_b__sum']
        # AB_count1=A_count1+B_count1
        # total_count1=curricular_list1.aggregate(Sum("sign_total"))['sign_total__sum']
        # A_scale1=int(A_count1*100/total_count1)
        # B_scale1=int(B_count1*100/total_count1)
        # AB_scale1=A_scale1+B_scale1

        curricular_list=curricular_list.filter(subject=cds['subject'],year__gte=int(cds['year_start']),year__lte=int(cds['year_end']),semester__in=cds['semester'].split())
        if cds.has_key('department'):
            curricular_list=curricular_list.filter(department=cds['department'])
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
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif instructor_detail_array_length<end_index:
            data={
                'code':0,
                'msg':u'成功',
                'instructor_detail_array':instructor_detail_array[start_index:],
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data={
                'code':0,
                'msg':u'成功',
                'instructor_detail_array':instructor_detail_array[start_index:end_index],
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


class CurricularView(View):
    # 学生选课，新增不选department也能查出数据
    def get(self,request):
        curricular_list = Curricular.objects.all()
        department_array = []
        subject_array = []
        year_list = curricular_list.values('year').annotate(count=Count('year')).order_by('year')
        department_list = curricular_list.values('department').annotate(count=Count('department')).order_by(
            'department')
        if request.GET.get('export', '') == 'true':
            for department_dic in department_list:
                department_str = department_dic['department']
                for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(
                        count=Count('subject')).order_by('subject'):
                    subject_array.append({
                        'department': department_str,
                        'subject': subject_dic['subject'],
                        'subject_number': subject_dic['subject'].split()[-1],
                    })

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=subject.csv'
            import csv
            writer = csv.writer(response)
            for item in subject_array:
                li = [item['department'], item['subject']]
                print li
                writer.writerow(li)
            return response

        for department_dic in department_list:
            department_str = department_dic['department']
            department_array.append(department_str)
            for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(
                    count=Count('subject')).order_by('subject'):
                subject_array.append({
                    'department': ''.join(department_str.split()),
                    'subject': subject_dic['subject'],
                    'subject_number': subject_dic['subject'].split()[-1],
                })
        subject_array.sort(key=operator.itemgetter('subject_number'), reverse=False)
        context = {
            'department_array': department_array,
            'subject_array': subject_array,
            'year_list': year_list,
        }
        for i in range(1, 6):
            web_belong_to = u'选课C%s' % i
            wap_belong_to = u'选课D%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to).exists():
                web_key = 'ad_C%s' % i
                context.update({
                    web_key: Advertising.objects.filter(belong_to=web_belong_to)[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to).exists():
                wap_key = 'ad_D%s' % i
                context.update({
                    wap_key: Advertising.objects.filter(belong_to=wap_belong_to)[0]
                })

        return render(request, 'csinla_curricular/Classes.html', context)
    def post(self,request):
        curricular_list = Curricular.objects.all()
        cds = request.POST.dict()
        if request.user.is_authenticated():
            SearchRecord.objects.create(creator=request.user, search_str=str(cds))

        page = int(cds.pop('page', 1))
        if not cds.has_key('subject'):
            data = {
                'code': 1,
                'msg': u'缺少subject参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_start'):
            data = {
                'code': 1,
                'msg': u'缺少year_start参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_end'):
            data = {
                'code': 1,
                'msg': u'缺少year_end参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('semester'):
            data = {
                'code': 1,
                'msg': u'缺少semester参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

        # clase_total_count1=curricular_list1.count(),
        # A_count1=curricular_list1.aggregate(Sum("sign_a"))['sign_a__sum']
        # B_count1=curricular_list1.aggregate(Sum("sign_b"))['sign_b__sum']
        # AB_count1=A_count1+B_count1
        # total_count1=curricular_list1.aggregate(Sum("sign_total"))['sign_total__sum']
        # A_scale1=int(A_count1*100/total_count1)
        # B_scale1=int(B_count1*100/total_count1)
        # AB_scale1=A_scale1+B_scale1

        curricular_list = curricular_list.filter(subject=cds['subject'], year__gte=int(cds['year_start']),
                                                 year__lte=int(cds['year_end']), semester__in=cds['semester'].split())
        if cds['department'] != 'select':

            curricular_list = curricular_list.filter(department=cds['department'])
        # if curricular_list == []:
        else:
           curricular_list = curricular_list.filter(subject=cds['subject'], year__gte=int(cds['year_start']),
                                                     year__lte=int(cds['year_end']),
                                                     semester__in=cds['semester'].split())
        instructor_detail_array = []
        for item in curricular_list.values('instructor').annotate(count=Count('instructor')).order_by('instructor'):
            instructor = item['instructor']
            instructor_class_count = item['count']
            instructor_curricular_list = curricular_list.filter(instructor=instructor)
            print instructor_curricular_list.aggregate(Sum("sign_a"))
            A_count = instructor_curricular_list.aggregate(Sum("sign_a"))['sign_a__sum']
            B_count = instructor_curricular_list.aggregate(Sum("sign_b"))['sign_b__sum']
            C_count = instructor_curricular_list.aggregate(Sum("sign_c"))['sign_c__sum']
            D_count = instructor_curricular_list.aggregate(Sum("sign_d"))['sign_d__sum']
            F_count = instructor_curricular_list.aggregate(Sum("sign_f"))['sign_f__sum']
            P_count = instructor_curricular_list.aggregate(Sum("sign_p"))['sign_p__sum']
            NP_count = instructor_curricular_list.aggregate(Sum("sign_np"))['sign_np__sum']
            total_count = instructor_curricular_list.aggregate(Sum("sign_total"))['sign_total__sum']

            A_scale = int(A_count * 100 / total_count)
            B_scale = int(B_count * 100 / total_count)
            C_scale = int(C_count * 100 / total_count)
            D_scale = int(D_count * 100 / total_count)
            F_scale = int(F_count * 100 / total_count)
            P_scale = int(P_count * 100 / total_count)
            NP_scale = int(NP_count * 100 / total_count)
            instructor_curricular_array = []
            for instructor_curricular in instructor_curricular_list:
                sign_a = instructor_curricular.sign_a
                sign_b = instructor_curricular.sign_b
                sign_c = instructor_curricular.sign_c
                sign_d = instructor_curricular.sign_d
                sign_f = instructor_curricular.sign_f
                sign_p = instructor_curricular.sign_p
                sign_np = instructor_curricular.sign_np
                sign_total = instructor_curricular.sign_total

                sign_a_scale = int(sign_a * 100 / sign_total)
                sign_b_scale = int(sign_b * 100 / sign_total)
                sign_c_scale = int(sign_c * 100 / sign_total)
                sign_d_scale = int(sign_d * 100 / sign_total)
                sign_f_scale = int(sign_f * 100 / sign_total)
                sign_p_scale = int(sign_p * 100 / sign_total)
                sign_np_scale = int(sign_np * 100 / sign_total)
                instructor_curricular_array.append({
                    'subject': instructor_curricular.subject,
                    'sign_a': sign_a,
                    'sign_b': sign_b,
                    'sign_c': sign_c,
                    'sign_d': sign_d,
                    'sign_f': sign_f,
                    'sign_p': sign_p,
                    'sign_np': sign_np,
                    'sign_total': sign_total,
                    'sign_a_scale': sign_a_scale,
                    'sign_b_scale': sign_b_scale,
                    'sign_c_scale': sign_c_scale,
                    'sign_d_scale': sign_d_scale,
                    'sign_f_scale': sign_f_scale,
                    'sign_p_scale': sign_p_scale,
                    'sign_np_scale': sign_np_scale,
                })
            instructor_curricular_array.sort(key=operator.itemgetter('sign_a_scale'), reverse=True)
            instructor_info = {
                'instructor_class_total': instructor_class_count,
                'instructor': instructor,
                'A_count': A_count,
                'B_count': B_count,
                'C_count': C_count,
                'D_count': D_count,
                'F_count': F_count,
                'P_count': P_count,
                'NP_count': NP_count,
                'total_count': total_count,
                'A_scale': A_scale,
                'B_scale': B_scale,
                'C_scale': C_scale,
                'D_scale': D_scale,
                'F_scale': F_scale,
                'P_scale': P_scale,
                'NP_scale': NP_scale,
                'instructor_curricular_array': instructor_curricular_array,
            }
            instructor_detail_array.append(instructor_info)

        instructor_detail_array.sort(key=operator.itemgetter('A_scale'), reverse=True)
        instructor_detail_array_length = len(instructor_detail_array)
        start_index = (page - 1) * 40
        end_index = page * 40
        if instructor_detail_array_length <= start_index:
            data = {
                'code': 2,
                'msg': u'数据已取完',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif instructor_detail_array_length < end_index:
            data = {
                'code': 0,
                'msg': u'成功',
                'instructor_detail_array': instructor_detail_array[start_index:],
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {
                'code': 0,
                'msg': u'成功',
                'instructor_detail_array': instructor_detail_array[start_index:end_index],
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

def subjects_compare(request):
    if request.method=='POST':
        # if not request.user.is_authenticated():
        #     data={
        #         'code':3,
        #         'msg':u'请先登录',
        #     }
        #     return HttpResponse(json.dumps(data), content_type='application/json')
        cds=request.POST.dict()
        if not cds.has_key('subject1'):
            data={
                'code':1,
                'msg':u'缺少第一个subject参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('subject2'):
            data={
                'code':1,
                'msg':u'缺少第二个subject参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_start'):
            data={
                'code':1,
                'msg':u'缺少最早年份参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('year_end'):
            data={
                'code':1,
                'msg':u'缺少最晚年份参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        if not cds.has_key('semester'):
            data={
                'code':1,
                'msg':u'缺少semester参数',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        curricular_list=Curricular.objects.filter(year__gte=int(cds['year_start']),year__lte=int(cds['year_end']),semester__in=cds['semester'].split())
        scale=cds.get('scale',100)
        scale = int(scale)
        curricular_list1=curricular_list.filter(subject=cds['subject1'])
        if cds.has_key('department1'):
            curricular_list1=curricular_list1.filter(department=cds['department1'])
        clase_total_count1=curricular_list1.count()
        clase_total_count1 = math.ceil(clase_total_count1*scale/100)
        clase_total_count1 = math.ceil(clase_total_count1)
        clase_total_count1=int(clase_total_count1)
        curricular_list1=curricular_list1[:clase_total_count1]
        A_count1=curricular_list1.aggregate(Sum("sign_a"))['sign_a__sum']
        B_count1=curricular_list1.aggregate(Sum("sign_b"))['sign_b__sum']
        AB_count1=int(A_count1)+int(B_count1)
        total_count1=curricular_list1.aggregate(Sum("sign_total"))['sign_total__sum']
        A_scale1=int(A_count1*100/total_count1)
        B_scale1=int(B_count1*100/total_count1)
        AB_scale1=A_scale1+B_scale1

        instructor_detail1_array=[]
        for item in  curricular_list1.values('instructor').annotate(count=Count('instructor')):
            instructor=item['instructor']
            instructor_class_count=item['count']
            instructor_curricular_list = Curricular.objects.filter(year__gte=int(cds['year_start']),
                                                        year__lte=int(cds['year_end']),
                                                        semester__in=cds['semester'].split())
            instructor_curricular_list = instructor_curricular_list.filter(subject=cds['subject1'])
            if cds.has_key('department1'):
                instructor_curricular_list = instructor_curricular_list.filter(department=cds['department1'])
            instructor_curricular_list=instructor_curricular_list.filter(instructor=instructor)
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
            'name1':cds['subject1'],
            'nums1':len(instructor_detail1_array),
        }
        curricular_list2=curricular_list.filter(department=cds['department2'],subject=cds['subject2'])
        if cds.has_key('department2'):
            curricular_list2=curricular_list2.filter(department=cds['department2'])
        clase_total_count2=curricular_list2.count()
        clase_total_count2 = math.ceil(clase_total_count2*scale/100)
        clase_total_count2 = math.ceil(clase_total_count2)
        clase_total_count2=int(clase_total_count2)
        curricular_list2=curricular_list2[:clase_total_count2]
        A_count2=curricular_list2.aggregate(Sum("sign_a"))['sign_a__sum']
        B_count2=curricular_list2.aggregate(Sum("sign_b"))['sign_b__sum']
        AB_count2=A_count2+B_count2
        total_count2=curricular_list2.aggregate(Sum("sign_total"))['sign_total__sum']
        A_scale2=int(A_count2*100/total_count2)
        B_scale2=int(B_count2*100/total_count2)
        AB_scale2=A_scale2+B_scale2

        instructor_detail2_array=[]
        for item in  curricular_list2.values('instructor').annotate(count=Count('instructor')):
            instructor=item['instructor']
            instructor_class_count=item['count']
            instructor_curricular_list = Curricular.objects.filter(year__gte=int(cds['year_start']),
                                                                   year__lte=int(cds['year_end']),
                                                                   semester__in=cds['semester'].split())
            instructor_curricular_list = instructor_curricular_list.filter(subject=cds['subject2'])
            if cds.has_key('department2'):
                instructor_curricular_list = instructor_curricular_list.filter(department=cds['department2'])
            instructor_curricular_list = instructor_curricular_list.filter(instructor=instructor)
            # print instructor_curricular_list.aggregate(Sum("sign_a"))
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
            'name2': cds['subject2'],
            'nums2': len(instructor_detail2_array),
        }
        data={
            'code':0,
            'msg':u'成功',
            'subject1_info':subject1_info,
            'subject2_info':subject2_info,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
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
            'department_array':department_array,
            'subject_array':subject_array,
        }
        return render(request,'csinla_curricular/compare.html',context)




    # if not cds.has_key('department1'):
    # if not cds.has_key('department1'):
    # if not cds.has_key('department1'):
    # if not cds.has_key('department1'):
    # if not cds.has_key('department1'):
    # if not cds.has_key('department1'):


    # if cds.has_key('department'):
    #     curricular_list=curricular_list.filter(department=cds['department'])
    #     if cds.has_key('subject'):
    #         curricular_list=curricular_list.filter(subject=cds['subject'])
    
    # if request.method=='GET':
    #     department_array=[]
    #     subject_array=[]
    #     department_list=curricular_list.values('department').annotate(count=Count('department')).order_by('department')
    #     for department_dic in department_list:
    #         department_str=department_dic['department']
    #         department_array.append(department_str)
    #         subject_item_list=[]
    #         for subject_dic in curricular_list.filter(department=department_str).values('subject').annotate(count=Count('subject')).order_by('subject'):
    #             subject_array.append({
    #                 'department':department_str,
    #                 'subject':subject_dic['subject'],
    #             })
    #     context = {
    #         'department_array':department_array,
    #         'subject_array':subject_array,
    #     }
    #     return render(request,'csinla_curricular/Classes.html',context)
    # else:
    #     paginator = Paginator(curricular_list, 12)
    #     cds=request.POST.dict()
    #     page =cds.get('page',1)
    #     try:
    #         curricular_list = paginator.page(page)
    #     except PageNotAnInteger:
    #         curricular_list = paginator.page(1)
    #     except EmptyPage:
    #         curricular_list = paginator.page(paginator.num_pages)
    #     curricular_array=[]
    #     for curricular in curricular_list:
    #         curricular_array.append(curricular.to_dict)
    #     data={
    #         'code':0,
    #         'msg':u'成功',
    #         'curricular_array':curricular_array,
    #     }
    #     return HttpResponse(json.dumps(data), content_type='application/json')
    
def pdf_view(request):
    return render(request,'csinla_curricular/pdf.html')

def build_view(request):
    return render(request,'build1/build/generic/web/view.html')
