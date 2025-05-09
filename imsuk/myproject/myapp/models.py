from django.db import models
from django.contrib.auth.models import User
class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)  # เช่น ของหวาน, ของคาว
    image = models.ImageField(upload_to='stores/', blank=True)
    def __str__(self):
        return self.name
class MenuItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    image = models.ImageField(upload_to='menu_items/', blank=True)
    def __str__(self):
        return f"{self.name} ({self.store.name})"
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    address = models.TextField()
    subdistrict = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    def __str__(self):
        return self.name
class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name} ({self.user.username})"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"Order #{self.pk}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
class FavoriteStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'store')
    def __str__(self):
        return f"{self.user.username} ❤️ {self.store.name}"
