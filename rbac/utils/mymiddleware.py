
import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,HttpResponse
from django.urls import reverse
from supercrm import models


# class UserAuth(MiddlewareMixin):
#
#     def process_request(self,request):
#         #登录认证
#         white_list=[reverse('login'),reverse('register')]
#         if request.path in white_list:
#             return
#         user_id = request.session.get('user_id')
#         if user_id:
#             user_obj = models.UserInfo.objects.get(id=request.session.get('user_id'))
#             request.user_obj=user_obj
#             return
#         else:
#             return redirect('login')

class PermissionAuth(MiddlewareMixin):
    # 权限认证
    def process_request(self,request):
        #登录认证

        request.current_id=None # 当前访问的url权限对应的二级菜单权限的id

        request.bread_crumbs=[
            {
                'url': reverse('home'),
                'title': '首页'
            }
        ]
        # 登录，注册url白名单
        white_list=[reverse('login'),reverse('register'),'/admin/*']
        for i in white_list:
            ret = re.match(i,request.path)
            if ret:
                return

        user_id = request.session.get('user_id',None)
        if not user_id:
            return redirect('login')
        user_obj = models.UserInfo.objects.get(id=request.session.get('user_id'))
        request.user_obj = user_obj
        request_path = request.path
        #权限白名单
        permission_white__list = [reverse('home'),]
        if request_path in permission_white__list:
            return
        permission_list = request.session.get('permission_list')
        for reg in permission_list:
            if re.search(reg['permissions__url'], request_path):
                pid = reg.get('permissions__parent_id')
                if pid:
                    request.current_id = pid
                    # models.Permission.objects.filter(pk=pid).first() 代码简单，但是效率低。。。。

                    request.bread_crumbs.append({
                        'url':None,
                        'title':reg['permissions__title']
                    })
                    request.bread_crumbs.append({
                        'url':None,
                        'title':reg['permissions__title']
                    })
                else:
                    # 二级菜单面包屑数据
                    request.bread_crumbs.append({
                        'url':None,
                        'title':reg['permissions__title']
                    })
                    request.current_id = reg.get('permissions__pk')
                return
        else:
            return HttpResponse('没有权限')
