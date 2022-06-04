from django.shortcuts import render
from rest_framework import decorators, response

from .models import Customer, Product, OrderItem


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
    return response.Response('hello')


@decorators.api_view()
def product_detail(request, _id):
    return response.Response('Hi: '+str(_id))
