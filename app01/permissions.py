from django.core.urlresolvers import resolve
from django.shortcuts import render
import json
from app01 import models

perm_dic = {
    'view_customer_list':['customer_list','GET',None],#浏览列表
    'view_customer_info':['customer_detail','GET',None],#查看详细
    'edit_own_customer_info':['customer_detail','POST','customer'],#修改详细
    'add_customer_get':['customer_add','GET',None],#进入新增
    'add_customer_post':['customer_add','POST',None],#提交新增
    'batch_own_customer_info':['customer_list','POST','customer'],#批量修改

    # 'view_customer_list':['customer_list','GET',''],#浏览列表
    # 'view_customer_info':['customer_detail','GET',''],#查看详细
    # 'edit_own_customer_info':['customer_detail','POST','customer'],#修改详细
    # 'add_customer_info':['customer_add','GET',''],#进入新增
    # 'add_customer_info':['customer_add','POST',''],#提交新增
    # 'batch_own_customer_info':['customer_list','POST','customer'],#批量修改



}

def perm_check(*args,**kwargs):
    request = args[0]
    #获取url中的id
    if len(args) > 1:
        id = args[1]

    #自动解析出请求url对应的别名
    url_resolve_obj = resolve(request.path_info)
    current_url_namespace = url_resolve_obj.url_name
    print('url namespace: ', current_url_namespace)

    #获取批量操作的所有对象id
    if request.method == 'POST' and request.POST.get('data'):
        ids = json.loads(request.POST.get('data'))['ids']
    else:
        ids = []

    #找到动作对应的权限
    matched_flag = False
    matched_perm_key = False
    if current_url_namespace is not None:
        print('find perm...')
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:
                url_namespace,request_method,relation_string = perm_val
                print(perm_val)
                #匹配url别名
                if url_namespace == current_url_namespace:
                    #匹配请求方法
                    if request.method == request_method:
                        print('matched url_namespace: %s, method: %s ' % (url_namespace,request_method))
                        if not relation_string:#没有第三个参数，也就是不用管操作的对象是不是需要关联到用户
                            matched_flag = True
                            matched_perm_key = perm_key
                            print('matched [%s]...' % perm_key)
                        else:
                            obj = models.UserProfile.objects.select_related()
                            if len(ids)>0:#批量操作
                                filter_dic = {}
                                relation_name = '%s__id' % relation_string
                                print('****batch ids:',ids)
                                not_match = False
                                for id in ids:
                                    filter_dic[relation_name] = id
                                    filter_dic['id'] = request.user.userprofile.id
                                    if not obj.filter(**filter_dic).exists():#只要有一个不匹配就失败
                                        not_match =True
                                        break
                                if not_match:#匹配失败就退出整个权限查找循环
                                    break

                            else:#修改单个
                                print('****single id:', id)
                                filter_dic = {}
                                relation_name = '%s__id' % relation_string
                                filter_dic[relation_name] = id
                                filter_dic['id'] = request.user.userprofile.id
                                if not obj.filter(**filter_dic).exists():  # 不匹配就失败，退出整个权限查找循环
                                    break
                            #走到这表示成功匹配了
                            matched_flag = True
                            matched_perm_key = perm_key
                            print('matched [%s]...' % perm_key)

                        print('\033[42;1m--- find permission string ---\033[0m')
                        break#匹配成功了也退出整个权限查找循环

    else:
        return True

    #判断用户是否有权限
    if matched_flag == True:
        perm_str = 'app01.%s' % (matched_perm_key)
        if request.user.has_perm(perm_str):
            print('\033[42;1m---- passed permission check ----\033[0m')
            return True
        else:
            print('\033[41;1m---- no permission ----\033[0m')
            return False
    else:
        print('\033[41;1m---- no matched permission ----\033[0m')
        return False

#权限装饰器定义
def check_permission(func):
    def inner(*args,**kwargs):
        print('--- start check perm ---')
        if perm_check(*args,**kwargs) is not True:
            return render(args[0],'app01/403.html')
        return func(*args,**kwargs)
    return inner