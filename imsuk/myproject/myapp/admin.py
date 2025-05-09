from django.contrib import admin
from .models import Store, MenuItem, Address, PaymentMethod, Order, OrderItem, FavoriteStore
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'original_price', 'sale_price']
    list_filter = ['store']
    search_fields = ['name']
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'province', 'is_default']
    list_filter = ['province']
    search_fields = ['name', 'user__username']
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    search_fields = ['name', 'user__username']
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_paid', 'total_price']
    list_filter = ['is_paid']
    inlines = [OrderItemInline]
@admin.register(FavoriteStore)
class FavoriteStoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'store']
    search_fields = ['user__username', 'store__name']