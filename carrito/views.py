from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response 
from .models import User, Supplier, Product, Customer, Order, OrderItem, Cart
from .serializer import UserSerializer, SupplierSerializer, ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, CartSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsStaffOrReadOnly
import time

# Nota: Asumo que todos los modelos están en .models

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(ModelViewSet):
    # El modelo define `product_id` como primary key — no existe `id`.
    # Ordenamos por `product_id` para evitar FieldError al cargar las rutas en runserver.
    queryset = Product.objects.all().order_by('product_id')
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]

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
    # Permitimos que cualquiera cree una orden (checkout de invitado). Lectura puede restringirse por get_queryset.
    permission_classes = [permissions.AllowAny]

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
        """
        Crea una orden asignando el cliente autenticado si existe.
        Si no hay usuario autenticado, crea/usa un "cliente invitado" a partir de los datos enviados.
        Usa los valores de total/status que envíe el frontend; si faltan, aplica defaults.
        """
        # 1) Intentar resolver un Customer según el usuario autenticado
        customer_obj = None
        username = getattr(self.request.user, 'username', '') or ''
        if username:
            try:
                customer_obj = Customer.objects.get(username=username)
            except Customer.DoesNotExist:
                customer_obj = None

        # 2) Si no hay Customer autenticado, crear/usar uno temporal a partir del payload
        if customer_obj is None:
            data = self.request.data if hasattr(self.request, 'data') else {}
            base_username = data.get('username') or f"guest_{int(time.time())}"
            # Aseguramos unicidad en username/email mínimos
            safe_username = f"{base_username}"
            # Email opcional: si no viene, generamos uno sintético único
            email = data.get('email') or f"{safe_username}@guest.local"
            first_name = data.get('first_name') or data.get('firstName') or 'Invitado'
            last_name = data.get('last_name') or data.get('lastName') or ''
            address = data.get('address') or ''
            phone = data.get('phone') or ''

            # get_or_create para evitar romper unicidades si se reintenta
            customer_obj, _ = Customer.objects.get_or_create(
                username=safe_username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'address': address,
                    'phone': phone,
                    # la password no es utilizada para invitados, se setea por defecto en modelo
                }
            )

        # 3) Tomar total/status del payload si se pasan; sino defaults
        req_total = self.request.data.get('total', 0.00)
        try:
            req_total = float(req_total)
        except Exception:
            req_total = 0.00
        req_status = self.request.data.get('status', 'Pending')
        shipping = self.request.data.get('shipping', 0.00)
        try:
            shipping = float(shipping)
        except Exception:
            shipping = 0.00
        payment_method = self.request.data.get('payment_method', '')
        card_type = self.request.data.get('card_type')
        card_brand = self.request.data.get('card_brand')
        installments = int(self.request.data.get('installments', 1) or 1)

        # Guardar la orden base
        order = serializer.save(
            customer=customer_obj,
            total=req_total,
            status=req_status,
            shipping=shipping,
            payment_method=payment_method,
            card_type=card_type,
            card_brand=card_brand,
            installments=installments,
        )

        # Crear ítems si fueron provistos
        items = self.request.data.get('items') or []
        computed_total = 0.0
        for it in items:
            try:
                product_id = it.get('product_id') or it.get('product')
                if product_id is None:
                    continue
                product = Product.objects.get(product_id=product_id)
                qty = int(it.get('quantity', 1))
                unit_price = float(it.get('unit_price', product.price))
                subtotal = unit_price * qty
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )
                computed_total += subtotal
            except Exception:
                # Omitimos ítems inválidos sin romper el flujo
                continue

        # Si no enviaron total, recalculamos (productos + envío)
        if not self.request.data.get('total'):
            order.total = round(computed_total + shipping, 2)
            order.save(update_fields=['total'])

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
