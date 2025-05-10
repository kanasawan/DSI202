from django import forms
from .models import UserProfile

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address','phone']