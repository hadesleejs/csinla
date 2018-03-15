import json
import datetime
import time

from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponse

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(time.mktime(
                obj.timetuple()))
        if isinstance(obj, datetime.date):
            return int(time.mktime(obj.timetuple()))
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj,unicode):
            obj = obj.encode('utf-8')
            return obj
        if isinstance(obj,bool):
            return 1 if obj else 0
            
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.path
            except ValueError:
                return ''
        return json.JSONEncoder.default(self, obj)

def putNoneToString(x):
    if isinstance(x,dict):
        for key in x:
            x[key] = putNoneToString(x[key])
    if isinstance(x,list):
        for i in range(len(x)):
            x[i] = putNoneToString(x[i])
    if x is None:
        x = ''
    return x

def json_response(x):
    return HttpResponse(json.dumps(putNoneToString(x), cls=ComplexEncoder,separators=(',', ':'),ensure_ascii=True))