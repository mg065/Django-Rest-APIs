from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    
    ORDER_STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.AutoField(primary_key=True, unique=True)
    order_name = models.CharField(default='', max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=255)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing')

    # def __str__(self):
    #     return self.user.email + ' -> ' + str(self.order_number)