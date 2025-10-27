from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
# Importamos modelos desde la misma app
from .models import Customer, Product, Cart, Order 

class CarritoApiTests(APITestCase):
    
    def setUp(self):
        """Configuración: Crea un cliente y un producto con stock inicial."""
        # 1. Creamos un Customer de prueba para la autenticación
        self.customer = Customer.objects.create(
            username='cliente_test', 
            email='cliente@test.com',
            first_name='Cliente', 
            last_name='Test', 
            address='Calle Falsa 123', 
            phone='123456789'
            # ADVERTENCIA: Se requiere que el modelo tenga métodos de password para un login real
        )
        # 2. Creamos un Producto de prueba con stock inicial
        self.product = Product.objects.create(
            product_id=100,
            name='Camiseta',
            description='camiseta oficial',
            price=50000.00,
            stock=5, # Stock inicial = 5
            category='Camisetas',
            brand='Test'
        )
        # 3. Forzamos la autenticación (simula el login obligatorio para comprar)
        self.client.force_authenticate(user=self.customer)
        
    def test_add_to_cart_and_reduce_stock(self):
        """
        Prueba 1: Verificar el descuento de stock al agregar un producto al carrito. (CORE TP)
        """
        stock_antes = self.product.stock # 5
        url = reverse('cart-list') # Nombre generado por DefaultRouter
        
        data = {
            'product': self.product.product_id,
            'quantity': 2, # Cantidad a comprar
            'unit_price': self.product.price,
            'total': self.product.price * 2,
            'shipping': 500.00
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # VERIFICACIÓN CORE (Funciones CRUD sobre Stocks: Update)
        self.product.refresh_from_db()
        # El stock debe ser 5 - 2 = 3
        self.assertEqual(self.product.stock, stock_antes - 2) 

    def test_add_to_cart_exceeds_stock(self):
        """
        Prueba 2: Verificar que el sistema no permite agregar más que el stock disponible.
        """
        url = reverse('cart-list')
        data = {
            'product': self.product.product_id,
            'quantity': 10, # Mayor al stock disponible (5)
            'unit_price': self.product.price,
            'total': self.product.price * 10,
            'shipping': 500.00
        }
        
        response = self.client.post(url, data, format='json')
        
        # Debe fallar con 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_order_from_cart_success(self):
        """
        Prueba 3: Verificar que la creación del pedido (checkout) sea exitosa.
        (Requiere la lógica perform_create en OrderViewSet y OrderSerializer flexible)
        """
        # 1. Preparación: Crear un ítem en el carrito (descuenta 1 unidad de stock)
        Cart.objects.create(
            product=self.product, 
            quantity=1, 
            unit_price=self.product.price,
            total=self.product.price * 1,
            shipping=0.00
        )
        self.product.refresh_from_db()
        stock_despues_cart = self.product.stock # 4
        
        # 2. Crear Pedido (POST al endpoint de orders)
        url_order = reverse('order-list') 
        response = self.client.post(url_order) 
        
        # 3. Verificación: Debe ser 201 Created gracias a la lógica perform_create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        
        # 4. Verificar stock final (no debe haber nuevo descuento)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, stock_despues_cart)
    # carrito/tests.py (Añadir a CarritoApiTests)

    def test_user_can_only_view_own_orders_list(self):
        """
        Prueba 4: Verifica que el usuario solo vea sus propias órdenes (Seguridad).
        (Requiere el filtro get_queryset en OrderViewSet).
        """
        # 1. Crear un segundo cliente (el "otro" usuario)
        other_customer = Customer.objects.create(
            username='adrian',
            email='adrian@gmail.com',
            first_name='Adrian',
            last_name='Donaire',
            phone='260456789',
        )
        # 2. Crear una orden para el cliente autenticado (self.customer)
        Order.objects.create(customer=self.customer, total=10.00, status='Pending')
        # 3. Crear una orden para el otro cliente (la orden prohibida)
        Order.objects.create(customer=other_customer, total=20.00, status='Pending')

        # 4. Iniciar sesión como self.customer (ya está hecho en setUp, pero lo repetimos por claridad)
        self.client.force_authenticate(user=self.customer)
        
        # 5. Intentar ver la lista de órdenes
        url_order_list = reverse('order-list') 
        response_list = self.client.get(url_order_list)
        
        # Verificación CORE: Debe devolver 200 OK
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        # Debe ver solo 1 orden (la suya), NO las dos.
        self.assertEqual(len(response_list.data), 1) 
        
        # Verificación adicional: Asegurar que el ID del cliente de la orden sea el correcto
        self.assertEqual(response_list.data[0]['customer'], self.customer.User_id)