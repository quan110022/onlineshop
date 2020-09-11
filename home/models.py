from django.db import models
from django.conf import settings
from django.shortcuts import reverse


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
    Item = models.ForeignKey(item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.Item.title}"



class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    Items = models.ManyToManyField(orderitem)
    startdate = models.DateTimeField(auto_now_add=True)
    orderdate = models.DateTimeField()


    def __str__(self):
        return str(self.user.username)


