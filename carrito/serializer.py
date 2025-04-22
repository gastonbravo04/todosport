from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all_' 


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '_all_'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = '_all_'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '_all_'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '_all_'