from django.db import models
from django.conf import settings

class Category(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.FileField(upload_to='categories/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория / Программа"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название тега")
    color = models.CharField(max_length=7, default="#808080", verbose_name="Цвет (HEX)")
    icon = models.FileField(upload_to='tags/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Attribute(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название атрибута")
    
    TYPE_CHOICES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('date', 'Дата'),
        ('boolean', 'Да/Нет'),
    ]
    attr_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    icon = models.FileField(upload_to='attributes/icons/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник атрибутов"
        verbose_name_plural = "Справочник атрибутов"


class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской (Male)'),
        ('F', 'Женский (Female)'),
        ('O', 'Другой (Other)'),
    ]


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        null=True, blank=True,
        verbose_name="Аккаунт для входа"
    )

    # Кто ведет этого клиента
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name="Тренер"
    )

    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    photo = models.ImageField(upload_to='clients/avatars/', null=True, blank=True, verbose_name="Фото")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Пол")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    categories = models.ManyToManyField(Category, blank=True, related_name='clients', verbose_name="Программы")
    tags = models.ManyToManyField(Tag, blank=True, related_name='clients', verbose_name="Теги")

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-created_at']


class ClientAttribute(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name="Значение")

    class Meta:
        unique_together = ('client', 'attribute')
        verbose_name = "Параметр клиента"
        verbose_name_plural = "Параметры клиента"


class WorkSession(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('completed', 'Выполнено'),
        ('review', 'Проверено'),
        ('missed', 'Пропущено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sessions', verbose_name="Клиент")
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Задание / План")
    client_feedback = models.TextField(blank=True, verbose_name="Отчет клиента")
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