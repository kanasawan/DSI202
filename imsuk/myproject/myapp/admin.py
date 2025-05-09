from django.contrib import admin
from .models import (
    Store,
    MenuItem,
    Address,
    PaymentMethod,
    Order,
    OrderItem,
    FavoriteStore
)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'original_price', 'sale_price', 'available_time_start', 'available_time_end')
    list_filter = ('store',)
    search_fields = ('name', 'description')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'province', 'is_default')
    search_fields = ('user__username', 'name', 'province')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'detail')
    search_fields = ('user__username', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_paid', 'total_price')
    list_filter = ('is_paid',)
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')

@admin.register(FavoriteStore)
class FavoriteStoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'store')
    search_fields = ('user__username', 'store__name')
