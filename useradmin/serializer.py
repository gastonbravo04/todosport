from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'address', 'phone']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'address', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    # CORRECCIÓN CLAVE: Añadir validación de unicidad de email
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            # Devuelve 400 Bad Request con un mensaje específico
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user']


class RegisterCustomerSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()

    class Meta:
        model = Customer
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user)
        return customer
