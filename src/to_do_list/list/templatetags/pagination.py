from django import template
from django.http import QueryDict
from django.utils.safestring import mark_safe
from django.core.paginator import Page
register = template.Library()


def generate_link(page_number: int, link_title: str,  query: QueryDict, active=False) -> str:
    classes = 'active' if active else ''
    query['page'] = page_number
    return f'<a class="{classes} larger-size" href="?{query.urlencode()}">{link_title}</a>'


@register.simple_tag(takes_context=True)
def paginate(context):
    query = context['request'].GET.copy()
    page_obj: Page = context['page_obj']
    paginate_html = ''
    current_page = page_obj.number
    total_page = page_obj.paginator.num_pages

    if page_obj.has_previous():
        paginate_html += generate_link(page_obj.previous_page_number(), '«', query)
        if current_page - 3 >= 1:
            paginate_html += generate_link(1, '1', query)
        if current_page - 2 >= 3:
            paginate_html += generate_link(current_page - 3, '...', query)

    if total_page > 1:
        start_page = max(current_page - 2, 1)
        last_page = min(current_page + 3, total_page + 1)
        for page in range(start_page, last_page):
            paginate_html += generate_link(page, str(page), query, page == current_page)

    if page_obj.has_next():
        if current_page + 3 < total_page:
            paginate_html += generate_link(current_page + 3, '...', query)
        if current_page + 3 <= total_page:
            paginate_html += generate_link(total_page, total_page, query)
        paginate_html += generate_link(page_obj.next_page_number(), '»', query)

    html = f'<div class="container pagination"><div class="row text-center">{paginate_html}</div></div>'
    return mark_safe(html)
