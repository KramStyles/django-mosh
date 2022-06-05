from decimal import Decimal

from rest_framework import serializers

from . import models


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=25)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    original_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='price')
    description = serializers.CharField(max_length=20000)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.StringRelatedField()  # Requires loading product and collections together
    collection = CollectionSerializer()

    def calculate_tax(self, product: models.Product):
        answer = product.price * Decimal(1.14)
        return round(answer, 2)
