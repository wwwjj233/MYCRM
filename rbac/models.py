from django.db import models

# Create your models here.
#权限相关表



class Role(models.Model):
    name = models.CharField(max_length=32)
    permissions=models.ManyToManyField(to='Permission')

    def __str__(self):
        return self.name

class Menu(models.Model):
    # 一级菜单
    title = models.CharField(max_length=32)
    icon = models.CharField(max_length=32, null=True, blank=True)
    weight=models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Permission(models.Model):
    url = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    menus=models.ForeignKey('Menu',null=True,blank=True,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)



    def __str__(self):
        return self.url + '----' + self.title