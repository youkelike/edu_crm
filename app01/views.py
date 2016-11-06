from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

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
            return HttpResponseRedirect('/')
        else:
            login_err = 'Wrong username or password'
            return render(request, 'login.html',{'login_err':login_err})
    return render(request,'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):

    return render(request,'app01/dashboard.html')

@check_permission
def customers(request):
    # 取出要过滤的字段值
    filter_dic = forms.get_filter_fields(models.Customer)

    page = request.GET.get('page')

    #构建过滤条件
    q = Q()
    q.connector = 'AND'
    filter_fields = settings.FILTER_FIELDS['Customer']
    search_str = ''
    search_val_dic = {}
    for field_name in filter_fields:
        search_val = request.GET.get(field_name)
        if search_val is not None:
            search_val_dic[field_name] = search_val
            print('***search_str:',search_val)
            q.children.append((field_name,search_val))
            search_str += '&%s=%s' % (field_name,search_val)#用在分页功能上
    if len(q.children) > 0:
        customer_list = models.Customer.objects.filter(q)
    else:
        customer_list = models.Customer.objects.all()

    #指定每页记录数量，生成实例
    paginator = Paginator(customer_list,3)
    try:
        # 取指定页的数据对象
        customer_objs = paginator.page(page)
    except PageNotAnInteger:
        #页码不是整数
        page = 1
    except EmptyPage:
        #页码超出范围
        page = paginator.num_pages
    customer_objs = paginator.page(page)



    return render(request,'app01/customers.html',{
        'customer_list':customer_objs,
        'filter_dic':filter_dic,
        'page':page,
        'search_str':search_str,
        'search_val_dic':search_val_dic,
    })

@check_permission
def customer_detail(request,customer_id):
    customer_obj = models.Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        form = forms.CustomerModelForm(request.POST,instance=customer_obj)
        if form.is_valid():
            form.save()

            #动态跳转
            base_url = '/'.join(request.path.split('/'))[:-2]
            return redirect(base_url)

    else:
        form = forms.CustomerModelForm(instance=customer_obj)

    return render(request,'app01/customer_detail.html',{'customer_form':form})

def customer_add(request):
    if request.method == 'POST':
        form = forms.CustomerModelForm(request.POST)
        print('***post data:',request.POST)
        print('***valid:',form.is_valid())
        print('***errors:',form.errors)
        print('***path:', request.path)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            return redirect(base_url)
    else:
        form = forms.CustomerModelForm()

    return render(request,'app01/customer_add.html',{'customer_form':form})