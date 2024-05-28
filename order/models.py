from django.db import models
from account.models import UserBase
from store.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(UserBase, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=15, null=False)
    postcode = models.CharField(max_length=12, null=False)
    town_city = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)

    shipped = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.created_at)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orderitems', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)