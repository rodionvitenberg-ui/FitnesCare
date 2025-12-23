from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Client

@receiver(post_delete, sender=Client)
def delete_related_user(sender, instance, **kwargs):
    """
    Уборка мусора: при удалении карточки Клиента удаляем и его аккаунт (User).
    Это нужно, чтобы освободить email и не хранить 'мертвые' аккаунты,
    в которые никто не может войти (так как удален профиль Client).
    """
    if instance.user:
        # Удаление User автоматически вызовет каскадное удаление всего, 
        # что привязано к User (например, токены авторизации)
        instance.user.delete()
        print(f"User {instance.user.email} was deleted via Client deletion.")