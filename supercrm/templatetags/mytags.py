
from collections import OrderedDict

from django.urls import reverse
from django.http.request import QueryDict
from django.conf import settings
from django import template

import re
import json

register=template.Library()

@register.simple_tag()

def reverse_url(request):
    if request.path == reverse('customers'):
        return '公共客户信息'
    elif request.path == reverse('mycustomers'):
        return '我的客户信息'

@register.simple_tag()
def resole_url(request,url_name,customer_pk):
    #编辑完成后跳转回的路径
    next_url=request.get_full_path()
    #编辑过程的url
    reverse_url = reverse(url_name,args=(customer_pk,))
    #url编码
    q=QueryDict(mutable=True)
    q['next']=next_url
    next_url=q.urlencode()
    full_url=reverse_url + '?' + next_url
    return full_url


@register.inclusion_tag('menu.html')
def menu(request):
    menu_dict=request.session.get(settings.MENU_KEY)

    keys=sorted(menu_dict,key=lambda x : menu_dict[x]['weight'],reverse=True)
    order_dict=OrderedDict()
    for key in keys:
        order_dict[key]=menu_dict[key]



    path=request.path
    for key,value in order_dict.items():
        for i in value['children']:
            # if re.match(i['url'],path):
            if request.current_id == i['id']:
                value['class'] = 'active' # 下拉菜单选中效果
                i['class'] = 'active' # 二级菜单选中效果
                '''
                有个bug，客户管理的二级菜单权限都关联到了我的客户里去了。。。。
                '''
    return {'order_dict':order_dict}



@register.inclusion_tag('bread.html')
def bread(request):
    pass