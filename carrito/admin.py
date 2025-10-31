from django.contrib import admin

from .models import Customer, Supplier, Product, Order, OrderItem, Cart

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)

# Register your models here.
