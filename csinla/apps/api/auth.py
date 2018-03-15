# coding=utf-8
# author=lijiaoshou
# date='2017/9/2 17:27'
import datetime
from csinla_accounts.models import Profile
import exceptions
from rest_framework.authentication import BaseAuthentication

def user_to_payload(user):
    exp = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 7)
    return {
        'user_id': str(user.id),
        'exp': exp
    }


def payload_to_user(payload):
    if not payload:
        return None
    user_id = payload.get('user_id')
    user = Profile.objects.get(user_id)
    return user

class WechatUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not request.jwt_user:
            msg = u'请先授权'
            raise exceptions.AuthenticationFailed(msg)
        return (request.jwt_user, request.jwt_user.uuid)

