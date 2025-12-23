from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.DateTimeField(source='created_at', format="%d.%m.%Y %H:%M", read_only=True)
    linked_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 
            'category', 
            'title', 
            'message', 
            'is_read', 
            'created_at', 
            'created_at_formatted',
            'linked_object'
        ]

    def get_linked_object(self, obj):
        """
        Помогает фронту понять, куда переходить при клике.
        Вернет: {'type': 'worksession', 'id': 5}
        """
        if obj.content_object:
            return {
                'type': obj.content_type.model, # 'worksession', 'sessioncomment'
                'id': obj.object_id
            }
        return None