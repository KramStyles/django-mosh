from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from rest_framework import decorators, response, status, generics

from .models import Customer, Product, OrderItem, Collection
from . import serializers


class ProductList(generics.GenericAPIView):
    def get(self, request):
        product = Product.objects.select_related('collection').all()
        serializer = serializers.ProductSerializer(product, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


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


@decorators.api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        product = Product.objects.select_related('collection').all()
        serializer = serializers.ProductSerializer(product, many=True)
        return response.Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


@decorators.api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, _id):
    product = get_object_or_404(Product, pk=_id)
    if request.method == 'GET':
        serializer = serializers.ProductSerializer(product)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = serializers.ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        # to prevent exceptions that come from orderitems (check the orderItem class) foreign key
        # The name order_items is from the related field
        if product.order_items.count() > 0:
            serializer = serializers.ProductSerializer(product)
            return response.Response({'error': "This particular information cannot be deleted due to foreign key constraints!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


@decorators.api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = serializers.CollectionSerializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = serializers.CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


@decorators.api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    # Called products instead of product because of related name in product.collection
    if request.method == 'GET':
        serializer = serializers.CollectionSerializer(collection)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = serializers.CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return response.Response({'error': "Collection cannot be deleted because it includes one or more products"})
        collection.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
