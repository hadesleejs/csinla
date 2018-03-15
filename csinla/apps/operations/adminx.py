# coding=utf-8
# author=lijiaoshou
# date='2017/7/18 18:00'
import xadmin
from .models import *


class AdvertisingAdmin(object):
	list_display = ['belong_to', 'text', 'url', 'img']
	search_fields = ['belong_to', 'text', 'url', 'img']
	list_filter = ['belong_to', 'text', 'url', 'img']


xadmin.site.register(Warnings)
xadmin.site.register(Protocol)
xadmin.site.register(Advertising,AdvertisingAdmin)
