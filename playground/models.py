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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

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

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=30)
    birthdate = models.DateTimeField(null=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_CHOICES[0][0])

    def __str__(self):
        return self.email


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_CHOICES[0][0])
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


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
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
