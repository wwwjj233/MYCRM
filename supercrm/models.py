from django.db import models
from multiselectfield import MultiSelectField
from rbac.models import Role,Permission,Menu
# Create your models here.



#具体产品名称
product_choices = (('MT4414/MT4414TE', 'MT4414/MT4414TE'),
                  ('GL070/Gl070E', 'GL070/Gl070E'),
                  ('GL100/Gl100E', 'GL100/Gl100E'),
                  ('GH070/GH070E', 'GH070/GH070E'),
                  ('GH104/GH104E', 'GH104/GH104E'),
                  ('F080/F080E', 'F080/F080E'),
                  ('HMIothers', 'HMI的其他产品'),
                  ('others', 'HMI产品外的其他产品'),
                  )
#产品类型
product_type_choices = (('HMI', 'HMI',),
                      ('PLC', '可编程控制器'),
                      ('Electric', '步进电机'),
                      ('others', '其它'),)

#客户来源
source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('others', "其它"),)

#客户过去购买信息
customer_status_choices = (('buyed', "已购买"),
                         ('unbuyed', "未购买"),
                         ('buying', '商讨中'),)

#客户当前状态
seek_status_choices = (('A', '近期无购买计划'), ('B', '1个月内购买'), ('C', '2周内购买'), ('D', '1周内购买'),
                       ('E', '定金'), ('F', '全款'), ('G', '无效' ),)

#客户付款方式
pay_type_choices = (('deposit', "订金"),
                    ('tuition', "全款"),
                    ('transfer', "换新"),
                    ('refund', "退款"),)



score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)

product_status_choice=(
    ('perfect','完美'),
    ('good','良好'),
    ('soso','一般'),
    ('bad','差'),
    ('verybad','极差'),
)


class UserInfo(models.Model):
    """
    用户表：销售
    """
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    roles=models.ManyToManyField(to=Role)
    def __str__(self):
        return self.username


class Customers(models.Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    name = models.CharField('姓名', max_length=32,
                            help_text='请输入真实姓名')  # 可为空，有些人就不愿意给自己的真实姓名
    user_type = (('person', '个人'), ('company', '公司'))  #
    customer_type = models.CharField("用户类型", choices=user_type, max_length=16, default='person',null=True
                                     )  # 存的是male或者female，字符串
    phone = models.BigIntegerField('手机号', help_text='请确认手机号正确'
                                   ) #手机号改成字符串的，不然不好搜索
    qq = models.CharField(verbose_name='QQ', max_length=64, blank=True, null=True,)
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True) #requierd:False
    #birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name="转介绍自客户", blank=True, null=True,on_delete=models.CASCADE
                                       )  #self指的就是自己这个表，和下面写法是一样的效果
    course = MultiSelectField("咨询产品", choices=product_choices,null=True
                              ) #多选，并且存成一个列表的格式,通过modelform来用的时候，会成为一个多选框
    # course = models.CharField("咨询课程", choices=course_choices) #如果你不想用上面的多选功能，可以使用Charfield来存
    product_type = models.CharField("产品类型", max_length=64, choices=product_type_choices, default='HMI')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=customer_status_choices,
                              max_length=64,
                              default="unbuyed",
                              help_text="选择客户此时的状态") #help_text这种参数基本都是针对admin应用里面用的
    date = models.DateTimeField("咨询日期", auto_now_add=True
                                )
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True
                                         ) #考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True
                                 ) #销售自己大概记录一下自己下一次会什么时候跟进，也没啥用
    #用户表中存放的是自己公司的所有员工。
    consultant = models.ForeignKey('UserInfo', verbose_name="销售",
                                   related_name='customers', blank=True, null=True,on_delete=models.CASCADE )

    #一个客户可以买多个产品，所以是多对多。
    product_list = models.ManyToManyField('ProductList', verbose_name="购买的产品", blank=True)
    #admin中的显示
    class Meta:
        ordering=['id',]
        verbose_name='客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name+":"+str(self.phone)


    # def get_classlist(self):  #当我们通过self.get_classlist的时候，就拿到了所有的班级信息，前端显示的时候用
    #
    #     l=[]
    #     for cls in self.class_list.all():
    #         l.append(str(cls))
    #     return mark_safe(",".join(l)) #纯文本，不用mark_safe也可以昂


class Campuses(models.Model):
    """
    公司/部门表
    """
    name = models.CharField(verbose_name='公司/部门', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductList(models.Model):
    """
    产品表
    """
    course = models.CharField("产品名称", max_length=64, choices=product_choices)
    semester = models.CharField("类型",max_length=32) #7寸/10寸
    campuses = models.ForeignKey('Campuses', verbose_name="部门",on_delete=models.CASCADE)
    price = models.IntegerField("价格", default=1000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开售日期")
    end_date = models.DateField("停产日期", blank=True, null=True) #不一定什么时候结业，哈哈，所以可为空

    #contract = models.ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True,on_delete=models.CASCADE)
    saler = models.ManyToManyField('UserInfo', verbose_name="对应销售",) #对了，还有一点，如果你用的django2版本的，那么外键字段都需要自行写上on_delete=models.CASCADE
    # situation = models.ManyToManyField('Productsituation', verbose_name="产品情况",) #对了，还有一点，如果你用的django2版本的，那么外键字段都需要自行写上on_delete=models.CASCADE

    product_type = models.CharField(choices=product_type_choices, max_length=64, verbose_name='产品类型', blank=True,null=True)

    def __str__(self):
        return self.course+'(' +self.campuses.name +')'


    class Meta:
        unique_together = ("course", "semester", 'campuses')

    # def __str__(self):
    #     return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)


class ConsultRecord(models.Model):
    '''
    客户状态跟进表
    '''
    customer=models.ForeignKey('Customers',verbose_name='所咨询的客户',on_delete=models.CASCADE)
    note=models.TextField(verbose_name='跟进内容')
    status=models.CharField('跟进状态',max_length=16,choices=seek_status_choices,help_text='选择客户此时的状态')
    consultant=models.ForeignKey(to='UserInfo',verbose_name='跟进人',related_name='records',on_delete=models.CASCADE)
    date=models.DateTimeField('跟进日期',auto_now_add=True)
    delete_status=models.BooleanField('删除状态',default=False)

    def __str__(self):
        return str(self.customer)+'跟进人:' + str(self.consultant)


class Enrollment(models.Model):
    '''
    客户购买表
    '''
    why_us=models.TextField('为什么选择我们的产品',max_length=1024,default=None,blank=True,null=True)
    enrolled_date=models.DateTimeField('购买日期',auto_now_add=True)
    memo=models.TextField('备注',null=True,blank=True)
    delete_status=models.BooleanField('删除状态',default=False)
    contract_approved=models.BooleanField('已审核',help_text='盛和通过后开始生成合同',default=False)
    customer=models.ForeignKey('Customers',verbose_name='客户名称',on_delete=models.CASCADE)
    product=models.ForeignKey('ProductList',verbose_name='购买产品',on_delete=models.CASCADE,default=1)

class Score(models.Model):
    '''
    客户反馈表
    '''
    customer=models.ForeignKey('Customers',verbose_name='客户名称',on_delete=models.CASCADE)
    product=models.ForeignKey('ProductList',verbose_name='产品名称',on_delete=models.CASCADE)
    appraise=models.IntegerField('评价',choices=score_choices,null=True,blank=True,default=32)
    memo=models.TextField('备注/其他反馈',null=True,blank=True)
    situation= models.ManyToManyField('Productsituation', verbose_name="产品情况", blank=True)
    date = models.DateTimeField('反馈日期', auto_now_add=True)

class Productsituation(models.Model):
    '''
    #产品情况表
    '''

    re_product=models.ForeignKey('ProductList',verbose_name='产品名称',on_delete=models.CASCADE)
    campuses=models.ForeignKey('Campuses',verbose_name='部门归属',on_delete=models.CASCADE)
    status=models.CharField('产品情况',choices=product_status_choice,max_length=32)
    leader=models.ForeignKey('UserInfo',verbose_name='负责人',on_delete=models.CASCADE)
    date=models.DateTimeField('日期',auto_now_add=True)