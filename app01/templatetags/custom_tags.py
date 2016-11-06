from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def a_upper(val):
    print('---val from template: %s---' % val)
    return val.upper()

@register.simple_tag
def guess_page(cur_page,loop_num):
    offset = abs(cur_page - loop_num)
    if offset < 3:
        if cur_page == loop_num:
            page_ele = '<li class ="active" > <a href="?page=%s" > %s </a> </li>' % (loop_num,loop_num)
        else:
            page_ele = '<li class ="" > <a href="?page=%s" > %s </a> </li>' % (loop_num, loop_num)
    else:
        page_ele = ''
    return format_html(page_ele)

@register.simple_tag
def pagination_bar(lists):
    page_ele = '<ul class="pagination">'
    if lists.has_previous():
        page_ele += '<li class=""><a href="?page=%s">&laquo;</a></li>' % lists.previous_page_number()
    for page_num in lists.paginator.page_range:
        offset = abs(lists.number - page_num)
        if offset < 3:
            if lists.number == page_num:
                page_ele += '<li class ="active" > <a href="?page=%s" > %s </a> </li>' % (page_num, page_num)
            else:
                page_ele += '<li class ="" > <a href="?page=%s" > %s </a> </li>' % (page_num, page_num)

    if lists.has_next():
        page_ele += '<li class=""><a href="?page=%s">&raquo;</a></li>' % lists.next_page_number()
    page_ele += '</ul>'
    return format_html(page_ele)