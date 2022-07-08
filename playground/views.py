from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404
from rest_framework import decorators, response, status, generics, views, viewsets, filters, pagination, mixins

from .models import Customer, Product, OrderItem, Collection, Review, Cart
from . import serializers
from .filters import ProductFilter


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.select_related('collection').all()


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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    # filterset_fields = ['collection_id']
    ordering_fields = ['price']
    search_fields = ['title', 'description']
    pagination_class = pagination.LimitOffsetPagination

    # def get_queryset(self):
    #     """
    #     We want to apply filtering to this list without filter_backends
    #     """
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id:
    #         queryset = queryset.filter(collection_id=collection_id)
    #
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        products = OrderItem.objects.filter(product_id=kwargs['pk'])
        if products.count() > 0:
            return response.Response({'error': "This particular information cannot be deleted due to foreign key constraints!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(ProductViewSet, self).destroy(request, *args, **kwargs)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if product.order_items.count() > 0:
            serializer = self.serializer_class(product)
            return response.Response({'error': "This particular information cannot be deleted due to foreign key constraints!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(generics.GenericAPIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, _id):
        product = get_object_or_404(Product, pk=_id)
        serializer = self.serializer_class(product)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, _id):
        product = get_object_or_404(Product, pk=_id)
        serializer = self.serializer_class(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, _id):
        product = get_object_or_404(Product, pk=_id)
        if product.order_items.count() > 0:
            serializer = self.serializer_class(product)
            return response.Response({'error': "This particular information cannot be deleted due to foreign key constraints!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


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


class CollectionViewset(viewsets.ModelViewSet):
    """
    As you can see we are having duplications in all the codes dealing with collections.
    i.e queryset and seralizer_class. The viewset helps to prevent such duplications.
    We are supposed to move everything inside it and create routes to seperate them
    """
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = serializers.CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = OrderItem.objects.filter(product_id=kwargs['pk'])
        if collection.count() > 0:
            return response.Response({'error': "Collection cannot be deleted because it includes one or more products"})
        return super(CollectionViewset, self).destroy(request, *args, **kwargs)


class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = serializers.CollectionSerializer


class CollectionDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = serializers.CollectionSerializer

    def delete(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])

        if collection.products.count() > 0:
            return response.Response({'error': "Collection cannot be deleted because it includes one or more products"})
        collection.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        """
        Using this in place of objects.all() so we can return reviews associated to a particular product
        """
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class CartViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
