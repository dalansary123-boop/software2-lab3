# from django.urls import path  # استيراد دالة path لتحديد مسارات الصفحات
# from . import views  # استيراد ملف العرض views

# app_name = 'students'  # تسجيل اسم التطبيق حل مشكلة الـ namespace

# urlpatterns = [  # قائمة تحتوي على مسارات الموقع
#     path('', views.home, name='home'),  # مسار الصفحة الرئيسية
#     path('about/', views.about, name='about'),  # مسار صفحة عن المتجر
# ]
from django.urls import path
from . import views

app_name = 'students' # منع تعارض الأسماء كما يظهر في الشريحة الأخيرة

urlpatterns = [
    path('', views.home, name='home'),
]