from django.db.models import Q
from .models import Perfume

def get_all_perfumes():
    return Perfume.objects.all()


def get_available_perfumes():
    return Perfume.objects.filter(stock__gt=0)


def search_perfumes(query):
    return Perfume.objects.filter(
        Q(name__icontains=query)
        | Q(brand__icontains=query)
        | Q(description__icontains=query)
    )


def get_featured_perfumes():
    return Perfume.objects.filter(
        is_featured=True,
        stock__gt=0
    )


def get_perfumes_without_stock():
    return Perfume.objects.filter(stock=0)


def get_perfumes_ordered_by_price():
    return Perfume.objects.order_by('price')


def get_perfumes_except(perfume_id):
    return Perfume.objects.exclude(pk=perfume_id)


def get_perfumes_count():
    return Perfume.objects.count()


def perfume_exists(perfume_name):
    return Perfume.objects.filter(name=perfume_name).exists()