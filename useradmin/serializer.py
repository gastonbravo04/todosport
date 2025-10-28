from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer
# Nota: La validación de formato de email ya la incluye AbstractUser
from django.core.exceptions import ValidationError 

User = get_user_model() 

# --- 1. UserSerializer (Para Perfil y Lectura) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'address', 'phone']


# --- 2. RegisterUserSerializer (Crea el Usuario Hasheado) ---
class RegisterUserSerializer(serializers.ModelSerializer):
    # Campo para ingresar la contraseña (solo escritura, nunca se muestra)
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'address', 'phone']

    # Lógica de Creación: Usa User.objects.create_user para hashear la contraseña
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        # Usamos el manager de Django para crear y hashear la password
        user = User.objects.create_user(**validated_data) 
        
        user.set_password(password)
        user.save()
        
        return user
        
    # Lógica de Validación: Verifica la unicidad del email
    def validate_email(self, value):
        # La validación de formato ya está implícita en Django, aquí verificamos unicidad
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value


# --- 3. CustomerSerializer (Lectura de Cliente) ---
class CustomerSerializer(serializers.ModelSerializer):
    # Serializa el objeto User completo dentro del Customer
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Customer
        fields = ['id', 'user']


# --- 4. RegisterCustomerSerializer (Creación Anidada y Final) ---
class RegisterCustomerSerializer(serializers.ModelSerializer):
    # Usa el serializer de registro del User de forma anidada
    user = RegisterUserSerializer() 

    class Meta:
        model = Customer
        fields = ['user']

    # LÓGICA DE CREACIÓN FINAL (CREA USER Y CUSTOMER)
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # 1. Crea el User: Llama al método create() del serializer anidado.
        # Creamos una instancia temporal del serializer para llamar a su método create.
        user_serializer = RegisterUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        # 2. Crea el Customer y lo asocia al User
        customer = Customer.objects.create(user=user, **validated_data)
        return customer