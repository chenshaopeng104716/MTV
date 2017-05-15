# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import django.utils.timezone as timezone
from datetime import datetime
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# ###模块表
# class Modules(models.Model):
#     module_ID = models.CharField(max_length=3)
#     module_Name = models.CharField(max_length=255)
#     module_qq = models.CharField(max_length=10)
#     class Meta:
#         db_table = "display_Modules"
#     def __unicode__(self):
#         return str(self.module_Name)

###权限表
class Authority(models.Model):
    authorityID = models.CharField(max_length=50,primary_key=True)
    authorityname = models.CharField(max_length=100)
    class Meta:
        db_table = "MTV_Authority"
    def __unicode__(self):
        return str(self.authorityname)

###用户表
class User(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    password = models.CharField(max_length=50)
    authorityID = models.ForeignKey(Authority, on_delete=models.CASCADE)
    class Meta:
        db_table = "MTV_user"
    def __unicode__(self):
        return str(self.username)

# ###表单汇总表
# class Tables(models.Model):
#     module_ID = models.ForeignKey(Modules,on_delete=models.CASCADE)
#     table_ID = models.CharField(max_length=5)
#     table_Name = models.CharField(max_length=255)
#     notes = models.CharField(max_length=255)
#     class Meta:
#         db_table = "display_Tables"
#     def __unicode__(self):
#         return str(self.table_Name)
#
# ###表单标签表
# class Labels(models.Model):
#     table_ID = models.ForeignKey(Tables,on_delete=models.CASCADE)
#     label_ID = models.CharField(max_length=5)
#     label_Name = models.CharField(max_length=255)
#     class Meta:
#         db_table = "display_Lables"
#     def __unicode__(self):
#         return str(self.label_Name)
#
# ###全平台每日基础指标汇总表
# class Platform_summary_day(models.Model):
#     date = models.DateField(default=datetime.now().date())
#     table_ID = models.CharField(max_length=5,default='1')
#     label_ID = models.CharField(max_length=5)
#     label_Value = models.DecimalField(max_digits=15,decimal_places=1)
#     class Meta:
#         db_table = "display_Platform_summary_day"