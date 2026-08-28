from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Perfume, CartItem, Order, OrderItem, ScentNote

@admin.register(ScentNote)
class ScentNoteAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    
@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'old_price', 'stock', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'brand', 'is_featured']
    search_fields = ['name', 'brand']
    list_editable = ['price', 'stock', 'is_featured']
    filter_horizontal = ['scent_notes']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'perfume', 'quantity', 'added_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    list_editable = ['status']