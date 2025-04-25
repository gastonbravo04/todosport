
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', admin.site.urls),  # Cambiá 'tu_app' por el nombre real de tu app
]
