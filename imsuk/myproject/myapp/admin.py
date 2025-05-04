from django.contrib import admin
from .models import (
    User, Store, MenuItem, StoreReview,
    Cart, CartItem, Order, OrderItem, OrderReview
)

# ------------------ ผู้ใช้ ------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'phone_number', 'is_staff']
    search_fields = ['username', 'full_name', 'email']
    list_filter = ['is_staff', 'is_superuser']

# ------------------ ร้านค้า ------------------
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'sale_price', 'original_price', 'open_time', 'close_time', 'delivery_time_estimate']
    list_filter = ['open_time', 'close_time']
    search_fields = ['name', 'address']
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'description', 'address', 'logo', 'banner')
        }),
        ('ราคา & เวลา', {
            'fields': ('original_price', 'sale_price', 'price_range', 'delivery_time_estimate', 'open_time', 'close_time')
        }),
    )

# ------------------ เมนู ------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'price', 'discount_percent', 'is_available']
    list_filter = ['is_available', 'store']
    search_fields = ['name', 'store__name']

# ------------------ รีวิวร้านค้า ------------------
@admin.register(StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    list_display = ['store', 'user', 'rating', 'created_at']
    search_fields = ['store__name', 'user__username']
    list_filter = ['rating', 'created_at']

# ------------------ ตะกร้า ------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity']
    list_filter = ['menu_item__store']

# ------------------ คำสั่งซื้อ ------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'store', 'total', 'status', 'created_at']
    search_fields = ['user__username', 'store__name']
    list_filter = ['status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price']

# ------------------ รีวิวคำสั่งซื้อ ------------------
@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'rating', 'created_at']
    search_fields = ['order__id']
    list_filter = ['rating']
