from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello),
    path('products/', views.product_list),
    path('products/<id>/', views.product_detail),
]
