from django.contrib import admin

from .models import Customer, Supplier, Product, Order, Cart

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)

# Register your models here.
