from django.contrib import admin

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('article', 'client_name', 'client_phone', 'seller', 'status', 'created_at')
    list_filter = ('status', 'seller', 'created_at')
    search_fields = ('client_name', 'client_phone', 'client_email', 'article__title')
