# _*_ encoding: utf-8 _*_
import threading
import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .models import UserFavorite, EmailPic, FavoriteNotice
from csinla_accounts.models import Profile, EmailVerifyRecord, Unread
from csinla_posts.models import Post, Rent, Car,PostHistory,PostMessage
from utils.email_send import send_util
# Create your views here.

def favorite_posts(request, posts_id):
    user = request.user
    fav = UserFavorite.objects.filter(user=user, fav_id=posts_id)
    posts = Post.objects.get(id=posts_id)
    try:
        pic = EmailPic.objects.all()[0]
    except:
        pic = ''
    if fav:
        pass
    else:
        fav = UserFavorite()
        fav.user = user
        fav.fav_id = posts_id
        if posts.is_notice:
            t = threading.Thread(target=send_util, args=(pic, posts.author.username, posts.belong_to, posts.title, posts.author.email, posts.id))
            t.start()
        #send_util(pic, user.username, posts.belong_to, posts.title, posts.author.email, posts.id)
        fav.save()
    return HttpResponseRedirect(reverse('posts:detail', args=(posts_id,)))


def delete_posts(request, posts_id):
    user = request.user
    UserFavorite.objects.filter(user=user, fav_id=posts_id).delete()
    return redirect("accounts:myFavorites")


def list_favorite(request):
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
    paginator = Paginator(favorites, 20)

    page = request.GET.get('page')
    try:
        my_favorite = paginator.page(page)
    except PageNotAnInteger:
        my_favorite = paginator.page(1)
    except EmptyPage:
        my_favorite = paginator.page(paginator.num_pages)
    # print collect_list
    return render(request,'csinla_posts/MyCollect.html',{'my_collect': my_favorite, 'num': num})


def off_posts(request, posts_id, code):
    records = EmailVerifyRecord.objects.filter(send_type='off_posts', code=code)
    if records:
        posts = Post.objects.get(id=posts_id)
        posts.expire_date = datetime.date.today() - datetime.timedelta(seconds=1)
        posts.save()
        PostHistory.objects.create(post=posts,operator=posts.author,remark=u'用户【%s】下架本帖子，本帖过期' % posts.author)
        request.session['old_url'] = '/accounts/myinfo/'
        # return redirect("accounts:myInfo")
        return render(request,'ok.html')

    else:
        return HttpResponse('认证失败')


def stop_posts(request, posts_id, code):
    records = EmailVerifyRecord.objects.filter(send_type='off_posts', code=code)
    if records:
        posts = Post.objects.get(id=posts_id)
        posts.is_notice = False
        posts.save()
        PostHistory.objects.create(post=posts,operator=posts.author,remark=u'用户【%s】取消本帖的消息通知' % posts.author)
        request.session['old_url'] = '/accounts/myinfo/'
        return redirect("accounts:myInfo")
    else:
        return HttpResponse('认证失败')

def Read_notice(request):
    Unread.objects.filter(user_id=request.user.id).delete()
    FavoriteNotice.objects.filter(post_user_id=request.user.id).update(has_readed=True)
    return redirect("accounts:myInfo")
