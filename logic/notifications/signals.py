from django.db.models.signals import post_save
from django.dispatch import receiver
# Используем apps.get_model, чтобы избежать Circular Import (так как models.py может ссылаться друг на друга)
from django.apps import apps
from .models import Notification

@receiver(post_save, sender='clients.WorkSession')
def notify_client_on_new_session(sender, instance, created, **kwargs):
    """
    Когда создается новая тренировка/сессия, уведомляем Клиента.
    """
    if created and instance.client.user:
        Notification.objects.create(
            recipient=instance.client.user,
            category='workout',
            title=f"Новое событие: {instance.title}",
            message=f"Тренер добавил новую задачу на {instance.date.strftime('%d.%m %H:%M')}",
            content_object=instance
        )

@receiver(post_save, sender='clients.SessionComment')
def notify_on_new_comment(sender, instance, created, **kwargs):
    """
    Уведомления о новых сообщениях в чате сессии.
    Определяем, кто написал, и шлем уведомление второй стороне.
    """
    if created:
        session = instance.session
        client_user = session.client.user
        coach_user = session.client.coach
        
        # Автор комментария
        author = instance.author
        
        # Если написал Тренер -> шлем Клиенту
        if author == coach_user and client_user:
            Notification.objects.create(
                recipient=client_user,
                category='message',
                title=f"Сообщение от тренера",
                message=f"К тренировке '{session.title}': {instance.text[:50]}...",
                content_object=session # Ссылка ведет на саму сессию
            )
            
        # Если написал Клиент -> шлем Тренеру
        elif author == client_user and coach_user:
            Notification.objects.create(
                recipient=coach_user,
                category='message',
                title=f"Сообщение от {session.client.name}",
                message=f"К тренировке '{session.title}': {instance.text[:50]}...",
                content_object=session
            )