from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """نموذج ملف المستخدم الشخصي"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    phone = models.CharField(max_length=20, blank=True, verbose_name='رقم الهاتف')
    address = models.TextField(blank=True, verbose_name='العنوان')
    city = models.CharField(max_length=100, blank=True, verbose_name='المدينة')
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاريخ الميلاد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'ملف مستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
        
    def __str__(self):
        return self.user.username

    def get_full_name(self):
        """إرجاع الاسم الكامل"""
        return self.user.get_full_name() or self.user.username