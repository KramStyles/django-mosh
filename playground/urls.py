from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello),
    path('products/', views.product_list),
    path('products/<_id>/', views.product_detail),

    path('collections/', views.collection_list),
    path('collections/<_id>/', views.collection_list),
]
