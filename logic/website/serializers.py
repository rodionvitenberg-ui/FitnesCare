from rest_framework import serializers
from .models import CarouselSlide

class CarouselSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselSlide
        fields = '__all__'