from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.FileField(default='cyn/default.jpg', upload_to='cyn/')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, null=True)
#     email = models.EmailField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.FileField(default='products/default.jpg', upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=200, null=True)
    color = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('detail', kwargs={'pk': self.pk})



RATE_CHOICES =[
            (1,'1-Very Dissatisfied'),
            (2,'2-Dissatisfied'),
            (3,'3-Fair'),
            (4,'4-Satisfied'),
            ( 5,'5-Very Satisfied'),
        ]
class Rating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,
     related_name='rating')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES,max_length=50, null= True)
    comment = models.CharField(max_length=100, null=True)
    posted = models.DateTimeField( auto_now_add=True,null= True)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.user)


class Orderitem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
