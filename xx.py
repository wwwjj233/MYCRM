

#测试所需要用到的客户生成
import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MYCRM.settings')
    import django
    import random
    django.setup()
    from supercrm import models

    source_type = (('qq', "qq群"),
                   ('referral', "内部转介绍"),
                   ('website', "官方网站"),
                   ('baidu_ads', "百度推广"),
                   ('office_direct', "直接上门"),
                   ('WoM', "口碑"),
                   ('others', "其它"),)

    product_type_choices = (('HMI', 'HMI',),
                            ('PLC', '可编程控制器'),
                            ('Electric', '步进电机'),
                            ('others', '其它'),)

    enroll_status_choices = (('buyed', "已购买过"),
                             ('unbuyed', "未购买过"),
                             ('buying', '商讨中'),)

    obj_list = []
    for i in range(251):
        a=random.randint(1,9)
        b=random.randint(1,9)
        c=random.randint(1,9)
        d={
            'name':str('客户%s'%i),
            'phone':int('13%s3838%s5%s8'%(a,b,c)),
            'source':source_type[random.randint(0,6)][0],#客户来源
            'product_type':product_type_choices[random.randint(0,3)][0],#产品类型
            'status':enroll_status_choices[random.randint(0,2)][0],#客户状况
        }

        obj=models.Customers(**d)
        obj_list.append(obj)
    models.Customers.objects.bulk_create(obj_list)
