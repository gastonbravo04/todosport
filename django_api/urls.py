from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('carrito.urls')),  # Cambiá 'tu_app' por el nombre real de tu app
    path('api/user/', include('useradmin.urls')),  # Rutas de autenticación y usuarios

# NUEVAS RUTAS JWT para obtener y refrescar tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
