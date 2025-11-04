from rest_framework import serializers
from .models import User, Supplier, Product, Customer, Order, OrderItem, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
class OrderItemSerializer(serializers.ModelSerializer):
    # Serializamos el producto embebido para que el frontend pueda mostrar nombre/imagen
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # CORRECCIÓN CLAVE para el checkout (soluciona el 400):
    # Hacemos total y status opcionales para que la vista pueda asignarlos.
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    status = serializers.CharField(max_length=100, required=False)
    shipping = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payment_method = serializers.CharField(max_length=50, required=False)
    card_type = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    card_brand = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    installments = serializers.IntegerField(required=False)
    
    # El campo customer se hace read_only ya que la vista lo asigna desde el usuario autenticado.
    # Serializamos customer completo para que el frontend reciba todos sus datos
    customer = CustomerSerializer(read_only=True)
    # Incluir ítems de la orden embebidos para que el frontend muestre detalle
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        if product.stock < quantity:
            raise serializers.ValidationError("No hay stock suficiente para este producto.")

        # Descontar stock (LÓGICA CORE TP)
        product.stock -= quantity
        product.save()

        return super().create(validated_data)