from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


#定义在外面就不能通过各模型类取到这个变量了
class_type_choices = (
    ('online',u'网络班'),
    ('offline_weekend',u'周末面授班'),
    ('offline_fulltime',u'脱产面授班'),
)

class UserProfile(models.Model):
    #继承内置的用户认证机制，可以实现继承并扩展自己的字段
    #在数据库中实现就是foreignkey，所以这种onetoone只能在django层面限制，不能在数据库里限制
    #
    user = models.OneToOneField(User)
    name = models.CharField(u'姓名',max_length=32)
    school = models.ForeignKey('School',verbose_name='校区',default=1)
    def __str__(self):
        return self.name

    #权限定义，与表结构本身没关系，可以写到任意表结构定义下面
    class Meta:
        permissions = (
            #讲师只能看，销售有全部权限
            ('view_customer_list',u'可以查看客户列表'),
            ('view_customer_info',u'可以查看客户详细信息'),
            ('edit_own_customer_info',u'可以修改自己的客户信息'),
            ('add_customer_get',u'可以进入新增客户界面'),
            ('add_customer_post', u'可以提交新增客户信息'),
            ('batch_own_customer_info', u'可以批量操作自己的客户信息'),

            #讲师有全部权限，销售、学员只能看
            ('view_courserecord_list', u'可以查看开课记录列表'),
            ('batch_own_courserecord_info',u'可以批量操作自己的开课记录'),
            ('add_courserecord_info',u'可以新增开课记录'),

            #讲师有全部权限，销售、学员只能看
            ('view_classlist_list', u'可以查看班级列表'),
            ('edit_classlist_info', u'可以修改班级'),
            ('batch_own_classlist_info', u'可以批量操作班级'),
            ('add_classlist_info', u'可以新增班级'),

            #讲师有全部权限，销售、学员只能看
            ('view_studyrecord_list', u'可以查看学习记录列表'),
            ('edit_studyrecord_info', u'可以修改学习记录'),
            ('batch_studyrecord_info', u'可以批量操作学习记录'),
            ('add_studyrecord_info', u'可以新增学习记录'),

            #校长有权限
            ('view_userprofile_list', u'可以查看用户列表'),
            ('view_school_list', u'可以查看校区列表'),

        )


class School(models.Model):
    name = models.CharField(u'校区名称',max_length=64,unique=True)
    addr = models.CharField(u'地址',max_length=128)
    #staffs = models.ManyToManyField('UserProfile',blank=True,verbose_name='成员')
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(u'课程名称',max_length=128,unique=True)
    price = models.IntegerField(u'面授价格')
    online_price = models.IntegerField(u'网络班价格')
    brief = models.TextField(u'课程简介')
    def __str__(self):
        return self.name

class ClassList(models.Model):
    course = models.ForeignKey(Course)
    course_type = models.CharField(u'课程类型',choices=class_type_choices,max_length=32)
    semester = models.IntegerField(u'学期')
    start_date = models.DateField(u'开班日期')
    graduate_date = models.DateField(u'毕业日期',blank=True,null=True)
    teachers = models.ManyToManyField(UserProfile,verbose_name=u'讲师')
    def __str__(self):
        #显示选项中的中文
        return u'%s(%s)[%s期]' % (self.course.name,self.get_course_type_display(),self.semester)
    class Meta:
        verbose_name = u'班级列表'
        verbose_name_plural = u'班级列表'
        #联合唯一
        unique_together = ('course','course_type','semester')

class Customer(models.Model):
    qq = models.CharField(u'QQ号',max_length=64,unique=True)
    name = models.CharField(u'姓名',max_length=32,blank=True,null=True)
    phone = models.BigIntegerField(u'手机',blank=True,null=True)
    stu_id = models.CharField(u'学号',blank=True,null=True,max_length=64)
    source_choices = (
        ('qq',u'qq群'),
        ('referral',u'内部转介绍'),
        ('51cto',u'51cto'),
        ('agent',u'招生代理'),
        ('others',u'其它'),
    )
    source = models.CharField(u'客户来源',max_length=64,choices=source_choices,default='qq')
    #加一个推荐人字段，关联到这个表的其它记录,self要加引号
    referral_from = models.ForeignKey('self',
                                      verbose_name=u'转介绍自学员',
                                      help_text='若客户是转介绍自学员，填写学员姓名',
                                      blank=True,
                                      null=True,
                                      # 这个一定要有，反查时用这个名
                                      related_name='internal_referral')

    course = models.ForeignKey(Course,verbose_name=u'咨询课程')
    class_type_choices = (
        ('online', u'网络班'),
        ('offline_weekend', u'周末面授班'),
        ('offline_fulltime', u'脱产面授班'),
    )
    class_type = models.CharField(u'班级类型',max_length=64,choices=class_type_choices)
    customer_note = models.TextField(u'客户咨询详情',help_text=u'客户咨询的对话记录')
    status_choices = (
        ('signed',u'已报名'),
        ('unregistered',u'未报名'),
        ('graduated',u'已毕业'),
        ('dropoff',u'已退学'),
    )
    status = models.CharField(u'客户状态',choices=status_choices,max_length=64,default='unregistered')
    consultant = models.ForeignKey(UserProfile,verbose_name=u'课程顾问')
    date = models.DateField(u'咨询日期',auto_now_add=True)
    #多对多或外键字段可以不填的情况，只要加上blank=True
    class_list = models.ManyToManyField(ClassList,verbose_name=u'已报名班级',blank=True)
    def __str__(self):
        return u'%s, %s' % (self.qq,self.name)

class ConsultRecord(models.Model):
    customer = models.ForeignKey(Customer,verbose_name=u'咨询客户')
    note = models.TextField(u'跟进内容')
    status_choices = (
        (1,u'近期无报名计划'),
        (2,u'2个月内报名'),
        (3,u'1个月内报名'),
        (4,u'2周内报名'),
        (5,u'1周内报名'),
        (6,u'2天内报名'),
        (7,u'已报名'),
    )
    status = models.IntegerField(u'状态',choices=status_choices,help_text=u'选择此客户的状态')
    consultant = models.ForeignKey(UserProfile,verbose_name=u'跟进人')
    date = models.DateField(u'跟进日期',auto_now_add=True)
    def __str__(self):
        return u'%s, %s' % (self.customer,self.status)
    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u'客户咨询跟进记录'

class CourseRecord(models.Model):
    course = models.ForeignKey(ClassList,verbose_name=u'班级（课程）')
    day_num = models.IntegerField(u'节次',help_text=u'填写第几节课')
    date = models.DateField(auto_now_add=True,verbose_name=u'上课日期')
    teacher = models.ForeignKey(UserProfile,verbose_name=u'讲师')
    def __str__(self):
        return u'%s 第%s天' % (self.course,self.day_num)
    class Meta:
        verbose_name = u'上课记录'
        verbose_name_plural = u'上课记录'
        unique_together = ('course','day_num')

class StudyRecord(models.Model):
    course_record = models.ForeignKey(CourseRecord,verbose_name=u'第几天课程')
    student = models.ForeignKey(Customer,verbose_name=u'学员')
    record_choices = (
        ('checked',u'已签到'),
        ('late',u'迟到'),
        ('absence',u'缺课'),
        ('leave_early',u'早退'),
    )
    record = models.CharField(u'上课记录',choices=record_choices,default='checked',max_length=32)
    score_choices = (
        (100,'A+'),
        (90,'A'),
        (85,'B+'),
        (80,'B'),
        (70,'B-'),
        (60,'C+'),
        (50,'C'),
        (0,'D'),
        (-1,'N/A'),
        (-100,'COPY'),
    )
    score = models.IntegerField(u'本节成绩',choices=score_choices,default=-1)
    date = models.DateField(auto_now_add=True)
    note = models.CharField(u'备注',max_length=255,blank=True,null=True)
    def __str__(self):
        return u'%s，学员：%s，记录：%s，成绩：%s' % (self.course_record,self.student.name,self.record,self.score)
    class Meta:
        verbose_name = u'学员学习记录'
        verbose_name_plural = u'学员学习记录'
        unique_together = ('course_record','student')
