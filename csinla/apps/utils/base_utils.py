# coding:utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from csinla.settings import BEFORE_RANGE_NUM, AFTER_RANGE_NUM



def ErrorDic2str(dic):
    res_list = []
    for key in dic.keys():
        res_list.append('%s%s' % (key, dic[key].as_text()))

    return '\n'.join(res_list)

# 获得分页page
def get_page_range(page, _list,page_limit):
    paginator = Paginator(_list, page_limit)
    page = int(page)
    try:
        _list = paginator.page(page)
    except PageNotAnInteger:
        _list = paginator.page(1)
    except EmptyPage:
        _list = paginator.page(paginator.num_pages)
    if page >= AFTER_RANGE_NUM:
        page_range = list(paginator.page_range)[
                     page - AFTER_RANGE_NUM:page + BEFORE_RANGE_NUM]
    else:
        page_range = list(paginator.page_range)[0:page + BEFORE_RANGE_NUM]
    return page_range, _list