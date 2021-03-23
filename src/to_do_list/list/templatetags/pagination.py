from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def paginate(context):
    print(context)
    page_obj = context['page_obj']
    paginate_html = '<div class="container pagination"><div class="row text-center">'
    current_page = page_obj.number
    total_page = page_obj.paginator.num_pages

    def generate_link(link, link_value, style=''):
        return f'<a class="{style} larger-size" href="?page={link}">{link_value}</a>'

    if page_obj.has_previous():
        paginate_html += generate_link(page_obj.previous_page_number(), '«')
        if current_page - 2 > 1:
            paginate_html += generate_link(1, 1)
        if current_page - 2 >= 3:
            paginate_html += generate_link(page_obj.previous_page_number(), '...')

    for page in range(total_page):
        page += 1
        if page == current_page:
            paginate_html += generate_link('#', page, style='active')
        elif current_page - 3 < page < current_page + 3:
            paginate_html += generate_link(page, page)

    if page_obj.has_next():
        if current_page + 3 < total_page:
            paginate_html += generate_link(current_page + 3, '...')
        if current_page + 2 < total_page:
            paginate_html += generate_link(total_page, total_page)
        paginate_html += generate_link(page_obj.next_page_number(), '»')

    paginate_html += '</div></div>'

    return mark_safe(paginate_html)
