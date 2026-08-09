from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Perfume, CartItem, Order, OrderItem
from .forms import  OrderForm


def home(request):
    """الصفحة الرئيسية - تعرض العطور المميزة والفئات"""
    # ===== متغيرات محلية (Local Variables) =====
    featured_perfumes = Perfume.objects.filter(is_featured=True, stock__gt=0)[:6]
    all_categories = Category.objects.all()
    new_arrivals = Perfume.objects.filter(stock__gt=0).order_by('-created_at')[:4]
    
    # حساب عدد العناصر في السلة للمستخدم
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    
    context = {
        'featured_perfumes': featured_perfumes,
        'categories': all_categories,
        'new_arrivals': new_arrivals,
        'cart_count': cart_count,
        'site_name': 'روائح الذهب',
        'welcome_message': 'اكتشف عالم العطور الفاخرة',
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """قائمة جميع العطور مع البحث والتصفية"""
    perfumes = Perfume.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    
    # ===== تعليمات الشرط (Conditional Statements) =====
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort', 'newest')
    
    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        perfumes = perfumes.filter(category_id=category_id)
    
    # ===== تعليمات الشرط المتعددة (if/elif/else) =====
    if sort_by == 'price_low':
        perfumes = perfumes.order_by('price')
    elif sort_by == 'price_high':
        perfumes = perfumes.order_by('-price')
    elif sort_by == 'name':
        perfumes = perfumes.order_by('name')
    else:  # newest
        perfumes = perfumes.order_by('-created_at')
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    
    context = {
        'perfumes': perfumes,
        'categories': categories,
        'query': query,
        'sort_by': sort_by,
        'cart_count': cart_count,
        'total_count': perfumes.count(),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """تفاصيل العطر الواحد"""
    perfume = get_object_or_404(Perfume, pk=pk)
    
    # عطور ذات صلة (نفس الفئة)
    related_perfumes = Perfume.objects.filter(
        category=perfume.category
    ).exclude(pk=pk)[:4]
    
    # ===== تعليمات الشرط =====
    in_stock = perfume.stock > 0
    has_discount = perfume.old_price is not None and perfume.old_price > perfume.price
    
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    
    context = {
        'perfume': perfume,
        'related_perfumes': related_perfumes,
        'in_stock': in_stock,
        'has_discount': has_discount,
        'cart_count': cart_count,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_to_cart(request, pk):
    """إضافة عطر إلى السلة"""
    perfume = get_object_or_404(Perfume, pk=pk)
   
    if perfume.stock <= 0:
        messages.error(request, 'عذراً، هذا العطر غير متوفر حالياً!')
        return redirect('shop:product_detail', pk=pk)
   
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        perfume=perfume
    )
   
    if not created:
        if cart_item.quantity < perfume.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'تمت زيادة الكمية: {perfume.name}')
        else:
            messages.warning(request, 'لا يمكن إضافة المزيد، الكمية محدودة!')
    else:
        messages.success(request, f'تم إضافة {perfume.name} إلى السلة!')
   
    return redirect('shop:cart')

@login_required
def cart(request):
    """عرض سلة التسوق"""
    cart_items = CartItem.objects.filter(user=request.user)
    
    # ===== الحلقة (Loop) لحساب الإجمالي =====
    total = 0
    item_count = 0
    for item in cart_items:
        total += item.total_price()
        item_count += item.quantity
    
    # ===== تعليمات الشرط =====
    if item_count == 0:
        messages.info(request, 'سلة التسوق فارغة! تصفح منتجاتنا.')
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
    }
    return render(request, 'shop/cart.html', context)


@login_required
def remove_from_cart(request, pk):
    """حذف من السلة"""
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    perfume_name = cart_item.perfume.name
    cart_item.delete()
    messages.success(request, f'تم إزالة {perfume_name} من السلة')
    return redirect('cart')


@login_required
def update_cart(request, pk):
    """تحديث كمية العطر في السلة"""
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    # ===== تعليمات الشرط =====
    if quantity > 0 and quantity <= cart_item.perfume.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'تم تحديث الكمية')
    elif quantity > cart_item.perfume.stock:
        messages.error(request, 'الكمية المطلوبة غير متوفرة!')
    else:
        cart_item.delete()
        messages.info(request, 'تم إزالة العنصر من السلة')
    
    return redirect('cart')


# @login_required
# def checkout(request):
#     """إتمام الطلب"""
#     cart_items = CartItem.objects.filter(user=request.user)
    
#     # ===== تعليمات الشرط =====
#     if not cart_items:
#         messages.warning(request, 'سلة التسوق فارغة!')
#         return redirect('product_list')
    
#     # ===== الحلقة لحساب الإجمالي =====
#     total = 0
#     for item in cart_items:
#         total += item.total_price()
    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.total_amount = total
#             order.save()
            
#             # نقل العناصر من السلة إلى الطلب
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     perfume=item.perfume,
#                     quantity=item.quantity,
#                     price=item.perfume.price
#                 )
#                 # تقليل المخزون
#                 item.perfume.stock -= item.quantity
#                 item.perfume.save()
            
#             # تفريغ السلة
#             cart_items.delete()
#             messages.success(request, f'تم إتمام طلبك بنجاح! رقم الطلب: #{order.id}')
#             return redirect('home')
#     else:
#         form = OrderForm()
    
#     context = {
#         'form': form,
#         'cart_items': cart_items,
#         'total': total,
#     }
#     return render(request, 'shop/checkout.html', context)
@login_required
def checkout(request):
    """إتمام الطلب"""
    cart_items = CartItem.objects.filter(user=request.user)
   
    if not cart_items:
        messages.warning(request, 'سلة التسوق فارغة!')
        return redirect('shop:product_list')
   
    total = 0
    for item in cart_items:
        total += item.total_price()
   
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()
           
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    perfume=item.perfume,
                    quantity=item.quantity,
                    price=item.perfume.price
                )
                item.perfume.stock -= item.quantity
                item.perfume.save()
           
            cart_items.delete()
            messages.success(request, f'تم إتمام طلبك بنجاح! رقم الطلب: #{order.id}')
            return redirect('shop:home')
    else:
        form = OrderForm()
   
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def my_orders(request):
    """طلباتي"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})


def perfume_search(request):
    """صفحة بحث باستخدام الفلتر المخصص"""
    result = None
    query = request.GET.get('q', '')
   
    if query:
        try:
            # البحث عن العطر
            result = Perfume.objects.filter(
                Q(name__icontains=query) | Q(brand__icontains=query)
            ).first()
        except:
            result = None
   
    context = {
        'query': query,
        'result': result,
        'site_name': 'روائح الذهب',
    }
    return render(request, 'shop/perfume_search.html', context)