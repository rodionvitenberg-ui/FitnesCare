from django.db import models
from django.core.exceptions import ValidationError

class CarouselSlide(models.Model):
    """
    Слайд для Hero-карусели.
    Всего существует ровно 5 слотов (1-5). Удалять их нельзя, можно только выключать.
    """
    SLOT_CHOICES = [(i, f"Слот {i}") for i in range(1, 6)]
    
    slot_id = models.IntegerField(choices=SLOT_CHOICES, unique=True, verbose_name="Номер слота (1-5)")
    is_active = models.BooleanField(default=False, verbose_name="Включен в ротацию?")
    
    # Медиа
    media = models.FileField(upload_to='website/carousel/', blank=True, null=True, verbose_name="Медиа файл")
    
    MEDIA_TYPE_CHOICES = [('image', 'Картинка'), ('video', 'Видео')]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image', editable=False)
    
    # Тексты
    headline = models.CharField(max_length=100, blank=True, verbose_name="Заголовок (H1)")
    subheadline = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок")
    
    # Кнопки (Конструктор)
    BUTTON_COUNT_CHOICES = [(0, 'Без кнопок'), (1, 'Одна кнопка'), (2, 'Две кнопки')]
    button_count = models.IntegerField(default=1, choices=BUTTON_COUNT_CHOICES, verbose_name="Кол-во кнопок")
    
    # Настройки кнопки 1
    btn1_text = models.CharField(max_length=50, blank=True, verbose_name="Кнопка 1: Текст")
    btn1_link = models.CharField(max_length=200, blank=True, verbose_name="Кнопка 1: Ссылка")
    btn1_style = models.CharField(max_length=20, default='white', choices=[('white', 'Белая'), ('outline', 'Контур')], verbose_name="Кнопка 1: Стиль")

    # Настройки кнопки 2
    btn2_text = models.CharField(max_length=50, blank=True, verbose_name="Кнопка 2: Текст")
    btn2_link = models.CharField(max_length=200, blank=True, verbose_name="Кнопка 2: Ссылка")
    btn2_style = models.CharField(max_length=20, default='outline', choices=[('white', 'Белая'), ('outline', 'Контур')], verbose_name="Кнопка 2: Стиль")

    class Meta:
        verbose_name = "Слайд карусели"
        verbose_name_plural = "Настройки Карусели"
        ordering = ['slot_id']

    def __str__(self):
        status = "🟢" if self.is_active else "🔴"
        return f"{status} Слот {self.slot_id}: {self.headline or 'Без заголовка'}"

    def save(self, *args, **kwargs):
        # Магия: Сам определяю, видео это или фото
        if self.media:
            ext = self.media.name.lower().split('.')[-1]
            if ext in ['mp4', 'mov', 'webm', 'avi']:
                self.media_type = 'video'
            else:
                self.media_type = 'image'
        super().save(*args, **kwargs)