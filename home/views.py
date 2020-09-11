from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView
from .models import item, orderitem, order
from django.utils import timezone

from django.contrib.auth import login

# Create your views here.
def product(request):
    context = {
        'Items': item.objects.all()
    }
    return render(request, 'onlineshoop/product.html', context)

def index(request):
    context = {
        'Items': item.objects.all()
    }
    return render(request, 'onlineshoop/index.html', context)

def cart(request):
    return render(request, 'onlineshoop/shopping-cart.html')

class itemproduct(DetailView):
    model = item
    template_name = 'onlineshoop/product.html'

def addcart(request, slug):
    Item = get_object_or_404(item, slug=slug)
    Order_item = orderitem.objects.create(Item=Item)
    Order_qt = order.objects.filter(user=request.user)
    if Order_qt.exists():
        Order = Order_qt[0]
        if Order.Items.filter(Item__slug=Item.slug).exists():
            Order_item.quantity += 1
            Order_item.save()
        else:
            Order.Items.add(Order_item)


    else:
        orderdate = timezone.now()
        Order = order.objects.create(user=request.user, orderdate=orderdate)
        Order.Items.add(Order_item)
    return redirect("home:product", slug=slug)

def loginpage(request):
    return render(request, 'onlineshoop/login.html')
















