from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import (
    Category, Client, Attribute, ClientAttribute, 
    Tag, WorkSession, SessionComment
)

# === Справочники ===

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    search_fields = ('name',)
    # prepopulated_fields больше не нужен для slug, если мы не редактируем его вручную, 
    # но обычно удобно оставить:
    prepopulated_fields = {'slug': ('name',)}

    def icon_preview(self, obj):
        if obj.icon:
            # Проверка расширения, чтобы не ломать админку SVG
            return mark_safe(f'<img src="{obj.icon.url}" style="max-height: 30px; max-width: 30px;" />')
        return "-"
    icon_preview.short_description = "Иконка"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'icon_preview')
    search_fields = ('name', 'slug')
    list_editable = ('color',)
    prepopulated_fields = {'slug': ('name',)}

    def icon_preview(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" style="max-height: 30px; max-width: 30px;" />')
        return "-"
    icon_preview.short_description = "Иконка"


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'attr_type', 'slug', 'icon_preview')
    list_filter = ('attr_type',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def icon_preview(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" style="max-height: 30px; max-width: 30px;" />')
        return "-"
    icon_preview.short_description = "Иконка"


# === Вспомогательные инлайны ===

class ClientAttributeInline(admin.TabularInline):
    """Атрибуты клиента (Вес, Рост) прямо в карточке клиента"""
    model = ClientAttribute
    extra = 1
    autocomplete_fields = ['attribute']

class SessionCommentInline(admin.TabularInline):
    """Чат внутри сессии. Позволяет видеть переписку в админке."""
    model = SessionComment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'text', 'attachment', 'created_at')

class WorkSessionInline(admin.TabularInline):
    """Список последних тренировок в карточке клиента"""
    model = WorkSession
    extra = 0
    fields = ('title', 'date', 'status')
    show_change_link = True
    ordering = ('-date',)


# === Основные модели ===

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'avatar_preview', 'coach', 'user_email', 'is_active', 'created_at')
    list_filter = ('is_active', 'categories', 'tags', 'coach')
    search_fields = ('name', 'user__email', 'coach__username', 'coach__email')
    autocomplete_fields = ['categories', 'tags', 'coach', 'user']
    inlines = [ClientAttributeInline, WorkSessionInline]
    
    fieldsets = (
        ('Основное', {
            'fields': ('coach', 'user', 'name', 'photo', 'is_active')
        }),
        ('Классификация', {
            'fields': ('categories', 'tags'),
        }),
    )

    def avatar_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;" />')
        return "-"
    avatar_preview.short_description = "Фото"

    def user_email(self, obj):
        return obj.user.email if obj.user else "-"
    user_email.short_description = "Email (Login)"


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'date', 'status')
    list_filter = ('status', 'date', 'client__coach')
    search_fields = ('title', 'description', 'client__name', 'client__user__email')
    date_hierarchy = 'date'
    autocomplete_fields = ['client']
    inlines = [SessionCommentInline] # Чат прямо внутри тренировки!

    fieldsets = (
        ('Детали сессии', {
            'fields': ('client', 'title', 'date', 'status', 'attachment')
        }),
        ('Контент', {
            'fields': ('description', 'client_feedback')
        }),
    )
    
    # Регистрация модели комментариев отдельно, если нужно искать по всем сообщениям
@admin.register(SessionComment)
class SessionCommentAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'session', 'author', 'created_at')
    search_fields = ('text', 'author__username')
    list_filter = ('created_at',)
    
    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    short_text.short_description = "Текст"