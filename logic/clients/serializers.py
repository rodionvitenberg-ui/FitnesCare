from rest_framework import serializers
from .models import ClientProfile, WorkoutSession, MediaReport, Program, BodyMetric

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'cover_image']

class MediaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaReport
        fields = ['id', 'file', 'media_type', 'created_at']

class WorkoutSessionSerializer(serializers.ModelSerializer):
    # Вкладываем отчеты внутрь тренировки, чтобы видеть их сразу
    media = MediaReportSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = [
            'id', 'title', 'description', 'status', 
            'scheduled_at', 'event_type', 
            'client_comment', 'coach_feedback', 
            'media'
        ]

class ClientProfileSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    
    class Meta:
        model = ClientProfile
        fields = ['id', 'full_name', 'program', 'coach_notes']