
"""MYCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path

from supercrm.views import auth,customer

urlpatterns = [


#首页展示
    path('home/', auth.home,name='home'),
#所有客户信息展示
    path('customers/', customer.CustomerView.as_view(),name='customers'),
#个人客户信息展示
    path('mycustomers/', customer.CustomerView.as_view(),name='mycustomers'),
#添加客户
    path('add_customer/', customer.add_edit_customer,name='add_customer'),
#修改客户
    re_path('edit_customer/(\d+)/',customer.add_edit_customer,name='edit_customer'),
#跟进记录
    path('consult_record/',customer.ConsultRecordView.as_view(),name='consult_record'),
    path('add_consult_record/',customer.AddConsultView.as_view(),name='add_consult_record'),
    re_path('edit_consult_record/(\d+)/',customer.AddConsultView.as_view(),name='edit_consult_record'),
#购买记录
    path('enrollment/',customer.EnrollmentsView.as_view(),name='enrollment'),
    path('enroll_add/',customer.AddEditEnrollView.as_view(),name='enroll_add'),
    re_path('enroll_edit/(\d+)/',customer.AddEditEnrollView.as_view(),name='enroll_edit'),
#客户反馈记录
    path('score/', customer.ScoreView.as_view(), name='score'),
    path('score_add/', customer.AddEditScoreView.as_view(), name='score_add'),
    re_path('score_edit/(\d+)/', customer.AddEditScoreView.as_view(), name='score_edit'),


#产品情况展示：
    path('situation/', customer.SituationView.as_view(), name='situation'),
    # path('score_add/', customer.AddEditScoreView.as_view(), name='score_add'),
    # re_path('score_edit/(\d+)/', customer.AddEditScoreView.as_view(), name='score_edit'),
    re_path('score_more/(\d+)/', customer.MoreScoreView.as_view(), name='score_more'),

]
