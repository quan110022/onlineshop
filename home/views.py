from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, View
from .models import item, orderitem, order, check_out, Payment, Men, Women
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from django.conf import settings



import stripe
stripe.api_key = settings.STRIPE_PRIVATE_KEY

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token


# Create your views here.




def index(request):
    context = {
        'Items': item.objects.all()
    }
    return render(request, 'onlineshoop/index.html', context)

class itemproduct(DetailView):
    model = item
    template_name = 'onlineshoop/product.html'

@login_required()
def addcart(request, slug):
    Item = get_object_or_404(item, slug=slug)
    Order_item, created = orderitem.objects.get_or_create(Item=Item, user=request.user, ordered=False)
    Order_qt = order.objects.filter(user=request.user)
    if Order_qt.exists():
        Order = Order_qt[0]
        if Order.Items.filter(Item__slug=Item.slug).exists():
            Order_item.quantity += 1
            Order_item.save()
            return redirect('home:cart')
        else:
            Order.Items.add(Order_item)


    else:
        orderdate = timezone.now()
        Order = order.objects.create(user=request.user, orderdate=orderdate)
        Order.Items.add(Order_item)
    return redirect("home:cart")


class shoppingcart(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order_user = order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order_user
            }
            return render(self.request, 'onlineshoop/shopping-cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You No Login')
            return redirect('/')

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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }

        return render(self.request, 'onlineshoop/check-out.html', context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            Order = order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                save_info = form.cleaned_data.get('save_info')
                payment = form.cleaned_data.get('payment')
                checkout = check_out(
                    user=self.request.user,
                    address=address,
                    country=country,
                    zip=zip,
                )
                checkout.save()
                Order.checkout = checkout
                Order.save()
                if payment == 'S':
                    return redirect('home:payment', payment='stripe')
                elif payment == 'P':
                    return redirect('home:payment', payment='paypal')
                else:
                    messages.warning(self.request, 'failed checkout')
                    return redirect('home:check-out')

        except ObjectDoesNotExist:
            messages.error(self.request, 'Not Login')
            return redirect('home:cart')


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'onlineshoop/payment.html')
    def post(self, *args, **kwargs):
        Order = order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(Order.final_total_price() * 100)
        try:
            charge = stripe.Charge.create(

                amount=amount,
                currency="usd",
                source=token,

            )

            # create Payment

            payment = Payment()
            payment.stripe = charge['id']
            payment.user = self.request.user
            payment.amount = Order.final_total_price()
            payment.save()

            # save order

            Order.ordered = True
            Order.payment = payment
            Order.save()

            messages.success(self.request, 'thanh toan thanh cong ')
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            messages.error(self.request, f"{err.get('messages')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limited")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API

            messages.error(self.request, "Invalid")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            messages.error(self.request, "Not Authen")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "API error")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            messages.error(self.request, "Not Payment")
            return redirect("/")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Exception !!")
            return redirect("/")


def MenClothing(request):
    context = {
        'Items': Men.objects.all()
    }
    return render(request, 'onlineshoop/men-clothing.html', context)

def WomenView(request):
    context = {
        'Items': Women.objects.all()
    }
    return render(request, 'onlineshoop/women.html', context)





















