# coding:utf-8
import json
import urllib
import datetime
import time

from django.utils import timezone
from urllib import urlencode

from csinla_accounts.models import Profile,WechatInfo,WechatOpenToken

def get_opentoken(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {
        'appid':'wx338fa9b6b1183c16',
        'secret' : 'ba2f5a2eff614e93d6707be889416bd9',
        'code':code,
        'grant_type':'authorization_code',
    }
    # 拉取access_token
    params = urlencode(params)
    f = urllib.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    if res:
        open_id=res['openid']
        unionid=res.get('unionid','')
        access_token=res['access_token']
        refresh_token=res['refresh_token']
        expires_in=int(res['expires_in'])
        scope_array=res['scope'].split(',')
        try:
            wechatinfo=WechatInfo.objects.get(open_id=open_id)
            user=wechatinfo.userinfo
            opentoken= WechatOpenToken.objects.get(account=user)
            opentoken.open_id=open_id
            opentoken.access_token=access_token
            opentoken.refresh_token=refresh_token
            opentoken.expire_time=int(time.time())+expires_in
            opentoken.save()
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
                user = Profile.objects.create_user(username='%s' % (res['nickname'].encode('iso8859-1').decode('utf-8')), password='wx_CSinLA', source='WECHAT')
                wechatinfo = WechatInfo()
                wechatinfo.open_id = res['openid']
                wechatinfo.nickname = res['nickname']
                wechatinfo.sex = res['sex']
                wechatinfo.headimgurl = res['headimgurl']
                wechatinfo.province = res['province']
                wechatinfo.city = res['city']
                wechatinfo.country = res['country']
                wechatinfo.save()
                return True
            else:
                return False
        # if 'snsapi_userinfo' in scope_array:
        return opentoken
    else:
        return None

def get_userinfo(opentoken):
    url = "https://api.weixin.qq.com/sns/userinfo"
    params = {
        'access_token':opentoken.access_token,
        'openid' : opentoken.open_id,  
    }
    params = urlencode(params)
    f = urllib.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    if res:
        try:
            wechatinfo=WechatInfo.objects.get(userinfo=opentoken.account)
        except WechatInfo.DoesNotExist:
            wechatinfo=WechatInfo(userinfo=opentoken.account)
        wechatinfo.open_id=res['openid']
        wechatinfo.nickname=res['nickname']
        wechatinfo.sex=res['sex']
        wechatinfo.headimgurl=res['headimgurl']
        wechatinfo.province=res['province']
        wechatinfo.city=res['city']
        wechatinfo.country=res['country']
        wechatinfo.save()
        return True
    else:
        return False
