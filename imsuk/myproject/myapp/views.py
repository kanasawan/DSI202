from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Store, MenuItem

# หน้า Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'login.html', {'timestamp': now().timestamp()})

# ✅ หน้า Home: ดึงร้าน + เมนูอาหารของร้าน
@login_required
def home_view(request):
    stores = Store.objects.all().prefetch_related('menu_items')
    return render(request, 'home.html', {
        'timestamp': now().timestamp(),
        'stores': stores
    })

# รายชื่อร้าน
class StoreListView(ListView):
    model = Store
    template_name = 'store_list.html'
    context_object_name = 'stores'

# รายละเอียดร้าน
class StoreDetailView(DetailView):
    model = Store
    template_name = 'store_detail.html'
    context_object_name = 'store'

# รายละเอียดเมนู
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'menu_item_detail.html'
    context_object_name = 'menu_item'

# หน้า About
def about_view(request):
    return render(request, 'about.html', {'timestamp': now().timestamp()})
