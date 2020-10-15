from django import template
from home.models import order, orderitem

register = template.Library()
@register.filter
def cart_count(user):
    if user.is_authenticated:
        number = order.objects.filter(user=user, ordered=False)
        if number.exists():
            return number[0].Items.count()
    return 0



