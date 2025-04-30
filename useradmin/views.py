from rest_framework import generics
from .models import Customer
from .serializer import (
    UserSerializer,
    RegisterUserSerializer,
    CustomerSerializer,
    RegisterCustomerSerializer
)

# Registrar un usuario común
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer


# Registrar un cliente (Customer)
class RegisterCustomerView(generics.CreateAPIView):
    serializer_class = RegisterCustomerSerializer


# Ver el perfil de usuario (ya autenticado)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Ver lista de clientes
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
