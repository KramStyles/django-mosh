from decimal import Decimal

from rest_framework import serializers

from . import models


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField(max_length=20000)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: models.Product):
        return product.price * Decimal(1.2)
