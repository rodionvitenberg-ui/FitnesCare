from rest_framework import generics, permissions, parsers
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import WorkoutSession, MediaReport, ClientProfile
from .serializers import WorkoutSessionSerializer, MediaReportSerializer, ClientProfileSerializer
from rest_framework import generics, permissions

class MyProfileView(generics.RetrieveAPIView):
    """
    Показывает клиенту его собственный профиль и программу.
    """
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ищем профиль, связанный с текущим залогиненным юзером
        try:
            return self.request.user.client_profile
        except ClientProfile.DoesNotExist:
            raise PermissionDenied("У этого пользователя нет профиля атлета.")

class WorkoutListView(generics.ListAPIView):
    """
    Список тренировок для календаря.
    Можно фильтровать по дате: /api/workouts/?date=2025-12-20
    """
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'scheduled_at': ['date', 'gte', 'lte'], 'status': ['exact']}

    def get_queryset(self):
        # Отдаем только тренировки текущего пользователя
        return WorkoutSession.objects.filter(
            client__user=self.request.user
        ).order_by('scheduled_at')

class WorkoutDetailView(generics.RetrieveUpdateAPIView):
    """
    Детальный просмотр одной тренировки + возможность оставить комментарий.
    """
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(client__user=self.request.user)

class MediaUploadView(generics.CreateAPIView):
    """
    Загрузка фото или видео отчета к тренировке.
    """
    serializer_class = MediaReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] # Чтобы принимать файлы

    def perform_create(self, serializer):
        workout_id = self.request.data.get('workout_id')
        
        # Проверяем, что тренировка принадлежит этому клиенту
        if not WorkoutSession.objects.filter(id=workout_id, client__user=self.request.user).exists():
            raise PermissionDenied("Вы не можете грузить отчеты к чужой тренировке.")
            
        workout = WorkoutSession.objects.get(id=workout_id)
        serializer.save(workout=workout)

class CoachClientListView(generics.ListCreateAPIView):
    """
    [ДЛЯ ТРЕНЕРА]
    GET: Получить список всех своих клиентов.
    POST: Создать нового клиента (Быстрый онбординг).
    """
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только тех, кого ведет этот тренер
        return ClientProfile.objects.filter(coach=self.request.user)

    def perform_create(self, serializer):
        # При создании клиента автоматически привязываем текущего тренера
        serializer.save(coach=self.request.user)