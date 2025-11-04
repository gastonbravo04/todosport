from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response 
from .models import Product, Customer, Order, OrderItem, Cart
from django.db import transaction
from .serializer import ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, CartSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsStaffOrReadOnly
import time

# Nota: Asumo que todos los modelos están en .models

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
        Checkout flow:
        - Asigna el Customer autenticado (buscando por username en self.request.user).
        - Crea la Order con total=0.00 y status='Pending'.
        - Mueve/vincula todos los ítems del `Cart` a `OrderItem` (no vuelve a tocar stock,
        ya que el descuento de stock ocurre al crear los `Cart` items en `CartSerializer`).
        - Vacía el carrito del usuario (aquí se borran los registros de `Cart`).
        Todo dentro de una transacción atómica.
        """
        # Resolver customer por username del request.user
        customer_obj = None
        username = getattr(self.request.user, 'username', '') or ''
        if username:
            try:
                customer_obj = Customer.objects.get(username=username)
            except Customer.DoesNotExist:
                customer_obj = None

        # Si no existe un Customer autenticado, creamos/obtenemos un cliente "guest"
        if customer_obj is None:
            data = self.request.data if hasattr(self.request, 'data') else {}
            base_username = data.get('username') or f"guest_{int(time.time())}"
            safe_username = base_username
            email = data.get('email') or f"{safe_username}@guest.local"
            first_name = data.get('first_name') or data.get('firstName') or 'Invitado'
            last_name = data.get('last_name') or data.get('lastName') or ''
            address = data.get('address') or ''
            phone = data.get('phone') or ''

            customer_obj, _ = Customer.objects.get_or_create(
                username=safe_username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'address': address,
                    'phone': phone,
                }
            )

        # Forzamos que toda orden creada vía checkout se registre como 'Paid'.
        # Si en el futuro se integra un gateway de pagos, cambiar esta lógica
        # para validar el pago antes de marcar la orden como pagada.
        initial_status = 'Pagado'

        # Crear la orden base con los valores requeridos por la especificación
        with transaction.atomic():
            order = serializer.save(
                customer=customer_obj,
                total=0.00,
                status=initial_status,
            )

            # Obtener los items del carrito (nota: el modelo Cart no tiene relación con Customer
            # en este proyecto, así que se toman todos los items del carrito existentes). Si no hay
            # items en la tabla Cart (por ejemplo cuando el frontend usa localStorage), procesamos
            # los items enviados en request.data y allí descontamos stock.
            cart_items = Cart.objects.all()

            computed_total = 0.0
            total_shipping = 0.0

            if cart_items.exists():
                for c in cart_items:
                    try:
                        OrderItem.objects.create(
                            order=order,
                            product=c.product,
                            quantity=c.quantity,
                            unit_price=c.unit_price,
                            subtotal=c.total,
                        )
                        computed_total += float(c.total)
                        total_shipping += float(c.shipping or 0)
                    except Exception:
                        # Omitir ítems inválidos sin romper la creación de la orden
                        continue

                # Actualizar total (productos + envío) si corresponde
                order.total = round(computed_total + total_shipping, 2)
                order.save(update_fields=['total'])

                # Vaciar el carrito
                cart_items.delete()
            else:
                # No hay items en la tabla Cart: tomamos items desde el payload y descontamos stock aquí.
                items = self.request.data.get('items') or []
                for it in items:
                    try:
                        product_id = it.get('product_id') or it.get('product')
                        if product_id is None:
                            continue
                        product = Product.objects.get(product_id=product_id)
                        qty = int(it.get('quantity', 1))

                        # Validar stock
                        if product.stock < qty:
                            raise serializers.ValidationError(
                                f"No hay stock suficiente para {product.name}. Disponible: {product.stock}, solicitado: {qty}"
                            )

                        # Descontar stock ahora (no existe Cart que ya lo haya hecho)
                        product.stock -= qty
                        product.save()

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
                    except serializers.ValidationError:
                        # Re-raise para que create() lo capture y devuelva detail al frontend
                        raise
                    except Exception:
                        # Omitimos ítems inválidos pero continuamos con el resto
                        continue

                # Guardar total calculado
                order.total = round(computed_total + total_shipping, 2)
                order.save(update_fields=['total'])

    def create(self, request, *args, **kwargs):
        """Override create to return a JSON error message when something fails
        (helps the frontend show a useful alert instead of a generic failure).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            # Log traceback to console (runserver) and return readable message
            import traceback
            traceback.print_exc()
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Re-serializar la orden recién creada para incluir campos relacionados
        try:
            created_order = Order.objects.get(pk=serializer.instance.pk)
            out_data = OrderSerializer(created_order, context={'request': request}).data
        except Exception:
            out_data = serializer.data

        headers = self.get_success_headers(out_data)
        return Response(out_data, status=status.HTTP_201_CREATED, headers=headers)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    """API para CRUD de items de carrito. Al crear un Cart item, el CartSerializer
    ya se encarga de descontar el stock del producto.
    """
    queryset = Cart.objects.all().order_by('cart_id')
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]
