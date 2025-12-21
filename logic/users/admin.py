from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Админка для пользователей.
    ОБЯЗАТЕЛЬНО: search_fields нужен для работы autocomplete_fields в других моделях.
    """
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    list_display = ('username', 'email', 'is_coach', 'studio_name', 'is_staff')
    list_filter = ('is_coach', 'is_staff', 'is_active')
    
    # Добавляем наши кастомные поля (is_coach, studio_name и т.д.) в форму
    fieldsets = UserAdmin.fieldsets + (
        ('Специализация (FitCare)', {
            'fields': ('is_coach', 'is_onboarded', 'studio_name', 'phone', 'avatar')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Специализация (FitCare)', {
            'fields': ('is_coach', 'studio_name', 'email')
        }),
    )