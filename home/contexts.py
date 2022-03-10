from django import template
from home.models import Address, HeroText, HeroHeader


register = template.Library()


@register.inclusion_tag('base.html', takes_context=True)
def address(context):
    address = Address.objects.all()
    hero_header = HeroHeader.objects.all()
    hero_text = HeroText.objects.all()
    context = {
        'address': address,
        'hero_header': hero_header,
        'hero_text': hero_text,
    }
    return context
