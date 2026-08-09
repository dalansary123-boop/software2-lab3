from django import template

register = template.Library()


@register.filter
def yemeni(text):
    """فلتر يحول الجملة الفصحى إلى لهجة يمنية"""
    if not isinstance(text, str):
        return text
    
    replacements = {
        'ماذا': 'ايش',
        'كيف': 'كيفش',
        'هل': 'هلّا',
        'اليوم': 'اليوم',
        'أنت': 'انت',
        'تفعل': 'تسوي',
        'حالك': 'حالك',
        'جيد': 'تمام',
        'نعم': 'اي',
        'لا': 'لا',
    }
    
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    return result


@register.filter
def perfume_status(stock):
    """فلتر يحدد حالة العطر بناءً على المخزون"""
    if stock == 0:
        return 'نفذت الكمية'
    elif stock <= 5:
        return 'كمية محدودة'
    elif stock <= 10:
        return 'متوسط'
    else:
        return 'متوفر بكثرة'


@register.filter
def currency(value):
    """فلتر يضيف رمز العملة"""
    try:
        return f"{float(value):.2f} ر.س"
    except (ValueError, TypeError):
        return value


@register.filter
def shorten_name(name, length=15):
    """فلتر يقصر الاسم"""
    if len(name) > length:
        return name[:length] + '...'
    return name