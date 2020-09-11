from django.urls import path
from .views import (
    index,
    cart,
    itemproduct,
    addcart,
    loginpage,
)
app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('cart/', cart, name='cart'),
    path('product/<slug>/', itemproduct.as_view(), name='product'),
    path('addcart/<slug>/', addcart, name='addcart'),
    path('login/', loginpage, name='loginpage'),
]