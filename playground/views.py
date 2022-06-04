from django.shortcuts import render, get_object_or_404
from rest_framework import decorators, response, status

from .models import Customer, Product, OrderItem
from . import serializers


def hello(request):
    queryset = Customer.objects.all()
    spec = Product.objects.filter(price__range=[20, 30])
    spec = Product.objects.filter(collection__id__range=(1, 3))
    spec = Product.objects.filter(title__contains='coffee').filter(price__gte=50)

    # communicating with two tables. get distinct products from a table and
    # apply them in another table
    ordered_products = OrderItem.objects.values('product__id').distinct()
    spec = Product.objects.filter(id__in=ordered_products).order_by('title')
    # This would hang the application. because you are selecting related fields individually
    spec = Product.objects.all()
    # Best approach
    spec = Product.objects.select_related('collection').all()

    context = {
        'customers': queryset,
        'spec': spec
    }

    return render(request, 'playground/index.html', context)


@decorators.api_view()
def product_list(request):
    product = Product.objects.all()
    serializer = serializers.ProductSerializer(product, many=True)
    return response.Response(serializer.data)


@decorators.api_view()
def product_detail(request, _id):
    product = get_object_or_404(Product, pk=_id)
    serializer = serializers.ProductSerializer(product)
    return response.Response(serializer.data, status=status.HTTP_200_OK)
