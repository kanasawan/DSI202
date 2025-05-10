from django.urls import path
from .views import (
    login_view,
    home_view,
    about_view,
    StoreListView,
    StoreDetailView,
    MenuItemDetailView
)

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('stores/', StoreListView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu_detail'),
]
