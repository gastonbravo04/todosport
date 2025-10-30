from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

