from django.forms import Form,ModelForm
from app01 import models
from django.db.models import Count
from stu_man import settings

def get_filter_fields(cls):
    filter_fields = settings.FILTER_FIELDS.get(cls.__name__.lower())
    if filter_fields is None:
        return None
    print('***filter fields:', filter_fields)
    field_list = cls._meta.local_fields#取出模型对应表的字段列表

    filter_dic = []
    for field in field_list:
        print('***field_name:', field.attname)
        if field.attname in filter_fields:#只处理配置中存在的字段
            name = field.verbose_name#模型中定义的字段别名
            print('***is relation:', bool(field.is_relation))
            if bool(field.is_relation):  # 如果是关联字段
                is_relation = True
                group_id = field.attname
                group_name = '%s__name' % field.attname[:-3]
                print('***group_name:', group_name)
                #得到的是group by group_name后，取(group_id,count(group_name))两个字段组成的二元组列表
                val_list = cls.objects.all().values_list(group_id, group_name).annotate(Count(group_name))
                print('***relation val_dic:', val_list)
            else:
                is_relation = False
                group_name = field.attname
                val_dic = cls.objects.all().values_list(group_name).annotate(Count(group_name))
                #加上选项对应的别名
                alias_list = dict(getattr(cls,'%s_choices' % group_name))
                val_list = []
                for i in val_dic:
                    tmp_list = list(i)
                    tmp_list.append(alias_list[i[0]])
                    val_list.append(tmp_list)

            filter_dic.append({'name': name, 'tags': list(val_list),'is_relation':is_relation,'field_name':field.attname})
    print('***filter_dic:', filter_dic)
    return filter_dic

class CustomerModelForm(ModelForm):
    class Meta:
        #指定模式表单对应的模型
        model = models.Customer
        #模型中以下指定的字段不显示在表单中
        exclude = ()

    #给模式表单中的字段加自定义样式
    def __init__(self,*args,**kwargs):
        super(CustomerModelForm,self).__init__(*args,**kwargs)
        #self.fields['qq'].widget.attrs['class'] = 'form-control'

        #遍历模型里的所有字段，加上一些表单属性
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})

class CourseModelForm(ModelForm):
    class Meta:
        model = models.Course
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(CourseModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class SchoolModelForm(ModelForm):
    class Meta:
        model = models.School
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(SchoolModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileModelForm(ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(UserProfileModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class CourseRecordModelForm(ModelForm):
    class Meta:
        model = models.CourseRecord
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(CourseRecordModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class StudyRecordModelForm(ModelForm):
    class Meta:
        model = models.StudyRecord
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(StudyRecordModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class ConsultRecordModelForm(ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(ConsultRecordModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class ClassListModelForm(ModelForm):
    class Meta:
        model = models.ClassList
        exclude = ()
    # 给模式表单中的字段加自定义样式
    def __init__(self, *args, **kwargs):
        super(ClassListModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

