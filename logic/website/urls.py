from django.urls import path
from .views import CarouselListView, CarouselUpdateView

urlpatterns = [
    # Получить все слайды (GET)
    path('carousel/', CarouselListView.as_view(), name='carousel-list'),
    
    # Обновить слайд №1, 2... (PUT/PATCH)
    path('carousel/<int:slot_id>/', CarouselUpdateView.as_view(), name='carousel-update'),
]