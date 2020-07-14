# Create your views here.
import copy
import datetime

from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from django.shortcuts import render, redirect ,HttpResponse
from django.db import transaction
from django.forms.models import modelformset_factory

from MYCRM import settings
from supercrm import models
from supercrm.utils.page import MyPagenation
from supercrm.myforms import CustomerForm,ConsultRecordForm,EnrollForm,ScoreForm,MoreScoreModelForm











# 客户信息 包括分页/搜索
class CustomerView(View):
    '''
    用户页面
    '''
    def get(self,request):
        current_request_path = request.path
        if current_request_path == reverse('customers'):
            tag='1'
            customer_list = models.Customers.objects.filter(consultant__isnull=True)
        else:
            tag='2'
            user_obj = request.user_obj
            customer_list = models.Customers.objects.filter(consultant=user_obj)

        # get_data=request.GET.urlencode()#提交过来的搜索条件
        # get_data=request.GET#提交过来的搜索条件 是一个Querydict字典对象,不允许直接修改
        get_data = copy.copy(request.GET)
        page_num = request.GET.get('page')
        search_field = str(request.GET.get('search_field')) + '__contains'.strip()  # 查询关键字
        kw = request.GET.get('kw')  # 关键字内容

        if kw:
            kw.strip()
            # 设置多个条件之间的关系
            # q_obj=Q()
            # q_obj.connector='or'
            # q_obj.children.append((search_field,kw))
            customer_list = customer_list.filter(**{search_field: kw})
        else:
            customer_list = customer_list
        base_url = request.path  # 访问路径

        customer_count = customer_list.count()
        per_page_num = settings.PER_PAGE_NUM  # 每页显示的信息
        page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数量
        page_obj = MyPagenation(page_num, customer_count, base_url, get_data, per_page_num, page_num_show, )
        page_html = page_obj.page_hmtl()
        customer_obj = customer_list.reverse()[
                       page_obj.start_data_num:page_obj.end_data_num
                       ]

        return render(request, 'infohtml/customers.html', {'customer_obj': customer_obj,
                                                           'page_html': page_html,
                                                           'tag':tag})

    def post(self,request):
        action=request.POST.get('action')
        cids=request.POST.getlist('cids')
        # if cids:
        if hasattr(self,action):
            ret=getattr(self,action)(request,cids)
            if ret:
                return ret
            return redirect(request.path)
        # else:
        #     return HttpResponse('未选择客户')

    #公转私
    '''
    存在一个bug，当两个用户同时操作的时候后操作的回抢走先操作的人的客户
    '''
    def reverse_gs(self,request,cids):
        with transaction.atomic():
            customers = models.Customers.objects.filter(pk__in=cids,consultant__isnull=True).select_for_update()
            #如果已经被选走，根据*consultant__isnull=True*条件查到的客户数量会少于选择的客户数量
        if customers.count()!=len(cids):
            return HttpResponse('手速不够被人抢走了')
        customers.update(consultant_id=request.session.get('user_id'))


    def reverse_sg(self, request, cids):
        customers = models.Customers.objects.filter(pk__in=cids)
        customers.update(consultant=None)


# 添加/修改用户信息
def add_edit_customer(request, cid=None):
    '''
    添加，编辑客户
    :param request:
    :param cid: 客户pk
    :return:
    '''
    title='编辑客户' if cid else '添加客户'
    customer_obj = models.Customers.objects.filter(pk=cid).first()
    if request.method == 'GET':
        customer_form=CustomerForm(instance=customer_obj)
        return render(request, 'infohtml/add_edit_customer.html', {'customer_form':customer_form, 'title':title})
    elif request.method=='POST':
        next_url=request.GET.get('next')
        print(next_url)
        #忘了没有next_url的时候跳转回原页面
        if not next_url:
            next_url=reverse('customers')
        customer_form = CustomerForm(request.POST,instance=customer_obj)
        if customer_form.is_valid():
            customer_form.save()
            return redirect(next_url)
        else:
            return render(request, 'infohtml/add_edit_customer.html', {'customer_form':customer_form, 'title':title})


# 客户跟进记录 没加搜索
class ConsultRecordView(View):

    def get(self,request):
        cid=request.GET.get('cid')
        if cid:
            #显示单个客户的详细客户跟进信息
            consult_list = models.ConsultRecord.objects.filter(consultant=request.user_obj,
                                                               customer_id=cid,
                                                               delete_status=False).order_by('date')
        else:
            consult_list=models.ConsultRecord.objects.filter(consultant=request.user_obj,
                                                             delete_status=False,
                                                             ).order_by('date')
        get_data = copy.copy(request.GET)
        page_num = request.GET.get('page')
        search_field = str(request.GET.get('search_field')) + '__contains'.strip()  # 查询关键字
        kw = request.GET.get('kw')  # 关键字内容

        if kw:
            kw.strip()
            # 设置多个条件之间的关系
            # q_obj=Q()
            # q_obj.connector='or'
            # q_obj.children.append((search_field,kw))
            consult_list = consult_list.filter(**{search_field: kw})
        else:
            consult_list = consult_list
        base_url = request.path  # 访问路径

        consult_count = consult_list.count()
        per_page_num = settings.PER_PAGE_NUM  # 每页显示的信息
        page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数量
        page_obj = MyPagenation(page_num, consult_count, base_url, get_data, per_page_num, page_num_show, )
        page_html = page_obj.page_hmtl()
        consult_list = consult_list.reverse()[
                       page_obj.start_data_num:page_obj.end_data_num
                       ]

        return render(request, 'infohtml/consultrecord.html', {'consult_list': consult_list,
                                                           'page_html': page_html,
                                                           })

# 添加/编辑跟进记录
class AddConsultView(APIView):

    def get(self,request,cid=None):
        title = '编辑跟进记录' if cid else '添加跟进记录'
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        consult_form = ConsultRecordForm(request,instance=consult_obj)
        return render(request, 'infohtml/add_edit_consult.html', {'consult_form': consult_form, 'title': title})

    def post(self,request,cid=None):
        print(request)
        print('-------------------------------------------------------')
        print(request.POST)
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        next_url = request.GET.get('next')
        if not next_url:
            next_url=reverse('consult_record')
        consult_form = ConsultRecordForm(request,request.POST,instance=consult_obj)
        if consult_form.is_valid():
            consult_form.save()
            print(datetime.datetime.now())
            models.ConsultRecord.objects.filter(pk=cid).update(date=datetime.datetime.now())
            return redirect(next_url)
        else:
            return render(request, 'infohtml/add_edit_consult.html', {'consult_form': consult_form})

# 购买记录 没加分页/搜索
class EnrollmentsView(View):

    def get(self,request):
        enrolls=models.Enrollment.objects.filter(customer__consultant=request.user_obj)
        return render(request, 'infohtml/enrollments.html', {'enrolls':enrolls})

# 添加/修改购买记录
class AddEditEnrollView(View):
    def get(self,request,cid=None):
        title = '编辑购买记录' if cid else '添加购买记录'
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        enroll_form = EnrollForm(request,instance=enroll_obj)
        return render(request, 'infohtml/add_edit_enroll.html', {'enroll_form': enroll_form, 'title': title})

    def post(self,request,cid=None):
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        next_url = request.GET.get('next')
        if not next_url:
            next_url=reverse('enrollment')
        enroll_form = EnrollForm(request,request.POST,instance=enroll_obj,)
        if enroll_form.is_valid():
            enroll_form.save()
            # print(datetime.datetime.now())
            # models.Enrollment.objects.filter(pk=cid).update(date=datetime.datetime.now())
            return redirect(next_url)
        else:
            return render(request, 'infohtml/add_edit_enroll.html', {'enroll_form': enroll_form})


# 客户反馈 没加分页/搜索
class ScoreView(View):

    def get(self,request):
        # scores=models.Score.objects.filter(customer__consultant=request.user_obj)
        scores=models.Score.objects.all()
        return render(request, 'infohtml/score.html', {'scores':scores})


    def post(self,request):
        action = request.POST.get('action')
        cids=request.POST.getlist('cids')
        if hasattr(self,action):
            getattr(self,action)(request,cids)
        return HttpResponse('ok')

    #批量生成客户反馈记录
    def bulk_create_srecore(self,request,cids):
        for cid in cids:
            course_obj=models.Score.objects.filter(pk=cid).first()
            id=course_obj.product.id
            customers=course_obj.product.customers_set.filter(status='buyed')
            print('>>>>>>>', customers)
            obj_list=[]
            for i in customers:
                # models.Score.objects.create(product_id=id,
                #                             customer=i,) 每生成一个需要操作一次数据库
                obj=models.Score(product_id=id,customer=i,)
                obj_list.append(obj)
            models.Score.objects.bulk_create(obj_list)

# 添加/修改客户反馈
class AddEditScoreView(View):
    #质量添加/查看客户反馈

    def get(self,request,cid=None):
        title = '编辑反馈记录' if cid else '添加反馈记录'
        score_obj = models.Score.objects.filter(pk=cid).first()
        score_form = ScoreForm(request,instance=score_obj)
        return render(request, 'infohtml/add_edit_score.html', {'score_form': score_form, 'title': title})

    def post(self,request,cid=None):

        score_obj = models.Score.objects.filter(pk=cid).first()
        next_url = request.GET.get('next')
        if not next_url:
            next_url=reverse('score')
        score_form = ScoreForm(request,request.POST,instance=score_obj,)
        if score_form.is_valid():
            score_form.save()
            # print(datetime.datetime.now())
            # models.Enrollment.objects.filter(pk=cid).update(date=datetime.datetime.now())
            return redirect(next_url)
        else:
            return render(request, 'infohtml/add_edit_score.html', {'score_form': score_form})


# 产品详情 没加分页/搜索
class SituationView(View):
    def get(self,request):
        situation=models.Productsituation.objects.all()
        return render(request, 'infohtml/situation.html', {'situation':situation})

#
#添加/修改产品详情

#产品详情————从概况跳转到对应产品的客户反馈
class MoreScoreView(View):
    def get(self,request,situation_id):
        situation_obj=models.Productsituation.objects.filter(id=situation_id).first()
        product_obj=situation_obj.re_product
        print(product_obj)
        queryset_obj=situation_obj.score_set.filter(product=product_obj)
        print(queryset_obj)
        formset_obj=modelformset_factory(model=models.Score,form=MoreScoreModelForm,extra=0)#默认底下多一行extra=1
        formset=formset_obj(queryset=queryset_obj)
        return render(request,'infohtml/score_more.html',{'formset':formset})

    def post(self,request,situation_id):
        situation_obj=models.Productsituation.objects.filter(id=situation_id).first()
        product_obj=situation_obj.re_product
        print(product_obj)
        queryset_obj=situation_obj.score_set.filter(product=product_obj)
        print(queryset_obj)
        formset_obj=modelformset_factory(model=models.Score,form=MoreScoreModelForm,extra=0)
        formset=formset_obj(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(request.path)
        else:
            return render(request,'infohtml/score_more.html',{'formset':formset})