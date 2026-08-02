from django import template

register = template.Library()
from django.shortcuts import render

def home(request):
    return render(request, 'students/home.html')

# 1. فلتر تحويل النص إلى حروف كبيرة (Upper)
@register.filter(name='upper_text')
def upper_text(value):
    """تحويل النص إلى حروف كبيرة"""
    if isinstance(value, str):
        return value.upper()
    return value

# 2. فلتر تحويل النص إلى حروف صغيرة (Lower)
@register.filter(name='lower_text')
def lower_text(value):
    """تحويل النص إلى حروف صغيرة"""
    if isinstance(value, str):
        return value.lower()
    return value

# 3. فلتر تكبير أول حرف من النص (Capitalize First)
@register.filter(name='cap_first')
def cap_first(value):
    """جعل الحرف الأول من الكلمة كبيراً"""
    if isinstance(value, str) and value:
        return value.capitalize()
    return value

# 4. فلتر قص النص عند عدد معين من الحروف (Truncate Characters)
@register.filter(name='truncate_chars')
def truncate_chars(value, arg):
    """اختصار النص إلى عدد محدد من الحروف مع إضافة نقاط"""
    try:
        length = int(arg)
        if isinstance(value, str) and len(value) > length:
            return value[:length] + '...'
    except ValueError:
        pass
    return value

# 5. فلتر تنسيق السعر وإضافة العملة (Format Currency)
@register.filter(name='currency')
def currency(value):
    """تنسيق المبلغ المالي وإضافة علامة الدولار"""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return value

# 6. فلتر تحويل الحالة إلى أيقونة أو نص منسق (Status Badge)
@register.filter(name='store_status')
def store_status(is_open):
    """إعادة نص حال المتجر مغلق أم مفتوح"""
    if is_open:
        return "✅ مفتوح ومستعد لاستقبال طلباتكم"
    return "❌ المتجر مغلق حالياً"

# 7. فلتر لحساب إجمالي السعر بعد الخصم (Apply Discount)
@register.filter(name='apply_discount')
def apply_discount(price, discount_percent):
    """حساب السعر النهائي بعد تطبيق نسبة خصم محددة"""
    try:
        price = float(price)
        discount = float(discount_percent)
        discounted_price = price - (price * (discount / 100))
        return f"${discounted_price:.2f}"
    except (ValueError, TypeError):
        return price