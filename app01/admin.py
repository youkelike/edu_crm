from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.Customer)
admin.site.register(models.ConsultRecord)
admin.site.register(models.CourseRecord)
admin.site.register(models.ClassList)
admin.site.register(models.StudyRecord)
admin.site.register(models.UserProfile)
admin.site.register(models.Course)
admin.site.register(models.School)