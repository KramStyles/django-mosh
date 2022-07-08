from decimal import Decimal

from rest_framework import serializers

from . import models


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=25)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'original_price', 'price_with_tax', 'collection', 'description', 'slug', 'inventory']

    original_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # collection = serializers.StringRelatedField()  # Requires loading product and collections together
    # collection = CollectionSerializer()

    def calculate_tax(self, product: models.Product):
        answer = product.price * Decimal(1.14)
        return round(answer, 2)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'


class SimpleProductSerializer(ProductSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'price', 'price_with_tax']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart_item: models.CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    all_total_price = serializers.SerializerMethodField()

    def get_all_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'all_total_price']
