from django.urls import path
from .views import (
    index,
    shoppingcart,
    itemproduct,
    addcart,
    loginpage,
    remove_item_from_cart,
    CheckoutView,
)
app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('cart/', shoppingcart.as_view(), name='cart'),
    path('product/<slug>/', itemproduct.as_view(), name='product'),
    path('addcart/<slug>/', addcart, name='addcart'),
    path('login/', loginpage, name='loginpage'),
    path('remove_cart/<slug>/', remove_item_from_cart, name='remove_cart'),
    path('check-out/', CheckoutView.as_view(), name='check-out'),
]