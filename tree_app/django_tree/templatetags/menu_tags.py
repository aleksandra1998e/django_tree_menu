from django import template
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html')
def draw_menu(request, menu_name):

    menu_items = MenuItem.objects.filter(parent__isnull=True, name=menu_name)
    menu_items = menu_items.prefetch_related('children')

    active_menu_item = None
    for menu_item in menu_items:
        if request.path.startswith(menu_item.link):
            active_menu_item = list(filter(None, request.path.split('/')))
            break
    return {
        'menu_items': [render_menu_item(menu_item, active_menu_item) for menu_item in menu_items],
    }


@register.simple_tag
def render_menu(menu_items):
    output = '<ul>'
    for menu_item in menu_items:
        output += '<li>'
        link = menu_item['link']
        label = menu_item['label']
        output += f'<a href="{link}">{label}</a>'
        if menu_item['children']:
            output += render_menu(menu_item['children'])
        output += '</li>'
    output += '</ul>'
    return output


def render_menu_item(menu_item, active_menu_item):
    active = (list(filter(None, menu_item.link.split('/')))[-1] in active_menu_item)
    children = []
    if active:
        children = menu_item.children.all()
    return {
        'name': menu_item.name,
        'link': menu_item.link,
        'label': menu_item.label,
        'active': active,
        'children': [render_menu_item(child, active_menu_item) for child in children],
    }