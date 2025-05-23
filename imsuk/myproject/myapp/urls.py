from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Google OAuth
    path('auth/', include('social_django.urls', namespace='social')),  

    # User Views
    path('home/', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),

    # Menu + Cart + Orders
    path('menu/<int:item_id>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/confirm/', views.order_confirm, name='order_confirm'),
    path('payment/select/', views.payment_select, name='payment_select'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/history/', views.order_history, name='order_history'),

    # Favorites
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/add/<int:restaurant_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:restaurant_id>/', views.remove_favorite, name='remove_favorite'),

    # Address
    path('address/', views.address_form, name='address_form'),
    path('address/update/', views.address_update, name='address_update'),
    path('check-address/', views.check_address_then_redirect, name='check_address_then_redirect'),

    # Help
    path('help-center/', views.help_center, name='help_center'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
