from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id','email','phone_number','full_name','is_staff','is_superuser','is_active')
    search_fields = ('email','phone_number','full_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email','phone_number','password')}),
        ('Personal', {'fields': ('full_name','address')}),
        ('Permissions', {'fields': ('is_staff','is_superuser','is_active','is_customer','is_farmer')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email','phone_number','full_name','password')}),
    )
