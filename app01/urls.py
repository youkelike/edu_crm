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

    # url(r'^courses/$', views.courses,name='course_list'),
    # url(r'^courses/(\d+)/$', views.course_detail,name='course_detail'),
    # url(r'^courses/add/$', views.course_add,name='course_add'),
]
