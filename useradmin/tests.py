# useradmin/tests.py

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import Client

# Obtenemos el modelo de Usuario que has extendido (AbstractUser)
User = get_user_model() 

class AutenticacionTests(APITestCase):

    def setUp(self):
        """Prepara un usuario normal y un usuario que será cliente."""
        self.username = 'testuser'
        self.password = 'PassSegura123'
        self.email = 'test@example.com'
        self.phone = '123456789'
        self.address = 'Av. Test 101'

        # Creamos el usuario base de Django (AbstractUser)
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            address=self.address,
            phone=self.phone,
        )
        
        # Creamos un segundo usuario para pruebas de seguridad
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass'
        )

    # --- 1. PRUEBAS DE REGISTRO ---

    def test_register_user_success(self):
        """Prueba POST a /api/user/register/user/."""
        url = reverse('register-user')
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'NewPass99',
            'address': 'Calle Nueva',
            'phone': '987654321'
        }
        response = self.client.post(url, data, format='json')
        
        # Debe devolver 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica que el usuario se haya creado en la DB
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_username_fails(self):
        """Prueba que no se pueda registrar un username duplicado."""
        url = reverse('register-user')
        data = {
            'username': self.username, # Ya existe
            'email': 'duplicate@test.com',
            'password': 'NewPass99'
        }
        response = self.client.post(url, data, format='json')
        
        # Debe fallar con 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- 2. PRUEBAS DE LOGIN/LOGOUT (Sesión) ---

    def test_login_success(self):
        """Prueba POST a /api/user/login/ con credenciales válidas."""
        url = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')
        
        # Debe devolver 200 OK y la sesión debe estar activa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que la cookie de sesión esté presente (prueba implícita de login)
        self.assertIn('sessionid', response.cookies) 

    def test_login_failure(self):
        """Prueba POST a /api/user/login/ con contraseña incorrecta."""
        url = reverse('login')
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        # Debe devolver 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid credentials', response.data['error'])

    def test_logout_success(self):
        """Prueba POST a /api/user/logout/ para eliminar la sesión."""
        # 1. Login primero (crear sesión)
        self.client.login(username=self.username, password=self.password)
        
        # 2. Logout
        url = reverse('logout')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Opcional: Verificar que el usuario ya no esté autenticado
        # (Depende de cómo manejes las sesiones, pero 200 OK es suficiente)

    # --- 3. PRUEBAS DE SEGURIDAD Y PERFIL ---

    def test_access_profile_unauthenticated(self):
        """Prueba GET a /api/user/profile/ sin sesión activa."""
        url = reverse('user-profile')
        response = self.client.get(url)

        # Debe fallar con 403 Forbidden o 401 Unauthorized
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def test_access_profile_authenticated(self):
        """Prueba GET a /api/user/profile/ con sesión activa."""
        # 1. Login
        self.client.login(username=self.username, password=self.password)
        
        # 2. Acceso al perfil
        url = reverse('user-profile')
        response = self.client.get(url)
        
        # Debe devolver 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)
        # Confirma que el perfil solo muestra los datos del usuario logueado
    # useradmin/tests.py (Añadir a la clase AutenticacionTests)

    def test_register_with_invalid_email_fails(self):
        """
        Verifica que el registro falle con un email mal formado.
        (Req. TP: Registro de usuario con datos inválidos [email mal formado])
        """
        url = reverse('register-user') 
        data = {
            'username': 'email_fail',
            'email': 'invalid-email', # Valor inválido (sin @ o dominio)
            'password': 'Password1',
            'address': 'Calle',
            'phone': '123'
        }
        response = self.client.post(url, data, format='json')
        
        # Debe fallar con 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Opcional: self.assertIn('email', response.data) # Verifica el mensaje de error

    def test_register_duplicate_email_fails(self):
        """
        Verifica que no se pueda registrar un email que ya existe.
        (Req. TP: Que no se pueda registrar dos usuarios con el mismo email)
        """
        url = reverse('register-user')
        data = {
            'username': 'otro_user',
            'email': self.email, # self.email ('test@example.com') ya fue usado en setUp
            'password': 'Password1',
            'address': 'Calle',
            'phone': '123'
        }
        response = self.client.post(url, data, format='json')
        
        # Debe fallar con 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Opcional: self.assertIn('email', response.data) # Verifica el mensaje de error

    # Nota: Tu método test_register_duplicate_username_fails ya cubre el username.