from django.contrib import admin
from supercrm.models import (
    UserInfo,Customers,Campuses,ProductList,Enrollment,ConsultRecord,Score,Productsituation,Role,Permission,Menu
)
# Register your models here.



@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass
@admin.register(Customers)
class CustomerAdmin(admin.ModelAdmin):
    pass
@admin.register(Campuses)
class CampusesAdmin(admin.ModelAdmin):
    pass
@admin.register(ProductList)
class ClassListAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(ConsultRecord)
class ConsultRecordtAdmin(admin.ModelAdmin):
    pass
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass

@admin.register(Productsituation)
class ProductsituationAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id','title','url','menus']
    list_editable = ['menus']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass