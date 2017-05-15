#coding:utf-8
from django.contrib import admin
from .models import Authority,User
# Register your models here.
import sys
reload(sys)
sys.setdefaultencoding('utf8')


####注册权限信息
class  AuthorityAdmin(admin.ModelAdmin):
    fieldsets = [('Authority information', {'fields': ('authorityID', 'authorityname')}), ]
    list_display = ('authorityID', 'authorityname')

##注册用户信息
class UserAdmin(admin.ModelAdmin):
    fieldsets = [('user information',{'fields':('username','password','authorityID')}),]
    list_display = ('username','password','authorityID')
    ordering = ('authorityID',)

# ###模块表
# class ModulesAdmin(admin.ModelAdmin):
#     fieldsets = [('Modules information', {'fields': ('module_ID', 'module_Name','module_qq ')}), ]
#     list_display = ('module_ID', 'module_Name','module_qq ')
# ###表单汇总表
# class TablesAdmin(admin.ModelAdmin):
#     fieldsets = [('Tables information', {'fields': ('module_ID', 'table_ID','table_Name','notes')}), ]
#     list_display = ('module_ID', 'table_ID','table_Name','notes')
# ###表单标签表
# class LabelsAdmin(admin.ModelAdmin):
#     fieldsets = [('Labels information', {'fields': ('table_ID', 'label_ID','label_Name')}), ]
#     list_display = ('table_ID', 'label_ID','label_Name')
# ###全平台每日基础指标汇总表
# class Platform_summary_dayAdmin(admin.ModelAdmin):
#     fieldsets = [('Platform_summary_day information', {'fields': ('date','table_ID', 'label_ID','label_Value')}), ]
#     list_display = ('date','table_ID', 'label_ID','label_Value')
#
#
#
#
#
admin.site.register(Authority, AuthorityAdmin)
admin.site.register(User, UserAdmin)
# admin.site.register(Modules,ModulesAdmin)
# admin.site.register(Tables,TablesAdmin)
# admin.site.register(Labels,LabelsAdmin)
# admin.site.register(Platform_summary_day,Platform_summary_dayAdmin)