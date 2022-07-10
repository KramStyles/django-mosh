from django.urls import path
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router = routers.DefaultRouter()

# Using the default router would make the play url have a page of information and going to products.json would show
# the json data

router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewset)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + product_router.urls + cart_router.urls

# To make use of path
# urlpatterns = [
#     path('', include(router.urls))
# ]


# urlpatterns = [
#     path('hello/', views.hello),
#     path('products/', views.product_list),
#     # path('products/<_id>/', views.product_detail),
#
#     path('collections/', views.collection_list),
#     path('collections/<_id>/', views.collection_list),
#
#     # CLASS BASED URLS
#     path('products/', views.ProductListCreate.as_view()),
#     # path('products/<_id>/', views.ProductDetail.as_view()),
#     path('products/<pk>/', views.ProductDetailApiView.as_view()),
#     # path('products/<id>/', views.ProductDetailApiView.as_view()),
#     path('collections_class/', views.CollectionList.as_view()),  # Better
#     path('collections_class/<pk>/', views.CollectionDetailApiView.as_view()),
# ]
