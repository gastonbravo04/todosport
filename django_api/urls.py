from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# 🛠️ IMPORTACIÓN CLAVE: Importamos el decorador para eximir de CSRF
from django.views.decorators.csrf import csrf_exempt 

# 🛠️ 1. Definir la vista del TokenObtainPairView con la exención de CSRF
# Esto le dice a Django: No verifiques el token CSRF para esta vista POST.
TokenObtainPairViewExempt = csrf_exempt(TokenObtainPairView.as_view())


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('carrito.urls')), 
    path('api/user/', include('useradmin.urls')), 

    # 🛠️ 2. USAR LA VISTA EXENTA PARA EL LOGIN
    path('api/token/', TokenObtainPairViewExempt, name='token_obtain_pair'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]