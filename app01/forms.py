from django.forms import Form,ModelForm
from app01 import models
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