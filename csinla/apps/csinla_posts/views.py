# coding=utf-8
from __future__ import division
import datetime
import threading
import json
import base64
import random
import time
# cache_control缓存机制
from django.views.decorators.cache import cache_control
import django.utils.timezone as timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.files.base import ContentFile
from django.views import generic
# from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *
from csinla_accounts.models import CustomizedCar
from operations.models import Warnings, UserFavorite,Advertising
from utils.email_send import send_feedback_mail
from utils.json_utils import json_response
from utils.base_utils import ErrorDic2str,get_page_range
from utils.mixin_utils import LoginRequiredMixin

def search(request):
    key = request.GET.get('keyword')
    post_id = ''
    try:
        posts = Car.objects.get(car_id=key)
        post_id = posts.id
    except:
        try:
            posts = Rent.objects.get(house_id=key)
            post_id = posts.id
        except:
            try:
                posts = Car.objects.get(vin_number=key)
                post_id = posts.id
            except:
                try:
                    posts = UsedGoods.objects.get(used_id=key)
                    post_id = posts.id
                except:
                    try:
                        posts = UsedBook.objects.get(book_id=key)
                        post_id = posts.id
                    except:
                        pass
    if post_id:
        return redirect('posts:detail', posts_id=post_id)
    return redirect('home')



class ListRent(generic.ListView):
    model = Rent
    template_name = 'csinla_posts/houseRenting.html'
    context_object_name = 'Rents'

    def get(self, request):
        rents = Rent.objects.filter(expire_date__gte = timezone.now())
        # rents = Rent.objects.all()
        key = request.GET.get('keyword','')
        cds=self.request.GET.dict()
        page=int(cds.pop('page',1))
        locat = cds.get('locat','')
        type = cds.get('type','')
        price = cds.get('price',0)
        if not price:
            price=0

        if type == '' or locat == '' or price == 0:
            rents = Rent.objects.filter(expire_date__gte = timezone.now())
            # rents = Rent.objects.all()
        else:
            if type != u'全部':
                rents = rents.filter(share = type)
            if locat != u'全部':
                if locat=='OTHER':
                    rents=rents.exclude(district__in=['USC','SMC UCLA','UCSB','UCSD','UCI','ELAC','PCC'])
                else:
                    rents = rents.filter( district = locat)
            if price != u'全部':
                if price == 'other':
                    rents = rents.filter(fee__gte = 1500)
                else:
                    price_up = int(price) - int(500)
                    rents = rents.filter( fee__lte = price , fee__gte = price_up)
        if key:
            rents = rents.filter(Q(title__icontains=key) | Q(content__icontains=key)
                                 |Q(district__icontains=key) | Q(address__icontains=key)
                                 | Q(fee__icontains=key) | Q(share__icontains=key)
                                 | Q(pet__icontains=key) | Q(smoke__icontains=key)
                                 | Q(parking__icontains=key) | Q(gender_require__icontains=key)
                                 |Q(house_id__icontains=key))
        rents=rents.order_by('-is_top','-active')
        numbs = len(rents)
        # if request.user.is_authenticated():
        #     if request.user.is_superuser:
        #         rents=rents.order_by('-is_sys','-is_top','-active')
        # paginator = Paginator(rents,16)
        # try:
        #     rents_p = paginator.page(page)
        # except PageNotAnInteger:
        #     rents_p = paginator.page(1)
        # except EmptyPage:
        #     rents_p = paginator.page(paginator.num_pages)
        # page_range, rents_p = get_page_range(page, rents,17)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(rents,17,request=request)

        rents = p.page(page)
        numb =  int(numbs/17)
        context={
            # 'page_range':page_range,
            'Rents': rents,
            'filter_dic':cds,
            'numb':numb,
            # 'ad_id_array':ad_id_array,
        }
        for i in range(1,8):
            web_belong_to=u'租房A%s' % i
            wap_belong_to=u'租房B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, self.template_name, context)


    def post(self, request):
        rents = Rent.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top','-active')
        locat = self.request.POST.get('locat')
        type = self.request.POST.get('type')
        price = self.request.POST.get('price')

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
        numbs = len(rents)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(rents,17,request=request)
        rents = p.page(page)
        numb =  int(numbs/17)
        context={
            # 'page_range':page_range,
            'Rents': rents,
            'numb':numb,
            # 'ad_id_array':ad_id_array,
        }
        return render(request, self.template_name, context)


class ListEntireRent(generic.ListView):
    # 整租列表
    model = EntireRent
    template_name = 'csinla_posts/list_entire_rent.html'
    context_object_name = 'EntireRents'

    def get(self, request):
        rents = EntireRent.objects.filter(expire_date__gte=timezone.now())
        key = request.GET.get('keyword', '')
        cds = self.request.GET.dict()
        page = int(cds.pop('page', 1))
        locat = cds.get('locat', '')
        type = cds.get('type', '')
        price = cds.get('price', 0)
        if not price:
            price = 0

        if type == '' or locat == '' or price == 0:
            rents = EntireRent.objects.filter(expire_date__gte=timezone.now())
        else:
            if type != u'全部':
                rents = rents.filter(share=type)
            if locat != u'全部':
                if locat == 'OTHER':
                    rents = rents.exclude(district__in=['USC', 'SMC UCLA', 'UCSB', 'UCSD', 'UCI', 'ELAC', 'PCC'])
                else:
                    rents = rents.filter(district=locat)
            if price != u'全部':
                if price == 'other':
                    rents = rents.filter(fee__gte=1500)
                else:
                    price_up = int(price) - int(500)
                    rents = rents.filter(fee__lte=price, fee__gte=price_up)
        if key:
            rents = rents.filter(Q(title__icontains=key) | Q(content__icontains=key)
                                 | Q(district__icontains=key) | Q(address__icontains=key)
                                 | Q(share__icontains=key) | Q(house_type__icontains=key)
                                 | Q(pet__icontains=key) | Q(parking__icontains=key)
                                 | Q(pak_nums__icontains=key)|Q(house_id__icontains=key))
        rents = rents.order_by('-is_top', '-active')
        numbs = len(rents)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(rents,17,request=request)
        rents = p.page(page)
        numb =  int(numbs/17)
        context={
            # 'page_range':page_range,
            'Rents': rents,
            'numb':numb,
            'filter_dic':cds,
            # 'ad_id_array':ad_id_array,
        }
        for i in range(1, 8):
            web_belong_to = u'租房A%s' % i
            wap_belong_to = u'租房B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to).exists():
                web_key = 'ad_A%s' % i
                context.update({
                    web_key: Advertising.objects.filter(belong_to=web_belong_to)[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to).exists():
                wap_key = 'ad_B%s' % i
                context.update({
                    wap_key: Advertising.objects.filter(belong_to=wap_belong_to)[0]
                })
        return render(request, self.template_name, context)
    def post(self, request):
        rents = EntireRent.objects.filter(expire_date__gte=timezone.now()).order_by('-is_top', '-active')
        locat = self.request.POST.get('locat')
        type = self.request.POST.get('type')
        price = self.request.POST.get('price')

        if type == None or locat == None or price == None:
            rents = EntireRent.objects.filter(expire_date__gte=timezone.now()).order_by('-is_top', '-active')
        if type != u'全部' and type != None:
            rents = rents.filter(share=type).order_by('-active')
        if locat != u'全部' and locat != None:
            rents = rents.filter(district=locat).order_by('-active')
        if price != u'全部' and price != None and price != 'other':
            if price == 'other':
                rents = rents.filter(fee__gte=1500).order_by('-active')
            else:
                price_up = int(price) - int(500)
                rents = rents.filter(fee__lte=price, fee__gte=price_up).order_by('-active')

        numbs = len(rents)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(rents,17,request=request)
        rents = p.page(page)
        numb =  int(numbs/17)
        context={
            # 'page_range':page_range,
            'Rents': rents,
            'numb':numb,
            # 'filter_dic':cds,
            # 'ad_id_array':ad_id_array,
        }
        return render(request, self.template_name, context)



class RoomMate(generic.ListView):
    model = Rent2
    template_name = 'csinla_posts/findRoommate.html'
    context_object_name = 'Rents'  

    def get_queryset(self):
        rents = Rent2.objects.filter(expire_date__gte = timezone.now()).order_by('-post_date')
        locat = self.request.GET.get('locat')
        type = self.request.GET.get('type')
        price = self.request.GET.get('price')

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

        paginator = Paginator(rents, 15)
        page = self.request.GET.get('page')
        try:
            rents_p = paginator.page(page)
        except PageNotAnInteger:
            rents_p = paginator.page(1)
        except EmptyPage:
            rents_p = paginator.page(paginator.num_pages)
        
        return rents_p

    def get_context_data(self,  **kwargs):
        # call super class
        context = super(RoomMate, self).get_context_data(**kwargs)
        # context['Rents'] = []
        return context


class ListCar(generic.ListView):
    model = Car
    template_name = 'csinla_posts/secondhandCar.html'
    context_object_name = 'Cars'    

    def get(self, request):
        cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
        # cars = Car.objects.all().order_by('is_top','-active')
        key = request.GET.get('keyword', '')
        cds=self.request.GET.dict()
        page=int(cds.pop('page',1))
        level = cds.get('level','')
        type = cds.get('type','')
        transmission = cds.get('transmission','')
        if type == '' or level == '' or transmission == '':
            cars = Car.objects.filter(expire_date__gte=timezone.now()).order_by('-is_top', '-active')
            # cars = Car.objects.all()

        else:
            if type != u'全部':
                if type == 'other':
                    cars=cars.exclude(car_type__in=[u'日系',u'德系',u'美系'])
                else:
                    cars = cars.filter(car_type = type)
            if level != u'全部':
                if type == 'other':
                    cars=cars.exclude(level_type__in=[u'轿车',u'跑车','SUV'])
                else:
                    cars = cars.filter( level_type = level)
            if transmission != u'全部':
                cars = cars.filter(transmission_type = transmission)
            # if price != u'全部' and price != None and price != 'other':
            #     if int(price) == 10000:
            #         cars = cars.filter(fee__lte = 10000).order_by('-active')
            #     else:
            #         price_up = int(price) - int(5000)
            #         cars = cars.filter(fee__lte = price , fee__gte = price_up).order_by('-active')
            # if price == 'other':
            #     cars = cars.filter(fee__gte = 40000).order_by('-active')
        if key:
            cars = cars.filter(Q(title__icontains=key) | Q(content__icontains=key)
                               | Q(vehicle_miles__icontains=key) | Q(vehicle_age__icontains=key)
                               | Q(car_type_other__icontains=key)| Q(car_id__icontains=key)
                               | Q(brand__icontains=key) | Q(transmission_type__icontains=key)
                               | Q(drive_type__icontains=key) | Q(inside_color__icontains=key)
                               | Q(outside_color__icontains=key) | Q(oil_type__icontains=key))
        cars=cars.order_by('-is_top','-active')
        numbs = len(cars)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(cars,17,request=request)
        cars = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'Cars': cars,
            'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'汽车A%s' % i
            wap_belong_to=u'汽车B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, self.template_name, context)

    def post(self, request):
        cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
        level = self.request.POST.get('level', None)
        type = self.request.POST.get('type', None)
        transmission = self.request.POST.get('transmission', None)
        price = self.request.POST.get('price', None)

        if type == None or level == None or transmission == None:
            cars = Car.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
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
        numbs = len(cars)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(cars,17,request=request)
        cars = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'Cars': cars,
            # 'filter_dic':cds,
        }
        return render(request, self.template_name, context)
        

    def get_context_data(self,  **kwargs):
        # call super class
        context = super(ListCar, self).get_context_data(**kwargs)
        # context['cars'] = []
        return context

class ListUsedGoods(generic.ListView):
    model = UsedGoods
    template_name = 'csinla_posts/UsedGoods_list.html'
    context_object_name = 'UsedGoods_list'    

    def get(self, request):
        usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        key = request.GET.get('keyword', '')
        cds=self.request.GET.dict()
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
        if key:
            usedgoods_list = usedgoods_list.filter(Q(title__icontains=key) | Q(content__icontains=key)
                                                   | Q(district__icontains=key) | Q(address__icontains=key)
                                                   | Q(content_detail__icontains=key) | Q(connect_name__icontains=key))
        usedgoods_list=usedgoods_list.order_by('-is_top','-last_change_time')
        numbs = len(usedgoods_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(usedgoods_list,17,request=request)
        usedgoods_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'UsedGoods_list': usedgoods_list,
            # 'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'二手商品A%s' % i
            wap_belong_to=u'二手商品B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, self.template_name, context)

    def post(self, request):
        usedgoods_list = UsedGoods.objects.filter(expire_date__gte = timezone.now())
        cds=self.request.POST.dict()
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
        numbs = len(usedgoods_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(usedgoods_list,17,request=request)
        usedgoods_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'UsedGoods_list': usedgoods_list,
            'filter_dic':cds,
        }
        return render(request, self.template_name, context)
    def get_context_data(self,  **kwargs):
        # call super class
        context = super(ListUsedGoods, self).get_context_data(**kwargs)
        # context['cars'] = []
        return context

@login_required
@csrf_exempt
def usedgoods_add(request):
    errors=[]
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
                            errors.append(u'商品【%s】的价格格式不合法' % item_name)
            if not errors:
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
                            picture=Rentpicture(post_id=usedgoods.id, image=file_image)
                            picture.save()
                data={
                    'code':0,
                    'msg':u'成功',
                    'post_id':usedgoods.id,
                }
                return json_response(data)
            else:
                print ';'.join(errors)
                data={
                    'code':1,
                    'msg':';'.join(errors),
                }
                return json_response(data)
                # return HttpResponseRedirect('/posts/complete/%s' % usedgoods.id)
    else:
        form = UsedGoodsForm()
    context={
        'form':form,
        'tag_list':tag_list,
        'errors':errors
    }
    return render(request, 'csinla_posts/UsedGoodsAdd.html', context)

class ListUsedBook(generic.ListView):
    model = UsedBook
    template_name = 'csinla_posts/usedbook_view.html'
    context_object_name = 'UsedBook_list'    

    def get(self, request):
        usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        key = request.GET.get('keyword', '')
        cds=self.request.POST.dict()
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
        if key:
            usedbook_list = usedbook_list.filter(Q(title__icontains=key) | Q(content__icontains=key)
                                                 | Q(district__icontains=key) | Q(address__icontains=key)
                                                 | Q(content_detail__icontains=key)| Q(connect_name__icontains=key))

        usedbook_list=usedbook_list.order_by('-is_top','-last_change_time')
        numbs = len(usedbook_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(usedbook_list,17,request=request)
        usedbook_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'UsedBook_list': usedbook_list,
            'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'二手书A%s' % i
            wap_belong_to=u'二手书B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, self.template_name, context)

    def post(self, request):
        usedbook_list = UsedBook.objects.filter(expire_date__gte = timezone.now())
        cds=self.request.POST.dict()
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
        numbs = len(usedbook_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(usedbook_list,17,request=request)
        usedbook_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'UsedBook_list': usedbook_list,
            'filter_dic':cds,
        }
        for i in range(1,8):
            web_belong_to=u'二手书A%s' % i
            wap_belong_to=u'二手书B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, self.template_name, context)
    
    def get_context_data(self,  **kwargs):
        # call super class
        context = super(ListUsedBook, self).get_context_data(**kwargs)
        # context['cars'] = []
        return context

@login_required
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
                            errors.append(u'二手书【%s】价格格式有误' % item_name)
            print usedbookitem_array
            if not errors:
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
                flex_base64_data_list_str = request.POST.get('image')
                if flex_base64_data_list_str:
                    for flex_base64_data in flex_base64_data_list_str.split('$$$$$'):
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
                            picture=Rentpicture(post_id=usedbook.id, image=file_image)
                            picture.save()
                data={
                    'code':0,
                    'msg':u'成功',
                    'post_id':usedbook.id,
                }
                return json_response(data)
            else:
                print ';'.join(errors)
                data={
                    'code':1,
                    'msg':';'.join(errors),
                }
                return json_response(data)

    else:
        form = UsedBookForm()
    return render(request, 'csinla_posts/UsedBookAdd.html', {'form':form,'errors':errors})

class ListExposure(generic.ListView):
    model = Exposure
    template_name = 'csinla_posts/exposure_view.html'
    context_object_name = 'exposure_list'

    def get(self, request):
        # exposure_list = Exposure.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
        # exposure_list = Exposure.objects.get(post_ptr_id=646)
        exposure_list = Exposure.objects.all().order_by('-is_top', '-active')
        key = request.GET.get('keyword', '')
        if key:
            exposure_list = exposure_list.filter(Q(title__icontains=key) | Q(content__icontains=key))
        numbs = len(exposure_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(exposure_list,17,request=request)
        exposure_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'exposure_list': exposure_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        exposure_list = UsedBook.objects.filter(expire_date__gte = timezone.now()).order_by('-is_top', '-active')
        cds=self.request.POST.dict()
        numbs = len(exposure_list)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(exposure_list,17,request=request)
        exposure_list = p.page(page)
        numb =  int(numbs/17)
        context={
            'numb':numb,
            'exposure_list': exposure_list,
            'filter_dic':cds,
        }
        return render(request, self.template_name, context)
    def get_context_data(self,  **kwargs):
        # call super class
        context = super(ListExposure, self).get_context_data(**kwargs)
        # context['cars'] = []
        return context

@login_required
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
                        picture=Rentpicture(post_id=exposure.id, image=file_image)
                        picture.save()
            data={
                'code':0,
                'msg':u'成功',
                'post_id':exposure.id,
            }
            return json_response(data)
        else:
            data={
                'code':1,
                'msg':ErrorDic2str(form.errors),
            }
            return json_response(data)

    else:
        form = CreateExposureForm()
    return render(request, 'csinla_posts/exposure_add.html', {'form':form})

class ViewPost(generic.DetailView):
    model = Rent
    template_name = 'csinla_posts/14.houseRenting_detail.html'
    context_object_name = 'rent'

    def get_context_data(self, **kwargs):
    #     # call super class
        context = super(ViewPost, self).get_context_data(**kwargs)

    #     # self.rent = Rent.objects.get(post_id=self.kwargs['pk'])
    #     self.post = Rent.objects.get(post_id=5)
    #     module = Module.objects.get(id=self.rent.post.belong_to.id)
    #     parent_module = Module.objects.get(id=module.belong_to.id)
    #     context['self_mod'] = module
    #     context['parent_module'] = parent_module
        picture = Rentpicture.objects.filter(rent__id=self.kwargs['pk'])
        context['pictures'] = picture
        return context

@cache_control(must_revalidate=True, max_age=7200)
def view_posts(request, posts_id):
    rent_template_name = 'csinla_posts/14.houseRenting_detail.html'
    car_template_name = 'csinla_posts/Car_detail.html'
    shared_template_name = 'csinla_posts/Rommate_detail.html'
    used_goods_template_name='csinla_posts/secondhandgoodsdetail.html'
    used_book_template_name='csinla_posts/Usedbook_detail.html'
    exposure_template_name='csinla_posts/exposure_detail.html'
    entire_rent_template_name = 'csinla_posts/entire_rent_detail.html'

    posts = Post.objects.get(id=posts_id)

    view_message=request.GET.get('view_message','')
    if view_message:
        view_message=int(view_message)
        message=posts.postmessage_set.get(id=view_message)
        if not message.has_read:
            message.has_read=True
            message.save()
        return HttpResponseRedirect('/posts/%s/#m%s' % (posts.id,message.id))
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
    is_collect=False
    try:
        PostMessage.objects.get(message_type='COLLECT',post=posts,creator=request.user,is_valid=True)
        is_collect=True
    except:
        pass
    if picture.exists():
            # picurl = 'http://www.csinla.com' + picture[0].image.url
            picurl = picture[0].image.url
    else:
            picurl = 'http://www.csinla.com/media/wxlogo.jpg'
    if posts.belong_to == u"个人转租":
        try:
            war = Warnings.objects.get(posts_type=u"个人转租")
            war = war.content
        except:
            war = u"未设置"
        context={
            'posts': posts.rent,
            'pictures': picture,
            'war': war,
            'is_collect':is_collect,
            'is_favor': is_favor,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'租房详情A%s' % i
            wap_belong_to=u'租房详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })
        return render(request, rent_template_name, context)
    elif posts.belong_to == u"二手车":
        try:
            war = Warnings.objects.get(posts_type=u"二手车")
            war = war.content
        except:
            war = ""
        context={
            'posts': posts.car,
            'pictures': picture,
            'war': war,
            'is_collect':is_collect,
            'is_favor': is_favor,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'二手车详情A%s' % i
            wap_belong_to=u'二手车详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, car_template_name, context)
    elif posts.belong_to == u"合租":
        try:
            war = Warnings.objects.get(posts_type=u"合租")
            war = war.content
        except:
            war = u"未设置"
        context={
            'posts': posts.rent2,
            'pictures': picture,
            'war': war,
            'is_collect':is_collect,
            'is_favor': is_favor,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'合租详情A%s' % i
            wap_belong_to=u'合租详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, shared_template_name, context)
    elif posts.belong_to == u"二手商品":
        try:
            war = Warnings.objects.get(posts_type=u"二手商品")
            war = war.content
        except:
            war = u"未设置"
        context={
            'posts': posts.usedgoods,
            'pictures': picture,
            'war': war,
            'is_collect':is_collect ,
            'is_favor': is_favor,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'二手商品详情A%s' % i
            wap_belong_to=u'二手商品详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, used_goods_template_name,context )
    elif posts.belong_to == u"二手书":
        try:
            war = Warnings.objects.get(posts_type=u"二手书")
            war = war.content
        except:
            war = u"未设置"
        context={
            'posts': posts.usedbook,
            'pictures': picture,
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'二手书详情A%s' % i
            wap_belong_to=u'二手书详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, used_book_template_name, context)
    elif posts.belong_to == u"朋友圈":
        try:
            war = Warnings.objects.get(posts_type=u"朋友圈")
            war = war.content
        except:
            war = u"未设置"
        context={
            'posts': posts.exposure,
            'pictures': picture,
            'war': war,
            'is_favor': is_favor,
            'is_collect':is_collect,
            'picurl': picurl,
            'reply_message_list':reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'朋友圈详情A%s' % i
            wap_belong_to=u'朋友圈详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, exposure_template_name,context)
    elif posts.belong_to == u'整租':
        try:
            war = Warnings.objects.get(posts_type=u"整租")
            war = war.content
        except:
            war = u"未设置"
        context = {
            'posts': posts.entirerent,
            'pictures': picture,
            'war': war,
            'is_collect': is_collect,
            'is_favor': is_favor,
            'picurl': picurl,
            'reply_message_list': reply_message_list,
        }
        for i in range(1,8):
            web_belong_to=u'整租详情A%s' % i
            wap_belong_to=u'整租详情B%s' % i

            if Advertising.objects.filter(belong_to=web_belong_to ).exists():
                web_key='ad_A%s' % i
                context.update({
                    web_key:Advertising.objects.filter(belong_to=web_belong_to )[0]
                })
            if Advertising.objects.filter(belong_to=wap_belong_to ).exists():
                wap_key='ad_B%s' % i
                context.update({
                    wap_key:Advertising.objects.filter(belong_to=wap_belong_to )[0]
                })

        return render(request, entire_rent_template_name, context)

def post_delete(request,pid):
    if not request.user.is_authenticated():
        return HttpResponse(u'请先登录')
    if not request.user.is_superuser:
        return HttpResponse(u'非管理员用户无法直接删除帖子')
    post=Post.objects.get(id=pid)
    post.delete()
    return HttpResponseRedirect('/')


@login_required
def type_select(request):
    return render(request,'csinla_posts/EditPosts.html')

@login_required
@require_POST
def new_posts(request):
    types = request.POST.get("checkbox")
    if types == None:
        return render(request, 'csinla_posts/EditPosts.html')
    types = types.encode('utf-8')
    if types == "个人转租":
        return HttpResponseRedirect(reverse('posts:add', args=('rent',)))
    elif types == "求室友合租":
        return HttpResponseRedirect(reverse('posts:add', args=('shared',)))
    elif types == "二手车":
        return HttpResponseRedirect(reverse('posts:add', args=('car',)))
    elif types == "我要买车，通知我":
        return HttpResponseRedirect(reverse('posts:buycar'))
    elif types == "二手商品":
        return HttpResponseRedirect('/posts/usedgoods/add')
    elif types == "二手书":
        return HttpResponseRedirect('/posts/usedbook/add')
    elif types == "二手书":
        return HttpResponseRedirect('/posts/usedbook/add')
    elif types == "万能的朋友圈":
        return HttpResponseRedirect('/posts/exposure/add')
    if types == "整套出租":
        return HttpResponseRedirect(reverse('posts:add', args=('entire_rent',)))
    return HttpResponse('"%s"功能开发中' % types)

def posts_create(request,types):
    shared_template_name = 'csinla_posts/RoommatetoShare.html'
    rent_template_name = 'csinla_posts/EditNewPosts.html'
    car_template_name = 'csinla_posts/BuyCar.html'
    entire_rent_template_name = 'csinla_posts/entire_rent.html'

    if request.method=='POST':
        if types == 'rent':
            belong = '个人转租'
            postsForm = CreateRentForm(request.POST)
            #pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif types == 'shared':
            belong = '合租'
            postsForm = CreateShareForm(request.POST)
            pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif types == 'car':
            belong = '二手车'
            postsForm = CreateCarForm(request.POST)
            pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors)
                }
                return json_response(data)
        elif types == 'entire_rent':
            # 如果发帖类型为整租
            belong = '整租'
            postsForm = CreateEntireRentForm(request.POST)
            pictureForm = CreatePictureForm(request.POST, request.FILES)
            if not postsForm.is_valid():
                data = {
                    'code': 1,
                    'msg': ErrorDic2str(postsForm.errors)
                }
                return json_response(data)

        posts = postsForm.save(commit=False)
        posts.belong_to = belong
        posts.author = request.user  
        posts.content = posts.content
        posts.save()
        # user.save()
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for im in images:
                picture = Rentpicture(post_id=posts.id, image=im)
                picture.save()
        flex_base64_data_list_str = request.POST.get('image')
        if flex_base64_data_list_str:
            for flex_base64_data in flex_base64_data_list_str.split('$$$$$'):
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
                    picture=Rentpicture(post_id=posts.id, image=file_image)
                    picture.save()
        # user = request.user
        # if user.phone == '' or user.phone == None:
        #     user.phone = posts.phone
        #     user.save()
        # if user.weixin == '' or user.weixin == None:
        #     user.weixin = posts.weixin
        #     user.save()
        data={
            'code':0,
            'msg':u'成功',
            'post_id':posts.id,
        }
        return json_response(data)
        # return redirect('posts:complete_post', pk=posts.id)
        #return HttpResponseRedirect(reverse('posts:complete_post', args=(posts.id,)))

        #return HttpResponse('提交失败')
    else:
        if types == 'rent':
            return render(request, rent_template_name)
        elif types == 'shared':
            return render(request, shared_template_name)
        elif types == 'car':
            return render(request, car_template_name)
        elif types == 'entire_rent':
            return render(request, entire_rent_template_name)


class CreatePosts2(generic.View):
    template_name = 'csinla_posts/ceshi.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            i = 0
            for im in images:
                i = i+ 1
        return HttpResponse(i)

class CarInspect(generic.View):
    template_name = 'csinla_posts/CarInspection.html'

    def get(self, request,ciid):
        inspect = CarInspection.objects.get(id=ciid)
        form = InspectForm(instance=inspect)
        return render(request, self.template_name, {'form': form, 'pic': inspect.image})
    def post(self, request,ciid):
        form = InspectForm(request.POST, instance=self.inspect)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})

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
            return redirect('home')
        context={
            'form':form,
        }
        return render(request, template_name, context)
    else:
        form = CustomizedCarForm()
        context={
            'form':form,
        }
        return render(request, template_name, context)


class CreateUsed(generic.View):
    template_name = 'csinla_posts/Used.html'

    def get(self, request):
        form = UsedForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = UsedForm(request.POST)
        if form.is_valid():
            used = form.save()
            return render(request, 'csinla_posts/Used1.html', {'form':form})
        else:
            return render(request, self.template_name, {'form':used})


#class CreateSuccess(generic.View):
#    template_name = 'csinla_posts/CarMessage.html'
#
#    def get(self, request):
#        return render(request, self.template_name)
        

def success_notice(request,pk=''):
    return render(request, 'csinla_posts/EditPostsSuccess.html', {'id': pk})
    


class DeletePost(generic.DeleteView):
    model = Post
    context_object_name = 'my_post'
    success_url = reverse_lazy('accounts:myPosts')




class ChangePost(LoginRequiredMixin,generic.View):
    shared_template_name = 'csinla_posts/RoommatetoShare.html'
    rent_template_name = 'csinla_posts/EditNewPosts.html'
    car_template_name = 'csinla_posts/BuyCar.html'
    usedgoods_template_name='csinla_posts/UsedGoodsAdd.html'
    userbook_template_name='csinla_posts/UsedBookAdd.html'
    exposure_template_name='csinla_posts/exposure_add.html'
    entire_rent_template_name = 'csinla_posts/entire_rent.html'

    def get(self, request, posts_id):
        posts = Post.objects.get(id=posts_id)
        picture = Rentpicture.objects.filter(post__id=posts_id)
        if posts.belong_to == u"个人转租":
            rentForm = CreateRentForm(instance=posts.rent)
            return render(request, self.rent_template_name, {'rentForm': rentForm, 'pictures': picture})
        elif posts.belong_to == u"合租":
            sharedForm = CreateShareForm(instance=posts.rent2)
            return render(request, self.shared_template_name, {'sharedForm': sharedForm, 'pictures': picture})
        elif posts.belong_to == u"二手车":
            carForm = CreateCarForm(instance=posts.car)
            return render(request, self.car_template_name, {'carForm': carForm, 'pictures': picture})
        elif posts.belong_to == u"二手商品":
            usedgoodsForm = CreateUsedGoodsForm(instance=posts.usedgoods)
            usedgoods=posts.usedgoods
            tag_list=UsedGoodsTag.objects.all()
            context={
                'form': usedgoodsForm,
                'pictures': picture,
                'select_tag_list':usedgoods.tags.all(),
                'tag_list':tag_list,
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
                        'item_value':usedgoodsitem,
                    })
                    i+=1
                context.update({
                    'item_list':item_list,    
                })
            return render(request, self.usedgoods_template_name, context)
        elif posts.belong_to == u"二手书":
            usedbookForm = CreateUsedBookForm(instance=posts.usedbook)
            usedbook=posts.usedbook
            context={
                'form': usedbookForm,
                'pictures': picture
            }
            item_count=usedbook.usedbookitem_set.all().count()
            if item_count>0:
                context.update({
                    'first_item':usedbook.usedbookitem_set.all().order_by('id')[0],    
                })
            if item_count>1:
                i=1
                item_list=[]
                for usedbookitem in usedbook.usedbookitem_set.all().order_by('id')[1:]:
                    item_list.append({
                        'item_index':i,
                        'item_value':usedbookitem,    
                    })
                    i+=1
                context.update({
                    'item_list':item_list,    
                })
            return render(request, self.userbook_template_name, context)
        elif posts.belong_to == u"朋友圈":
            form = CreateExposureForm(instance=posts.exposure)
            return render(request, self.exposure_template_name, {'form': form, 'pictures': picture})
        elif posts.belong_to == u'整租':
            rentForm = CreateEntireRentForm(instance=posts.entirerent)
            return render(request, self.entire_rent_template_name, {'rentForm': rentForm, 'pictures': picture})

    def post(self, request, posts_id):
        picture = Rentpicture.objects.filter(post__id=posts_id)
        picture.delete()
        posts = Post.objects.get(id=posts_id)
        if posts.belong_to == u"个人转租":
            postsForm = CreateRentForm(request.POST, instance=posts.rent)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif posts.belong_to == u'整租':
            postsForm = CreateEntireRentForm(request.POST,instance=posts.entirerent)
            if not postsForm.is_valid():
                data = {
                    'code': 1,
                    'msg': ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif posts.belong_to == u"合租":
            postsForm = CreateShareForm(request.POST, instance=posts.rent2)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif posts.belong_to == u"二手车":
            postsForm = CreateCarForm(request.POST, instance=posts.car)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
                }
                return json_response(data)
        elif posts.belong_to==u'二手商品':
            postsForm = CreateUsedGoodsForm(request.POST, instance=posts.usedgoods)
            if not postsForm.is_valid():
                data={
                    'code':1,
                    'msg':ErrorDic2str(postsForm.errors),
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
                    'msg':ErrorDic2str(postsForm.errors),
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
                return render(request, self.exposure_template_name, {'form': postsForm})
        posts = postsForm.save(commit=False)
        if posts.belong_to==u'二手商品':
            postsForm.save_m2m()
        if 'image' in request.FILES:
            Rentpicture.objects.filter(post__id=posts_id).delete()
            images = request.FILES.getlist('image')
            for im in images:
                picture = Rentpicture(post_id=posts.id, image=im)
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
                    picture=Rentpicture(post_id=posts.id, image=file_image)
                    picture.save()
        posts.author = request.user
        posts.active = timezone.now()
        posts.save()
        data={
            'code':0,
            'msg':u'成功',
            'post_id':posts.id,
        }
        return json_response(data)

def set_top(request, posts_id):
    posts = Post.objects.get(id=posts_id)
    if posts.is_top:
        posts.is_top = False
    else:
        posts.is_top = True
    posts.save()
    return HttpResponseRedirect(reverse('posts:detail', args=(posts_id,)))


def postmessage_leave(request):
    if request.method=='POST':
        user = request.user
        if not request.user.is_authenticated(): 
            data={
                'code':2,
                'msg':u'请先登录',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
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
                flex_base64_data_list_str = request.POST.get('content_image')
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
                return HttpResponse(json.dumps(data), content_type='application/json')
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
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except PostMessage.DoesNotExist:
                    PostMessage.objects.create(message_type='COLLECT',creator=user,post=post)
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
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
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except PostMessage.DoesNotExist:
                    pass
                data={
                    'code':1,
                    'msg':u'您尚未收藏',
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
            elif operate_type=='collect_read':
                pmid=int(request.POST.get('pmid',0))
                if not pmid:
                    data={
                        'code':1,
                        'msg':u'参数缺失',
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
                postmessage=PostMessage.objects.get(id=pmid)
                if postmessage.message_type=='COLLECT' and postmessage.is_valid:
                    postmessage.has_read=True
                    postmessage.save()
                    data={
                        'code':0,
                        'msg':u'成功',
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data={
                        'code':1,
                        'msg':u'当前消息并非有效的收藏信息',
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
            elif operate_type=='delete':
                if not user.is_superuser:
                    data={
                        'code':1,
                        'msg':u'只有超级用户才可以删除评论',
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
                pmid=int(request.POST.get('pmid',0))
                if not pmid:
                    data={
                        'code':1,
                        'msg':u'参数缺失',
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
                postmessage=PostMessage.objects.get(id=pmid)
                postmessage.delete()
                data={
                    'code':0,
                    'msg':u'成功',
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data={
                    'code':1,
                    'msg':u'无效操作',
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

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
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse(u'当前操作不接受get请求')
