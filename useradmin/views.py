from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from .models import Customer
from .serializer import (
    UserSerializer,
    RegisterUserSerializer,
    CustomerSerializer,
    RegisterCustomerSerializer,
    ChangePasswordSerializer
)

# --- Registro ---

# Registrar un usuario común
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]  # <- público

# Registrar un cliente (Customer)
class RegisterCustomerView(generics.CreateAPIView):
    serializer_class = RegisterCustomerSerializer
    permission_classes = [permissions.AllowAny]  # <- público

# --- Perfil y Listado ---

# Ver el perfil del usuario autenticado
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# Ver lista de clientes
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# --- Login y Logout ---

# Login de usuario
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]  # <- público
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Crea la cookie de sesión
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Logout de usuario
class LogoutView(views.APIView):
    permission_classes = [permissions.AllowAny]  # <- público
    def post(self, request):
        logout(request)  # Elimina la sesión
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

# --- Cambio de contraseña ---

# Cambio de contraseña
class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(ser.validated_data['old_password']):
            return Response({'detail': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(ser.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed'}, status=status.HTTP_200_OK)
