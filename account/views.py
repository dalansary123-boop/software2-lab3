from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile


def register(request):
    """تسجيل مستخدم جديد"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # إنشاء ملف المستخدم الشخصي
            phone = form.cleaned_data.get('phone', '')
            city = form.cleaned_data.get('city', '')
            UserProfile.objects.create(user=user, phone=phone, city=city)
            
            login(request, user)
            messages.success(request, 'تم إنشاء حسابك بنجاح! مرحباً بك في روائح الذهب')
            return redirect('shop:home')
    else:
        form = RegisterForm()
    
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request):
    """صفحة الملف الشخصي"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('account:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'account/profile.html', {'form': form, 'profile': profile})