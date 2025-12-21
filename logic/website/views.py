from rest_framework import generics, permissions
from .models import CarouselSlide
from .serializers import CarouselSlideSerializer

class CarouselListView(generics.ListCreateAPIView):
    """
    Отдает список всех 5 слотов.
    Если слотов нет в БД, создает их автоматически (Seed Data).
    """
    serializer_class = CarouselSlideSerializer
    permission_classes = [permissions.AllowAny] # Публично (для сайта)

    def get_queryset(self):
        # Если слотов нет, создаем 5 штук
        if CarouselSlide.objects.count() < 5:
            for i in range(1, 6):
                CarouselSlide.objects.get_or_create(slot_id=i)
        return CarouselSlide.objects.all().order_by('slot_id')

class CarouselUpdateView(generics.RetrieveUpdateAPIView):
    """
    [DevMode] Обновление конкретного слота по ID.
    Требует авторизации (только для Владельца).
    """
    queryset = CarouselSlide.objects.all()
    serializer_class = CarouselSlideSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slot_id' # Будем искать по номеру слота (1-5), а не по id базы