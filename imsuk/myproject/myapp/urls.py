from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home, name='home'),
    path('menu/<int:item_id>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/confirm/', views.order_confirm, name='order_confirm'),
    path('payment/select/', views.payment_select, name='payment_select'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/history/', views.order_history, name='order_history'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/add/<int:restaurant_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:restaurant_id>/', views.remove_favorite, name='remove_favorite'),
    path('address/', views.address_form, name='address_form'),
    path('address/update/', views.address_update, name='address_update'),
    path('check-address/', views.check_address_then_redirect, name='check_address_then_redirect'),
    path('help-center/', views.help_center, name='help_center'),
    path('profile/', views.profile_view, name='profile'),
]






