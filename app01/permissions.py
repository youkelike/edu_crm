from django.core.urlresolvers import resolve
from django.shortcuts import render

perm_dic = {
    'view_customer_list':['customer_list','GET',[]],
    'view_customer_info':['customer_detail','GET',[]],
    'edit_own_customer_info':['customer_detail','POST',['qq','name']],
}

def perm_check(*args,**kwargs):
    request = args[0]
    #自动解析出请求url对应的别名
    url_resolve_obj = resolve(request.path_info)
    current_url_namespace = url_resolve_obj.url_name
    print('url namespace: ', current_url_namespace)

    matched_flag = False
    matched_perm_key = False
    if current_url_namespace is not None:
        print('find perm...')
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:
                url_namespace,request_method,request_args = perm_val
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace:
                    if request.method == request_method:
                        if not request_args:
                            matched_flag = True
                            matched_perm_key = perm_key
                            print('matched...')
                            break
                        else:
                            for request_arg in request_args:
                                request_method_func = getattr(request,request_method)
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True
                                else:
                                    matched_flag = False
                                    print('request arg [%s] not matched' % request_arg)
                                    break
                            if matched_flag:
                                print('--- passed permission check ---')
                                matched_perm_key = perm_key
                                break
    else:
        return True

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


def check_permission(func):
    def inner(*args,**kwargs):
        print('--- start check perm ---')
        if perm_check(*args,**kwargs) is not True:
            return render(args[0],'app01/403.html')
        return func(*args,**kwargs)
    return inner