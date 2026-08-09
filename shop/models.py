from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """فئات العطور"""
    name = models.CharField(max_length=100, verbose_name='اسم الفئة')
    description = models.TextField(blank=True, verbose_name='وصف الفئة')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['name']

    def str(self):
        return self.name


class Perfume(models.Model):
    """نموذج العطر"""
    name = models.CharField(max_length=200, verbose_name='اسم العطر')
    brand = models.CharField(max_length=100, verbose_name='الماركة')
    description = models.TextField(verbose_name='وصف العطر')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='السعر القديم')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='perfumes', verbose_name='الفئة')
    image = models.ImageField(upload_to='perfumes/', blank=True, null=True, verbose_name='صورة العطر')
    stock = models.PositiveIntegerField(default=10, verbose_name='الكمية المتوفرة')
    is_featured = models.BooleanField(default=False, verbose_name='مميز')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'عطر'
        verbose_name_plural = 'العطور'
        ordering = ['-created_at']

    def str(self):
        return f"{self.name} - {self.brand}"

    def discount_percentage(self):
        """حساب نسبة الخصم"""
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


class CartItem(models.Model):
    """عنصر في سلة التسوق"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, verbose_name='العطر')
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'عنصر السلة'
        verbose_name_plural = 'عناصر السلة'

    def total_price(self):
        return self.quantity * self.perfume.price

    def str(self):
        return f"{self.perfume.name} ({self.quantity})"


class Order(models.Model):
    """نموذج الطلب"""
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    full_name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    address = models.TextField(verbose_name='العنوان')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ الإجمالي')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='حالة الطلب')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def str(self):
        return f"طلب #{self.id}"


class OrderItem(models.Model):
    """عنصر في الطلب"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='الطلب')
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, verbose_name='العطر')
    quantity = models.PositiveIntegerField(verbose_name='الكمية')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر عند الشراء')

    class Meta:
        verbose_name = 'عنصر الطلب'
        verbose_name_plural = 'عناصر الطلب'

    def total_price(self):
        return self.quantity * self.price
    #test