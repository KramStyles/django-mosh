from django.shortcuts import render

from .models import Customer, Product


def hello(request):
    queryset = Customer.objects.all()
    spec = Product.objects.filter(price__gt=20)
    context = {
        'customers': queryset,
        'spec': spec
    }

    return render(request, 'playground/index.html', context)
