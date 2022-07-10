from uuid import uuid4

from django.conf import settings
from django.contrib import admin
from django.core import validators
from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # An error occurs here. The '+' tells django not to create a reverse
    # relationship between Collection and Product
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        return self.description


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[validators.MinValueValidator(1)])
    inventory = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B', 'BRONZE'),
        ('S', 'SILVER'),
        ('G', 'GOLD')
    ]

    phone = models.CharField(max_length=30)
    birthdate = models.DateTimeField(null=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_CHOICES[0][0])

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} | {self.user.first_name} {self.user.last_name}"

    # Added this for sorting purposes in admin panel
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_CHOICES[0][0])
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel Orders'),
        ]


class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip = models.CharField(max_length=100, null=True)
    # Set primary key to prevent a one to many field because django will create an id
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.city


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)  # To generate our own unique ID
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
