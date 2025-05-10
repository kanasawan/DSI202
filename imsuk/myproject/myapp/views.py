from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, MenuItem, Cart, CartItem, Order, DeliveryAddress, Payment
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {'restaurants': restaurants})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})

def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'total': 0})
    cart_items = cart.items.all()
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        method = request.POST.get('method')

        delivery = DeliveryAddress.objects.create(user=request.user, address=address, phone=phone)
        total = sum(item.subtotal() for item in cart.items.all())
        order = Order.objects.create(user=request.user, cart=cart, total_price=total, delivery_address=delivery)

        Payment.objects.create(order=order, method=method, status='paid', paid_at=now())

        # ล้างตะกร้า
        cart.items.all().delete()

        return redirect('order_success')

    total = sum(item.subtotal() for item in cart.items.all())
    return render(request, 'checkout.html', {'total': total})

def order_success(request):
    return render(request, 'order_success.html')
