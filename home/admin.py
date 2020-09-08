from django.contrib import admin
from .models import item, orderitem, order

# Register your models here.
admin.site.register(item)
admin.site.register(order)
admin.site.register(orderitem)
