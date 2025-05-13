from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Restaurant, MenuItem, 
    Cart, CartItem, Order, Payment,
    DeliveryAddress, Review, Favorite, Notification,
    PaymentMethod  # ✅ เพิ่ม
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ['name', 'original_price', 'sale_price', 'is_available', 'image', 'description']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'address', 'open_time', 'close_time', 'delivery_fee', 'image_preview']
    list_filter = ['category', 'open_time']
    search_fields = ['name', 'address']
    inlines = [MenuItemInline]
    prepopulated_fields = {'slug': ('name',)}
    fields = ['owner', 'name', 'slug', 'category', 'address', 'open_time', 'close_time', 'phone', 'delivery_fee', 'image']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'original_price', 'sale_price', 'is_available', 'image_preview']
    list_filter = ['restaurant', 'is_available']
    search_fields = ['name', 'description']
    fields = ['restaurant', 'name', 'description', 'original_price', 'sale_price', 'is_available', 'image']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    fields = ['user']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity', 'subtotal']
    search_fields = ['cart__user__username', 'menu_item__name']
    fields = ['cart', 'menu_item', 'quantity']

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'status', 'created_at', 'estimated_delivery_time']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
    fields = ['user', 'cart', 'delivery_address', 'total_price', 'status', 'estimated_delivery_time']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'status', 'paid_at']
    list_filter = ['status', 'method']
    search_fields = ['order__id']
    fields = ['order', 'method', 'status', 'paid_at']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'method_name', 'card_info']
    search_fields = ['user__username', 'method_name']
    fields = ['user', 'method_name', 'card_info']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
    search_fields = ['user__username', 'address']
    fields = ['user', 'address', 'phone']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'restaurant__name']
    fields = ['user', 'restaurant', 'rating', 'comment']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'added_at']
    search_fields = ['user__username', 'restaurant__name']
    fields = ['user', 'restaurant']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'timestamp']
    list_filter = ['is_read']
    search_fields = ['user__username', 'message']
    fields = ['user', 'message', 'is_read']
