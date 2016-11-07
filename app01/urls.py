"""stu_man URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from app01 import views
urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^customers/$', views.customers,name='customer_list'),
    url(r'^customers/(\d+)/$', views.customer_detail,name='customer_detail'),#取别名
    url(r'^customers/add/$', views.customer_add,name='customer_add'),

    url(r'^courses/$', views.courses,name='course_list'),
    url(r'^courses/(\d+)/$', views.course_detail,name='course_detail'),
    url(r'^courses/add/$', views.course_add,name='course_add'),

    url(r'^schools/$', views.schools,name='school_list'),
    url(r'^schools/(\d+)/$', views.school_detail,name='school_detail'),
    url(r'^schools/add/$', views.school_add,name='school_add'),

    url(r'^userprofiles/$', views.userprofiles,name='userprofile_list'),
    url(r'^userprofiles/(\d+)/$', views.userprofile_detail,name='userprofile_detail'),
    url(r'^userprofiles/add/$', views.userprofile_add,name='userprofile_add'),

    url(r'^courserecords/$', views.courserecords,name='courserecord_list'),
    url(r'^courserecords/(\d+)/$', views.courserecord_detail,name='courserecord_detail'),
    url(r'^courserecords/add/$', views.courserecord_add,name='courserecord_add'),

    url(r'^studyrecords/$', views.studyrecords,name='studyrecord_list'),
    url(r'^studyrecords/(\d+)/$', views.studyrecord_detail,name='studyrecord_detail'),
    url(r'^studyrecords/add/$', views.studyrecord_add,name='studyrecord_add'),

    url(r'^consultrecords/$', views.consultrecords,name='consultrecord_list'),
    url(r'^consultrecords/(\d+)/$', views.consultrecord_detail,name='consultrecord_detail'),
    url(r'^consultrecords/add/$', views.consultrecord_add,name='consultrecord_add'),

    url(r'^classlists/$', views.classlists,name='classlist_list'),
    url(r'^classlists/(\d+)/$', views.classlist_detail,name='classlist_detail'),
    url(r'^classlists/add/$', views.classlist_add,name='classlist_add'),



]
