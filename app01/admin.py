from django.contrib import admin
from app01 import models
# Register your models here.

def change_record_2_delay(modelAdmin,request,queryset):
    print(request,queryset)
    queryset.update(record='late')

change_record_2_delay.short_description = u'更改上课记录为迟到'

class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ('student','course_record','record','score','date')
    list_filter = ('record',)
    actions = [change_record_2_delay,]

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('qq','source','referral_from','course','class_type','status','consultant','date')
    list_filter = ('status','consultant')

admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.ConsultRecord)
admin.site.register(models.CourseRecord)
admin.site.register(models.ClassList)
admin.site.register(models.StudyRecord,StudyRecordAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Course)
admin.site.register(models.School)