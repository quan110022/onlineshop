from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, View
from .models import item, orderitem, order
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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






class itemproduct(DetailView):
    model = item
    template_name = 'onlineshoop/product.html'
@login_required
def addcart(request, slug):
    Item = get_object_or_404(item, slug=slug)
    Order_item, created = orderitem.objects.get_or_create(Item=Item, user=request.user, ordered=False)
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


class shoppingcart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            Order = order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': Order
            }

            return render(self.request, 'onlineshoop/shopping-cart.html', context)
        except ObjectDoesNotExist:
            messages.error('ban can dang nhap')
            return redirect('???')
@login_required
def remove_item_from_cart(request, slug):
    Item = get_object_or_404(item, slug=slug)
    order_qs = order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        Order = order_qs[0]
        # check if the order item is in the order
        if Order.Items.filter(Item__slug=Item.slug).exists():
            order_item = orderitem.objects.filter(
                Item=Item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                Order.Items.remove(order_item)
            messages.info(request, "update quantity item.")
            return redirect("home:cart")
        else:
            messages.info(request, "not item")
            return redirect("home:product", slug=slug)
    else:
        messages.info(request, "not order")
        return redirect("home:product", slug=slug)

















