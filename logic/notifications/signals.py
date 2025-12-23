from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from clients.models import WorkSession, SessionComment

@receiver(post_save, sender=WorkSession)
def notify_client_on_new_session(sender, instance, created, **kwargs):
    """
    Когда создается новая тренировка/сессия, уведомляем Клиента.
    """
    # created=True означает, что объект только что создан (а не отредактирован)
    if created and instance.client.user:
        Notification.objects.create(
            recipient=instance.client.user,
            category='workout',
            title=f"Новое событие: {instance.title}",
            message=f"Тренер добавил новую задачу на {instance.date.strftime('%d.%m %H:%M')}",
            content_object=instance
        )

@receiver(post_save, sender=SessionComment)
def notify_on_new_comment(sender, instance, created, **kwargs):
    """
    Уведомления о новых сообщениях в чате сессии.
    """
    if created:
        session = instance.session
        
        # Получаем участников
        client_user = session.client.user
        coach_user = session.client.coach  # Владелец карточки клиента - это тренер
        
        # Кто написал комментарий?
        author = instance.author
        
        # 1. Если написал Тренер -> шлем Клиенту
        if author == coach_user and client_user:
            Notification.objects.create(
                recipient=client_user,
                category='message',
                title="Сообщение от тренера",
                message=f"К тренировке '{session.title}': {instance.text[:50]}...",
                content_object=session  # Ссылка ведет на саму сессию
            )
            
        # 2. Если написал Клиент -> шлем Тренеру
        elif author == client_user and coach_user:
            Notification.objects.create(
                recipient=coach_user,
                category='message',
                title=f"Сообщение от {session.client.name}",
                message=f"К тренировке '{session.title}': {instance.text[:50]}...",
                content_object=session
            )