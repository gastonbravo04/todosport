from django.contrib import admin

from .models import Cliente, Proveedor, Producto, Orden, Carrito

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(Carrito)

# Register your models here.
