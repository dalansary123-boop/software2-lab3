# from django.db import models

# Create your models here.
from django.db import models  # استيراد وحدة الجداول والقواعد من Django

class Product(models.Model):  # تعريف نموذج جدول المنتجات في قاعدة البيانات
    name = models.CharField(max_length=100, verbose_name="اسم المنتج")  # حقل نصي لاسم المنتج بحد أقصى 100 حرف
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر")  # حقل عشري لسعر المنتج
    category = models.CharField(max_length=50, verbose_name="التصنيف")  # حقل نصي لتصنيف المنتج (مثل: عناية، هدايا)
    image_url = models.URLField(verbose_name="رابط الصورة")  # حقل لتخزين رابط صورة المنتج

    def __str__(self):  # دالة نصية لتمثيل المنتج باسمه داخل لوحة التحكم
        return self.name  # إرجاع اسم المنتج عند طلب الكائن كـ نص
    from django.db import models

# 1. نموذج المنتجات (العطور)
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المنتج")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر")
    category = models.CharField(max_length=50, verbose_name="التصنيف")
    image_url = models.URLField(verbose_name="رابط الصورة", blank=True, null=True)

    def __str__(self):
        return self.name

# 2. نموذج العملاء (مستوحى من جدول العملاء في الواجهة)
class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم العميل")
    age = models.IntegerField(verbose_name="العمر", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")

    def __str__(self):
        return self.name

# 3. نموذج الطلبات (مستوحى من جدول إدارة الطلبات)
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'قيد التجهيز'),
        ('Completed', 'مكتمل'),
    ]

    product_name = models.CharField(max_length=100, verbose_name="اسم العطر")
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address = models.CharField(max_length=200, verbose_name="العنوان")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ الطلب")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="الحالة")

    def __str__(self):
        return f"طلب #{self.id} - {self.customer_name}"
