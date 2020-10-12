from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField


# Create your models here.
CATEGORY_CHOISE = (
    ('C', 'coat'),
    ('S', 'shoes'),
    ('T', 'tower'),
    ('O', 'orange'),
)


class item(models.Model):

    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOISE, max_length=1)
    pricesale = models.FloatField(default=0)
    img = models.ImageField(upload_to='images')
    slug = models.SlugField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("home:product", kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("home:addcart", kwargs={
            'slug': self.slug
        })


class orderitem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    Item = models.ForeignKey(item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.Item.title}"
    def total_price(self):
        return self.quantity * self.Item.pricesale
    def total_quantity(self):
        return self.quantity

class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    Items = models.ManyToManyField(orderitem)
    startdate = models.DateTimeField(auto_now_add=True)
    orderdate = models.DateTimeField()
    checkout = models.ForeignKey('check_out', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return str(self.user.username)

    def final_total_price(self):
        total = 0
        for order_item in self.Items.all():
            total += order_item.total_price()
        return total

class check_out(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe = models.CharField(max_length=20)
    amount = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Men(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOISE, max_length=1)
    img = models.ImageField(upload_to='images')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Women(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOISE, max_length=1)
    img = models.ImageField(upload_to='images')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title








