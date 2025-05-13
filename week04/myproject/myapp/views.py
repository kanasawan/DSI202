from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import timedelta

from .models import (
    Restaurant, MenuItem, Cart, CartItem, Order,
    Favorite, Notification, DeliveryAddress
)
from .forms import SignUpForm, DeliveryAddressForm


# 1. Home Page – แสดงเมนูทั้งหมด
def home(request):
    query = request.GET.get('q', '')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query, is_available=True)
    else:
        menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'home.html', {'menu_items': menu_items})


# 1.1 ดูรายละเอียดเมนู
def menu_detail(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    restaurant = menu_item.restaurant
    return render(request, 'menu_detail.html', {
        'item': menu_item,
        'restaurant': restaurant
    })


# 2. เพิ่มเมนูลงตะกร้า
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')


# 2.1 ดูตะกร้า
@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = sum(item.subtotal() for item in cart.items.all()) if cart else 0
    return render(request, 'cart.html', {'cart': cart, 'cart_total': total})


# 2.2 ลบรายการในตะกร้า
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')


# 3. กรอกที่อยู่ครั้งแรก
@login_required
def address_form(request):
    try:
        instance = request.user.delivery_address
        return redirect('home')
    except DeliveryAddress.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=instance)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('home')
    else:
        form = DeliveryAddressForm(instance=instance)

    return render(request, 'address_form.html', {'form': form})


# 3.1 แก้ไขที่อยู่
@login_required
def address_update(request):
    instance = DeliveryAddress.objects.filter(user=request.user).first()
    if not instance:
        return redirect('address_form')

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = DeliveryAddressForm(instance=instance)

    return render(request, 'address_form.html', {
        'form': form,
        'editing': True,
    })


# 4. หน้ายืนยันคำสั่งซื้อ
@login_required
def order_confirm(request):
    cart = Cart.objects.get(user=request.user)
    total = sum(item.subtotal() for item in cart.items.all())
    return render(request, 'order_confirm.html', {'cart': cart, 'total': total})


# 4.1 หน้าชำระเงิน
@login_required
def payment_select(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        total = sum(item.subtotal() for item in cart.items.all())

        try:
            address = DeliveryAddress.objects.get(user=request.user)
        except DeliveryAddress.DoesNotExist:
            return redirect('address_form')

        order = Order.objects.create(
            user=request.user,
            cart=cart,
            delivery_address=address,
            total_price=total,
            status='completed',  # ✅ กำหนดเป็นเสร็จสิ้นทันที
            estimated_delivery_time=timedelta(minutes=45)
        )

        cart.items.all().delete()  # ล้างตะกร้า

        Notification.objects.create(
            user=request.user,
            message=f"ระบบได้รับคำสั่งซื้อ #{order.id} แล้ว"
        )

        return redirect('order_detail', order_id=order.id)

    return render(request, 'payment_select.html')


# 5. รายละเอียดคำสั่งซื้อ
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


# 6. ประวัติการสั่งซื้อ
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


# 7. รายการโปรด
@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorites': favorites})


@require_POST
@login_required
def remove_favorite(request, restaurant_id):
    Favorite.objects.filter(user=request.user, restaurant_id=restaurant_id).delete()
    return redirect('home')


@login_required
def add_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    return redirect('favorite_list')


# 8. โปรไฟล์
@login_required
def profile_view(request):
    user = request.user
    default_address = DeliveryAddress.objects.filter(user=user).first()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()

        if not username:
            messages.error(request, "กรุณากรอกชื่อผู้ใช้")
            return redirect('profile')

        user.username = username
        user.email = email
        user.first_name = full_name
        user.save()

        likes = request.POST.getlist('likes')
        allergens = request.POST.getlist('allergens')
        other_like = request.POST.get('other_like', '').strip()
        other_allergen = request.POST.get('other_allergen', '').strip()

        request.session['likes'] = likes + ([other_like] if other_like else [])
        request.session['allergens'] = allergens + ([other_allergen] if other_allergen else [])

        messages.success(request, "บันทึกข้อมูลสำเร็จ")
        return redirect('home')

    return render(request, 'profile.html', {
        'default_address': default_address,
        'filters': ['ของคาว', 'ของหวาน', 'ฟาสต์ฟู้ด', 'เครื่องดื่ม'],
        'allergens': ['ถั่ว', 'อาหารทะเล', 'นม', 'กลูเตน', 'ไข่']
    })


# 9. สมัครสมาชิก
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('address_form')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# 10. ตรวจสอบว่าผู้ใช้มีที่อยู่หรือยัง
@login_required
def check_address_then_redirect(request):
    try:
        request.user.delivery_address
        return redirect('home')
    except DeliveryAddress.DoesNotExist:
        return redirect('address_form')


# 11. ศูนย์ช่วยเหลือ
def help_center(request):
    return render(request, 'help_center.html')
