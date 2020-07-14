


# Create your views here.

from django.shortcuts import render, redirect


from supercrm import models
from supercrm.utils.hashlib_func import mymd5
from supercrm.myforms import RegisterForm

from rbac.serve.permissions import permission_in
# 首页展示
def home(request):
    #展示页面
    return render(request, 'home.html')


# 用户登录
def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=mymd5(password)).first()
        # 基于form校验
        if user_obj:
            #使用rbac中的权限功能
            permission_in(request,user_obj)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})


# 用户注册
def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})
    elif request.method == 'POST':
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            # 密码md5加密
            password = register_form_obj.cleaned_data.pop('password')
            password = mymd5(password)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(**register_form_obj.cleaned_data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})
