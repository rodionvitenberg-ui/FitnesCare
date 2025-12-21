from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
import uuid

# --- СПРАВОЧНИКИ (Настройки Коуча) ---

class Program(models.Model):
    """
    Бывшая Category. Программа тренировок / Цель.
    Пример: "Сушка (Fat Loss)", "Набор массы", "Реабилитация".
    """
    name = models.CharField(max_length=200, verbose_name="Название программы")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Описание стратегии")
    
    # Nike Style: Красивая обложка программы
    cover_image = models.ImageField(
        upload_to='programs/', 
        null=True, 
        blank=True, 
        verbose_name="Обложка программы (Dark Theme)"
    )
    
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Программа / Цель"
        verbose_name_plural = "Программы"
        ordering = ['sort_order']

    def __str__(self):
        return self.name

class ClientStatus(models.Model):
    """
    Бывший Tag. CRM-статусы для управления бизнесом.
    Пример: "VIP", "Должник", "Травма колена".
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")
    slug = models.SlugField(max_length=100, unique=True)
    
    # Цвет плашки для UI (Nike style: Red for overdue, Green for paid)
    color_code = models.CharField(max_length=7, default="#FFFFFF", verbose_name="HEX цвет")
    
    icon = models.FileField(upload_to='status_icons/', blank=True, null=True)

    class Meta:
        verbose_name = "CRM-Статус"
        verbose_name_plural = "CRM-Статусы"

    def __str__(self):
        return self.name

class BodyMetric(models.Model):
    """
    Бывший Attribute. Метрики тела.
    Пример: "Вес (кг)", "Талия (см)", "Жим лежа (кг)".
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Метрика")
    unit = models.CharField(max_length=20, verbose_name="Ед. изм.", help_text="кг, см, %")
    is_chartable = models.BooleanField(default=True, verbose_name="Строить график?")
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Метрика тела"
        verbose_name_plural = "Метрики тела"
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.name} ({self.unit})"

# --- ОСНОВНЫЕ СУЩНОСТИ ---

class ClientProfile(models.Model):
    """
    Бывший Pet. Профиль атлета.
    Связывает Login (User) и Coach (Admin).
    """
    # Связь с аккаунтом для входа (создается автоматически)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        verbose_name="Аккаунт входа"
    )
    
    # Кто ведет этого клиента (Коуч)
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='clients',
        verbose_name="Тренер"
    )

    # Анкета
    full_name = models.CharField(max_length=255, verbose_name="ФИО Атлета")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    GENDER_CHOICES = [('M', 'Мужской'), ('F', 'Женский')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    
    # Настройки тренировок
    program = models.ForeignKey(
        Program, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='athletes', 
        verbose_name="Текущая программа"
    )
    statuses = models.ManyToManyField(ClientStatus, blank=True, verbose_name="CRM Теги")
    
    # Заметки тренера (скрытые от клиента)
    coach_notes = models.TextField(blank=True, verbose_name="Приватные заметки тренера")

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Клиент активен")

    class Meta:
        verbose_name = "Профиль Клиента"
        verbose_name_plural = "База Клиентов"

    def __str__(self):
        return self.full_name

class MetricLog(models.Model):
    """
    Бывший PetAttribute, но теперь с историей (Лог замеров).
    Хранит прогресс: 01.01 - 80кг, 01.02 - 78кг.
    """
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='metrics_log')
    metric = models.ForeignKey(BodyMetric, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Значение")
    date = models.DateField(auto_now_add=True, verbose_name="Дата замера")

    class Meta:
        verbose_name = "Замер"
        verbose_name_plural = "Журнал прогресса"
        ordering = ['-date']

class WorkoutSession(models.Model):
    """
    Бывший HealthEvent. Единица смысла - Тренировка или Событие.
    """
    client = models.ForeignKey(
        ClientProfile, 
        on_delete=models.CASCADE, 
        related_name='workouts', 
        verbose_name="Атлет"
    )
    
    EVENT_TYPES = [
        ('workout', '🏋️ Тренировка'),
        ('cardio', '🏃 Кардио'),
        ('meal', '🥦 Питание / БЖУ'),
        ('checkin', '📸 Чекин формы'),
        ('payment', '💰 Оплата'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='workout')
    
    STATUS_CHOICES = [
        ('planned', 'План 📅'),
        ('done', 'Сделано ✅'),
        ('reviewed', 'Проверено Коучем 🔥'), # Финальный статус
        ('missed', 'Пропущено ❌'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')

    title = models.CharField(max_length=255, verbose_name="Тема (День ног)")
    description = models.TextField(verbose_name="План тренировки (Задание)", help_text="Упражнения, подходы, веса")
    
    # Важные даты
    scheduled_at = models.DateTimeField(verbose_name="Дата и время тренировки")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Когда выполнил")
    
    # Коммуникация (Контекстный чат)
    client_comment = models.TextField(blank=True, verbose_name="Отчет клиента (Ощущения)")
    coach_feedback = models.TextField(blank=True, verbose_name="Ответ тренера")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Тренировка / Событие"
        verbose_name_plural = "Календарь событий"
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.title} ({self.client.full_name})"

class MediaReport(models.Model):
    """
    Бывший HealthEventAttachment.
    Фото/Видео отчеты. Загружаются в S3/Cloudflare.
    """
    workout = models.ForeignKey(
        WorkoutSession, 
        on_delete=models.CASCADE, 
        related_name='media',
        verbose_name="Тренировка"
    )
    file = models.FileField(
        upload_to='workouts/%Y/%m/%d/',
        verbose_name="Видео/Фото файл"
    )
    media_type = models.CharField(
        max_length=10, 
        choices=[('video', 'Видео'), ('image', 'Фото')],
        default='image'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Медиа-отчет"
        verbose_name_plural = "Медиа-отчеты"