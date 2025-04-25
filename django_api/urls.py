
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('carrito.urls')),  # Cambiá 'tu_app' por el nombre real de tu app
]
