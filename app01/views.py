from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

import json
from app01 import models
from app01 import forms
from app01.permissions import check_permission
from stu_man import settings
from django.db.models import Q

# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        #验证动作
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        if user is not None:
            #登录动作
            login(request,user)
            return HttpResponseRedirect('/crm/')
        else:
            login_err = 'Wrong username or password'
            return render(request, 'login.html',{'login_err':login_err})
    return render(request,'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):

    return render(request,'app01/dashboard.html')

def build_search_param(request,cls):
    # 取出要过滤的字段值
    filter_dic = forms.get_filter_fields(cls)

    page = request.GET.get('page')

    # 构建过滤条件
    q = Q()
    q.connector = 'AND'
    filter_fields = settings.FILTER_FIELDS.get(cls.__name__.lower(),[])
    search_str = ''
    search_val_dic = {}
    for field_name in filter_fields:
        search_val = request.GET.get(field_name)
        if search_val is not None:
            search_val_dic[field_name] = search_val
            print('***search_str:', search_val)
            q.children.append((field_name, search_val))
            search_str += '&%s=%s' % (field_name, search_val)  # 用在分页功能上

    # 找出搜索框输入,约定变量名为：find__字段名
    print('***GET:', request.GET)
    find_list = []
    for f_dic in request.GET.items():
        if f_dic[0].startswith('find__') and len(f_dic[1]) > 0:
            print('**********find str:', f_dic)
            q.children.append(('%s__contains' % f_dic[0].replace('find__',''), f_dic[1]))
            find_list = f_dic

    if len(q.children) > 0:
        data_obj = cls.objects.filter(q)
    else:
        data_obj = cls.objects.all()

    # 指定每页记录数量，生成实例
    paginator = Paginator(data_obj, 3)
    try:
        # 取指定页的数据对象
        data_list = paginator.page(page)
    except PageNotAnInteger:
        # 页码不是整数
        data_list = paginator.page(1)
    except EmptyPage:
        # 页码超出范围
        data_list = paginator.page(paginator.num_pages)

    return {
        'data_list':data_list,
        'filter_dic':filter_dic,
        'page':page,
        'search_str':search_str,
        'search_val_dic':search_val_dic,
        'find_list':find_list,
        'url_alias':'%s_list' % cls.__name__.lower(),
        'actions':settings.FRONT_ACTIONS.get(cls.__name__.lower(),[]),
    }

def front_action_handle(request,cls):
    print(json.loads(request.POST['data']))
    data = json.loads(request.POST['data'])
    if data['name'] == 'delete_select':
        cls.objects.filter(id__in=data['ids']).delete()
    else:
        field_name = data['name'].split('_2_')[0]
        field_val = data['name'].split('_2_')[1]
        cls.objects.filter(id__in=data['ids']).update(**{field_name: field_val})


def customers(request):
    # post方式请求就是执行操作
    if request.method == 'POST':
        front_action_handle(request, models.Customer)
        return HttpResponse('ok')

    #通用方法构建查询结果
    data_dic = build_search_param(request, models.Customer)

    return render(request,'app01/customers.html',data_dic)

@check_permission
def customer_detail(request,id):
    data_obj = models.Customer.objects.get(id=id)

    if request.method == 'POST':
        form = forms.CustomerModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()
            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CustomerModelForm(instance=data_obj)

    return render(request,'app01/customer_detail.html',{'data_form':form})

def customer_add(request):
    if request.method == 'POST':
        form = forms.CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CustomerModelForm()

    return render(request,'app01/customer_add.html',{'data_form':form})


def courses(request):
    #通用方法构建查询结果
    data_dic = build_search_param(request, models.Course)

    return render(request,'app01/courses.html',data_dic)

def course_detail(request,id):
    data_obj = models.Course.objects.get(id=id)
    if request.method == 'POST':
        form = forms.CourseModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CourseModelForm(instance=data_obj)

    return render(request,'app01/course_detail.html',{'data_form':form})

def course_add(request):
    if request.method == 'POST':
        form = forms.CourseModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CourseModelForm()

    return render(request,'app01/course_add.html',{'data_form':form})


def schools(request):
    #通用方法构建查询结果
    data_dic = build_search_param(request, models.School)

    return render(request,'app01/schools.html',data_dic)

def school_detail(request,id):
    data_obj = models.School.objects.get(id=id)
    if request.method == 'POST':
        form = forms.SchoolModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.SchoolModelForm(instance=data_obj)

    return render(request,'app01/school_detail.html',{'data_form':form})

def school_add(request):
    if request.method == 'POST':
        form = forms.SchoolModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.SchoolModelForm()

    return render(request,'app01/school_add.html',{'data_form':form})


def userprofiles(request):
    #通用方法构建查询结果
    data_dic = build_search_param(request, models.UserProfile)

    return render(request,'app01/userprofiles.html',data_dic)

def userprofile_detail(request,id):
    data_obj = models.UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = forms.UserProfileModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.UserProfileModelForm(instance=data_obj)

    return render(request,'app01/userprofile_detail.html',{'data_form':form})

def userprofile_add(request):
    if request.method == 'POST':
        form = forms.UserProfileModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.UserProfileModelForm()

    return render(request,'app01/userprofile_add.html',{'data_form':form})


def courserecords(request):
    #通用方法构建查询结果
    data_dic = build_search_param(request, models.CourseRecord)

    return render(request,'app01/courserecords.html',data_dic)

def courserecord_detail(request,id):
    data_obj = models.CourseRecord.objects.get(id=id)
    if request.method == 'POST':
        form = forms.CourseRecordModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CourseRecordModelForm(instance=data_obj)

    return render(request,'app01/courserecord_detail.html',{'data_form':form})

def courserecord_add(request):
    if request.method == 'POST':
        form = forms.CourseRecordModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CourseRecordModelForm()

    return render(request,'app01/courserecord_add.html',{'data_form':form})


def studyrecords(request):
    # post方式请求就是执行操作
    if request.method == 'POST':
        front_action_handle(request,models.StudyRecord)
        return HttpResponse('ok')

    #通用方法构建查询结果
    data_dic = build_search_param(request, models.StudyRecord)

    return render(request,'app01/studyrecords.html',data_dic)

def studyrecord_detail(request,id):
    data_obj = models.StudyRecord.objects.get(id=id)
    if request.method == 'POST':
        form = forms.StudyRecordModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.StudyRecordModelForm(instance=data_obj)

    return render(request,'app01/studyrecord_detail.html',{'data_form':form})

def studyrecord_add(request):
    if request.method == 'POST':
        form = forms.StudyRecordModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.StudyRecordModelForm()

    return render(request,'app01/studyrecord_add.html',{'data_form':form})


def consultrecords(request):
    #通用方法构建查询结果
    data_dic = build_search_param(request, models.ConsultRecord)

    return render(request,'app01/consultrecords.html',data_dic)

def consultrecord_detail(request,id):
    data_obj = models.ConsultRecord.objects.get(id=id)
    if request.method == 'POST':
        form = forms.ConsultRecordModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.ConsultRecordModelForm(instance=data_obj)

    return render(request,'app01/consultrecord_detail.html',{'data_form':form})

def consultrecord_add(request):
    if request.method == 'POST':
        form = forms.ConsultRecordModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.ConsultRecordModelForm()

    return render(request,'app01/consultrecord_add.html',{'data_form':form})


def classlists(request):
    # post方式请求就是执行操作
    if request.method == 'POST':
        print(request.POST)

    #通用方法构建查询结果
    data_dic = build_search_param(request, models.ClassList)

    return render(request,'app01/classlists.html',data_dic)

def classlist_detail(request,id):
    data_obj = models.ClassList.objects.get(id=id)
    if request.method == 'POST':
        form = forms.ClassListModelForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.ClassListModelForm(instance=data_obj)

    return render(request,'app01/classlist_detail.html',{'data_form':form})

def classlist_add(request):
    if request.method == 'POST':
        form = forms.ClassListModelForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.ClassListModelForm()

    return render(request,'app01/classlist_add.html',{'data_form':form})



