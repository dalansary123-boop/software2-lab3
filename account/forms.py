from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """نموذج تسجيل مستخدم جديد"""
    email = forms.EmailField(required=True, label='البريد الإلكتروني')
    first_name = forms.CharField(max_length=100, label='الاسم الأول')
    last_name = forms.CharField(max_length=100, label='الاسم الأخير')
    phone = forms.CharField(max_length=20, required=False, label='رقم الهاتف')
    city = forms.CharField(max_length=100, required=False, label='المدينة')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'city']
        labels = {
            'username': 'اسم المستخدم',
            'password1': 'كلمة المرور',
            'password2': 'تأكيد كلمة المرور',
        }


class UserProfileForm(forms.ModelForm):
    """نموذج تعديل الملف الشخصي"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'birth_date']
        labels = {
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'city': 'المدينة',
            'birth_date': 'تاريخ الميلاد',
        }