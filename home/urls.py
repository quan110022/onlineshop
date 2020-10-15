from django.urls import path
from .views import (
    index,
    shoppingcart,
    itemproduct,
    addcart,
    remove_item_from_cart,
    CheckoutView,
    PaymentView,
    MenClothing,
    WomenView,



)
app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('cart/', shoppingcart.as_view(), name='cart'),
    path('product/<slug>/', itemproduct.as_view(), name='product'),
    path('addcart/<slug>/', addcart, name='addcart'),
    path('remove_cart/<slug>/', remove_item_from_cart, name='remove_cart'),
    path('check-out/', CheckoutView.as_view(), name='check-out'),
    path('payment/<payment>/', PaymentView.as_view(), name="payment"),
    path('men-clothing/', MenClothing, name='men-clo'),
    path('women-clothing/', WomenView, name='women-clo'),
]