from django.urls import path
from .views import login_view, home_view, StoreListView, StoreDetailView

urlpatterns = [
    path('', login_view, name='login'),  # ✅ "/" เป็นหน้า login
    path('home/', home_view, name='home'),  # ✅ หน้า home ย้ายมาอยู่ /home/
    path('stores/', StoreListView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
]
