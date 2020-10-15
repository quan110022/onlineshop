from django.contrib import admin
from .models import item, orderitem, order, check_out, Payment, Men, Women



# Register your models here.
admin.site.register(item)
admin.site.register(order)
admin.site.register(orderitem)
admin.site.register(check_out)
admin.site.register(Payment)
admin.site.register(Men)
admin.site.register(Women)




