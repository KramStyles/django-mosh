from django.shortcuts import render

from .models import Customer


def hello(request):
    queryset = Customer.objects.all()
    context = {
        'customers': queryset
    }
    return render(request, 'playground/index.html', context)
