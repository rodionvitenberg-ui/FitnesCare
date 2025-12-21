from django.urls import path
from .views import MyProfileView, WorkoutListView, WorkoutDetailView, MediaUploadView, CoachClientListView

urlpatterns = [
    # Профиль
    path('profile/', MyProfileView.as_view(), name='my-profile'),
    
    # Тренировки
    path('workouts/', WorkoutListView.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    
    # Загрузка (Мясо)
    path('media/upload/', MediaUploadView.as_view(), name='media-upload'),
    path('coach/clients/', CoachClientListView.as_view(), name='coach-client-list'),
]