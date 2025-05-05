# myapp/urls.py
from django.urls import path
from .views import home_view, StoreListView, StoreDetailView

urlpatterns = [
    path('', home_view, name='home'),
    path('stores/', StoreListView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
]
