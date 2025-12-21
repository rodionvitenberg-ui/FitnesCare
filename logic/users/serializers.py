# logic/users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Получаем стандартные токены (access, refresh)
        data = super().validate(attrs)

        # Добавляем наши данные в JSON-ответ
        data['username'] = self.user.username
        data['is_coach'] = self.user.is_coach  # Берем реальное значение из БД
        
        # Можно добавить имя студии, если нужно сразу
        data['studio_name'] = self.user.studio_name 

        return data