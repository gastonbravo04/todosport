from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # agrega tus campos extra si existen
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields': ('address', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('address', 'phone')}),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
