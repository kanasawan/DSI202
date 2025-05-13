from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DeliveryAddress

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="อีเมล")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['address', 'phone']
        labels = {
            'address': 'ที่อยู่จัดส่ง',
            'phone': 'เบอร์โทรศัพท์'
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'})
        }
