from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Program, 
    ClientStatus, 
    BodyMetric, 
    ClientProfile, 
    MetricLog, 
    WorkoutSession, 
    MediaReport
)

# --- INLINES (Вложенные элементы) ---

class MetricLogInline(admin.TabularInline):
    """
    Позволяет добавлять замеры (вес, талия) прямо внутри профиля клиента.
    """
    model = MetricLog
    extra = 1
    readonly_fields = ('date',)
    classes = ('collapse',) # Свернуто по умолчанию, чтобы не мешать

class MediaReportInline(admin.TabularInline):
    """
    Показывает загруженные фото/видео внутри тренировки.
    """
    model = MediaReport
    extra = 0
    readonly_fields = ('preview_media',) # См. метод ниже
    
    def preview_media(self, obj):
        if obj.file:
            # Если это картинка - покажем миниатюру
            if obj.media_type == 'image':
                return format_html('<img src="{}" style="height: 100px; border-radius: 5px;" />', obj.file.url)
            # Если видео - ссылку
            return format_html('<a href="{}" target="_blank">🎥 Смотреть видео</a>', obj.file.url)
        return "-"
    preview_media.short_description = "Превью"

# --- MAIN ADMIN CLASSES ---

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'coach_link', 'program', 'get_statuses', 'is_active', 'created_at')
    list_filter = ('program', 'statuses', 'is_active', 'coach')
    search_fields = ('full_name', 'user__email', 'user__username', 'coach__username')
    autocomplete_fields = ['user', 'coach'] # Удобный поиск, если юзеров тысячи
    inlines = [MetricLogInline]
    
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'coach', 'full_name', 'is_active')
        }),
        ('Анкета', {
            'fields': ('birth_date', 'gender', 'program')
        }),
        ('CRM и Статусы', {
            'fields': ('statuses', 'coach_notes')
        }),
    )

    def coach_link(self, obj):
        return obj.coach.username
    coach_link.short_description = "Тренер"

    def get_statuses(self, obj):
        # Рисуем цветные плашки для статусов (VIP, Должник)
        html = []
        for status in obj.statuses.all():
            color = status.color_code or '#ccc'
            html.append(
                f'<span style="background-color: {color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 4px;">{status.name}</span>'
            )
        return format_html("".join(html))
    get_statuses.short_description = "Статусы"


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(SimpleHistoryAdmin): # Используем историю изменений
    list_display = ('title', 'client', 'date_formatted', 'status_badge', 'event_type')
    list_filter = ('status', 'event_type', 'scheduled_at')
    search_fields = ('title', 'client__full_name', 'description')
    date_hierarchy = 'scheduled_at'
    inlines = [MediaReportInline]
    
    fieldsets = (
        ('Кто и Когда', {
            'fields': ('client', 'scheduled_at', 'status', 'event_type')
        }),
        ('Задание', {
            'fields': ('title', 'description')
        }),
        ('Результат', {
            'fields': ('completed_at', 'client_comment', 'coach_feedback')
        }),
    )

    def date_formatted(self, obj):
        return obj.scheduled_at.strftime("%d.%m %H:%M")
    date_formatted.short_description = "Время"

    def status_badge(self, obj):
        colors = {
            'planned': 'gray',
            'done': 'blue',
            'reviewed': 'green',
            'missed': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_badge.short_description = "Статус"


# --- CONFIGURATION ADMINS ---

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')
    prepopulated_fields = {'slug': ('name',)} # Авто-заполнение слага
    ordering = ('sort_order',)

@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview')
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color_code
        )
    color_preview.short_description = "Цвет"

@admin.register(BodyMetric)
class BodyMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'is_chartable', 'sort_order')
    list_editable = ('sort_order',)