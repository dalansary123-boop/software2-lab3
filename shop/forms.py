from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order





class OrderForm(forms.ModelForm):
    """نموذج إتمام الطلب"""
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'city']
        labels = {
            'full_name': 'الاسم الكامل',
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'city': 'المدينة',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }