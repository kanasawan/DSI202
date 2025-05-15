from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DeliveryAddress

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            self.fields[field].help_text = None

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'ระบุที่อยู่โดยละเอียด'}),
            'phone': forms.TextInput(attrs={'placeholder': 'เช่น 08x-xxx-xxxx'}),
        }

# ✅ เพิ่ม alias ตรงนี้
SignUpForm = CustomSignupForm
