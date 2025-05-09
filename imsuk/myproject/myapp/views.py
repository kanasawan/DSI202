from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Store
from datetime import datetime

def home_view(request):
    return render(request, 'home.html', {
        'timestamp': datetime.now().timestamp()  # ใช้สำหรับ refresh รูปโลโก้
    })

class StoreListView(ListView):
    model = Store
    template_name = 'store_list.html'
    context_object_name = 'stores'

class StoreDetailView(DetailView):
    model = Store
    template_name = 'store_detail.html'
    context_object_name = 'store'
