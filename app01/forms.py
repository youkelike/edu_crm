from django.forms import Form,ModelForm
from app01 import models
from django.db.models import Count
from stu_man import settings

def get_filter_fields(cls):
    filter_fields = settings.FILTER_FIELDS.get(cls.__name__)
    if filter_fields is None:
        return None
    print('***filter fields:', filter_fields)
    field_list = cls._meta.local_fields

    filter_dic = []
    for field in field_list:
        print('***field_name:', field.attname)
        if field.attname in filter_fields:
            name = field.verbose_name
            print('***is relation:', bool(field.is_relation))
            if bool(field.is_relation):  # 如果是关联字段
                is_relation = True
                group_id = field.attname
                group_name = '%s__name' % field.attname[:-3]
                print('***group_name:', group_name)
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
        model = models.Customer
        exclude = ()

    #给模式表单中的字段加自定义样式
    def __init__(self,*args,**kwargs):
        super(CustomerModelForm,self).__init__(*args,**kwargs)
        #self.fields['qq'].widget.attrs['class'] = 'form-control'

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

