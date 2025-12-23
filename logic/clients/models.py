from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Категории клиентов или программ (например: 'Похудение', 'Набор массы', 'Реабилитация').
    """
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Иконка (поддержка SVG/PNG)
    icon = models.FileField(upload_to='categories/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория / Программа"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    """
    Теги для быстрой маркировки (например: 'VIP', 'Травма колена', 'Должник').
    """
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название тега")
    color = models.CharField(max_length=7, default="#808080", verbose_name="Цвет (HEX)") # Для UI
    
    # Вернули иконку
    icon = models.FileField(upload_to='tags/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Attribute(models.Model):
    """
    Справочник атрибутов (EAV).
    Например: 'Рост', 'Вес', 'Обхват груди', 'Целевой калораж'.
    """
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название атрибута")
    
    TYPE_CHOICES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('date', 'Дата'),
        ('boolean', 'Да/Нет'),
    ]
    attr_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    
    # Вернули иконку
    icon = models.FileField(upload_to='attributes/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник атрибутов"
        verbose_name_plural = "Справочник атрибутов"


class Client(models.Model):
    """
    Карточка Клиента.
    Связывает бизнес-логику (Коуч, Параметры) с аккаунтом входа (User).
    """
    # Связь с аккаунтом для входа (OneToOne)
    # null=True временно, чтобы создание через админку не ломалось до работы Сигналов
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        null=True, blank=True,
        verbose_name="Аккаунт для входа"
    )

    # Кто ведет этого клиента (Коуч/Владелец)
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name="Тренер"
    )

    name = models.CharField(max_length=100, verbose_name="Имя клиента (Display Name)")
    photo = models.ImageField(upload_to='clients/avatars/', null=True, blank=True, verbose_name="Фото")
    
    # Таксономия
    categories = models.ManyToManyField(Category, blank=True, related_name='clients', verbose_name="Программы")
    tags = models.ManyToManyField(Tag, blank=True, related_name='clients', verbose_name="Теги")

    # Технические поля
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-created_at']


class ClientAttribute(models.Model):
    """
    Значения атрибутов для конкретного клиента.
    Client: Иван -> Attribute: Вес -> Value: 85
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name="Значение")

    class Meta:
        unique_together = ('client', 'attribute')
        verbose_name = "Параметр клиента"
        verbose_name_plural = "Параметры клиента"


class WorkSession(models.Model):
    """
    Основная единица работы.
    """
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
        ('missed', 'Пропущено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sessions', verbose_name="Клиент")
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Задание / План")
    
    # Быстрый отчет (если не нужен чат)
    client_feedback = models.TextField(blank=True, verbose_name="Отчет клиента")
    
    # Вложение (файл к самой тренировке, например PDF программы)
    attachment = models.FileField(upload_to='sessions/attachments/', null=True, blank=True, verbose_name="Вложение")

    date = models.DateTimeField(verbose_name="Дата и время")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name="Статус")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.client.name})"

    class Meta:
        verbose_name = "Сессия / Тренировка"
        verbose_name_plural = "Сессии"
        ordering = ['-date']


class SessionComment(models.Model):
    """
    Чат внутри конкретной сессии.
    """
    session = models.ForeignKey(WorkSession, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    
    text = models.TextField(verbose_name="Сообщение")
    attachment = models.FileField(upload_to='comments/', null=True, blank=True, verbose_name="Файл")
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.session}"

    class Meta:
        ordering = ['created_at']
        verbose_name = "Комментарий к сессии"
        verbose_name_plural = "Комментарии к сессиям"