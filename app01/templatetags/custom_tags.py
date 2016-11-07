from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def a_upper(val):
    print('---val from template: %s---' % val)
    return val.upper()

@register.filter
def guess_param(name,dic):
    print('***guess_param:',dic)
    param = ''
    for d in dic.items():
        print(d)
        if d[0] != name:
            param += '&%s=%s' % (d[0],d[1])
    print('***param:',param)
    return param

@register.filter
def show_m_2_m(obj):
    strs = []
    for o in obj:
        strs.append(str(o.name))
    return ','.join(strs)

@register.simple_tag
def guess_page(cur_page,loop_num,search_str,find_list):
    offset = abs(cur_page - loop_num)
    if offset < 3:
        if cur_page == loop_num:
            page_ele = '<li class ="active" > <a href="?page=%s%s" > %s </a> </li>' % (loop_num,search_str,loop_num)
        else:
            page_ele = '<li class ="" > <a href="?page=%s%s"> %s </a> </li>' % (loop_num,search_str,loop_num)
    else:
        page_ele = ''
    return format_html(page_ele)

@register.simple_tag
def pagination_bar(lists,search_str,find_list):
    page_ele = '<ul class="pagination">'
    if lists.has_previous():
        if len(find_list) == 2:
            page_ele += '<li class=""><a href="?page=%s%s&%s=%s">&laquo;</a></li>' % (
                            lists.previous_page_number(), search_str,find_list[0],find_list[1]
                        )
        else:
            page_ele += '<li class=""><a href="?page=%s%s">&laquo;</a></li>' % (lists.previous_page_number(),search_str)
    for page_num in lists.paginator.page_range:
        offset = abs(lists.number - page_num)
        if offset < 3:
            if lists.number == page_num:
                page_ele += '<li class ="active" >'
            else:
                page_ele += '<li class ="" >'

            if len(find_list) == 2:
                page_ele += '<a href="?page=%s%s&%s=%s" > %s </a> </li>' % (page_num,search_str,find_list[0],find_list[1],page_num)
            else:
                page_ele += '<a href="?page=%s%s" > %s </a> </li>' % (page_num, search_str, page_num)

    if lists.has_next():
        if len(find_list) == 2:
            page_ele += '<li class=""><a href="?page=%s%s&%s=%s">&raquo;</a></li>' % (
                            lists.next_page_number(),search_str,find_list[0],find_list[1]
                        )
        else:
            page_ele += '<li class=""><a href="?page=%s%s">&raquo;</a></li>' % (lists.next_page_number(),search_str)
    page_ele += '</ul>'
    return format_html(page_ele)