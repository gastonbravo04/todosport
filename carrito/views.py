from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response 
from .models import User, Supplier, Product, Customer, Order, Cart
from .serializer import UserSerializer, SupplierSerializer, ProductSerializer, CustomerSerializer, OrderSerializer, CartSerializer

# Nota: Asumo que todos los modelos están en .models

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Lógica de Permisos: Navegación pública, Edición privada (IsAdminUser)
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()] 


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # CORRECCIÓN CLAVE: Sobrescribir get_queryset para filtrar órdenes propias
    def get_queryset(self):
        # NOTA: Usamos getattr() para verificar si el objeto Customer tiene el atributo
        # is_superuser, resolviendo el AttributeError.
        
        # 1. Verificación de Administrador/Superusuario
        # Si el objeto autenticado (Customer) tiene el atributo y es True, o es staff.
        is_admin =  getattr(self.request.user, 'is_superuser', False) or \
                    getattr(self.request.user, 'is_staff', False)
        
        if is_admin: 
            return Order.objects.all()

        # 2. Si no es admin, filtra por el cliente asociado.
        try:
            # Buscamos el objeto Customer por el username del usuario autenticado
            cliente_autenticado = Customer.objects.get(username=self.request.user.username)
            # Filtramos las órdenes por ese cliente (Customer)
            return Order.objects.filter(customer=cliente_autenticado)
        except Customer.DoesNotExist:
            # Si el usuario no está asociado a un Customer, no ve nada.
            return Order.objects.none()

    # LÓGICA DE CHECKOUT: Asigna cliente y campos obligatorios (Resuelve el 400 != 201)
    def perform_create(self, serializer):
        try:
            # 1. Obtener el Customer (Cliente) autenticado
            cliente_autenticado = Customer.objects.get(username=self.request.user.username)
        except Customer.DoesNotExist:
            raise Exception("Customer no encontrado para el usuario autenticado.")

        # 2. Guardar la orden, asignando los campos requeridos
        serializer.save(
            customer=cliente_autenticado,
            total=0.00,  # Valor de inicialización forzado
            status='Pending' # Estado inicial forzado
        )

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    