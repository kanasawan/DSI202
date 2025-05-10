from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),  # ✅ เส้นทางที่เพิ่ม
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_item, name='remove_item'),

]
