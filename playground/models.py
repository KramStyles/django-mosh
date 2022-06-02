from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B', 'BRONZE'),
        ('S', 'SILVER'),
        ('G', 'GOLD')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=30)
    birthdate = models.DateTimeField(null=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_CHOICES[0][0])


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(choices=PAYMENT_CHOICES, default=PAYMENT_CHOICES[0][0])
