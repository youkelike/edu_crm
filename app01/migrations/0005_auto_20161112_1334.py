# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 05:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20161112_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_customer_list', '可以查看客户列表'), ('view_customer_info', '可以查看客户详细信息'), ('edit_own_customer_info', '可以修改自己的客户信息'), ('add_customer_get', '可以进入新增客户界面'), ('add_customer_post', '可以提交新增客户信息'), ('batch_own_customer_info', '可以批量操作自己的客户信息'), ('view_courserecord_list', '可以查看开课记录列表'), ('batch_own_courserecord_info', '可以批量操作自己的开课记录'), ('add_courserecord_info', '可以新增开课记录'), ('view_classlist_list', '可以查看班级列表'), ('edit_classlist_info', '可以修改班级'), ('batch_own_classlist_info', '可以批量操作班级'), ('add_classlist_info', '可以新增班级'), ('view_studyrecord_list', '可以查看学习记录列表'), ('edit_studyrecord_info', '可以修改学习记录'), ('batch_studyrecord_info', '可以批量操作学习记录'), ('add_studyrecord_info', '可以新增学习记录'), ('view_userprofile_list', '可以查看用户列表'), ('view_school_list', '可以查看校区列表'))},
        ),
    ]
