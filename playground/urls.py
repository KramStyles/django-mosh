from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('products/', views.product_list),
    # path('products/<_id>/', views.product_detail),

    path('collections/', views.collection_list),
    path('collections/<_id>/', views.collection_list),

    # CLASS BASED URLS
    path('products/', views.ProductListCreate.as_view()),
    # path('products/<_id>/', views.ProductDetail.as_view()),
    path('products/<pk>/', views.ProductDetailApiView.as_view()),
    # path('products/<id>/', views.ProductDetailApiView.as_view()),
    path('collections_class/', views.CollectionList.as_view()),  # Better
    path('collections_class/<pk>/', views.CollectionDetailApiView.as_view()),
]
