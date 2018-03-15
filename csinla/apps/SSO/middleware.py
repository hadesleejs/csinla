# coding=utf-8

from django.utils.functional import SimpleLazyObject
from .models import *

import logging
logger = logging.getLogger(__name__)

def get_user(request):
    from django.contrib.auth.models import AnonymousUser

    if not hasattr(request, '_cached_user') or not request._cached_user:
            #request._cached_user = auth.get_user(request)
        if request.POST and 'ticket' in request.POST:
            ticket_str = request.POST.get('ticket')
        elif request.GET and 'ticket' in request.GET:
            ticket_str = request.GET.get('ticket','')
        else:
            ticket_str = request.COOKIES.get('ticket', '')
        open_id=request.COOKIES.get('open_id','')
        if not open_id:
            open_id=request.GET.get('open_id','')
            request.COOKIES['open_id']=open_id
        #logger.info(ticket_str)
        try:
            t = Ticket.objects.validate_ticket(ticket_str)
            print t
            user = t.user
            #logger.info(user)
        except InvalidTicket as e:
            #logger.info('can not get ticket')
            logger.info(e)
            user = AnonymousUser()
        except InvalidRequest as e:
            #logger.info(e)
            user = AnonymousUser()
        except Exception as e:
            print e
            user=AnonymousUser()
    request._cached_user = user
    return request._cached_user

class TicketAuthenticationMiddleware(object):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        path = request.path_info.lstrip('/')
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):    
            ip =    request.META['HTTP_X_FORWARDED_FOR']    
        else:    
            ip = request.META['REMOTE_ADDR']
        if request.user.is_authenticated():
            ViewItem.objects.create(creator=request.user,link=path,ip=ip)
        else:
            ViewItem.objects.create(link=path,ip=ip)
        # if not request.user.is_authenticated():
        #   temp_ticket_str = request.COOKIES.get('temp_ticket', '')
        #   if temp_ticket_str:
        #       tempticket=TempTicket.objects.get(temp_ticket=temp_ticket_str)
        #       if tempticket.ticket:
        #           request.COOKIES['ticket']=tempticket.ticket.ticket
        #           request._cached_user = None
        #           request.user = SimpleLazyObject(lambda: get_user(request))


from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

SSL = 'SSL'

class SSLRedirect:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False

        if not secure == self._is_secure(request):
            return self._redirect(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
            return True

        #Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        #newurl = "%s://%s%s" % (protocol,get_host(request),request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
                raise RuntimeError, \
        """Django can't perform a SSL redirect while maintaining POST data.
             Please structure your views so that redirects only occur during GETs."""

        #return HttpResponsePermanentRedirect(newurl)

