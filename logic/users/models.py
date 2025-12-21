from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Единая модель пользователя (Коуч или Клиент).
    """
    # Роли
    is_coach = models.BooleanField(
        default=False, 
        help_text="Отметьте, если это Тренер (Владелец кабинета)"
    )
    
    # Флаг для тех, кого создал тренер, но они еще не зашли
    is_onboarded = models.BooleanField(
        default=False,
        help_text="Клиент уже заходил в приложение?"
    )
    
    # Общие данные
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='users_avatars/', null=True, blank=True, verbose_name="Аватар")
    
    # Для Коуча
    studio_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Название студии / Бренда",
        help_text="Отображается в шапке у клиента (Nike Style)"
    )
    
    def __str__(self):
        role = "COACH" if self.is_coach else "ATHLETE"
        return f"{self.username} | {role}"