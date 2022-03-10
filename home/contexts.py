from django import template
from home.models import Address


register = template.Library()


@register.inclusion_tag('base.html', takes_context=True)
def address(context):
    address = Address.objects.all()
    return {'address': address}
