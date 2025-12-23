from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Client, Category, Tag, Attribute, ClientAttribute, 
    WorkSession, SessionComment
)

User = get_user_model()

# === Справочники ===

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name', 'description', 'icon']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['slug', 'name', 'color', 'icon']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['slug', 'name', 'attr_type', 'icon']

# === Атрибуты Клиента (EAV) ===

class ClientAttributeSerializer(serializers.ModelSerializer):
    attribute_slug = serializers.ReadOnlyField(source='attribute.slug')
    attribute_name = serializers.ReadOnlyField(source='attribute.name')
    attribute_type = serializers.ReadOnlyField(source='attribute.attr_type')

    class Meta:
        model = ClientAttribute
        fields = ['id', 'attribute', 'attribute_slug', 'attribute_name', 'attribute_type', 'value']
        extra_kwargs = {'attribute': {'write_only': True}}

# === Чат и Сессии ===

class SessionCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = SessionComment
        fields = ['id', 'session', 'author', 'author_name', 'text', 'attachment', 'created_at', 'is_read', 'is_me']
        read_only_fields = ['author', 'created_at', 'is_read']

    def get_is_me(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.author == request.user
        return False

class WorkSessionSerializer(serializers.ModelSerializer):
    comments = SessionCommentSerializer(many=True, read_only=True)
    client_name = serializers.ReadOnlyField(source='client.name')

    class Meta:
        model = WorkSession
        fields = [
            'id', 'client', 'client_name', 'title', 'description', 
            'client_feedback', 'attachment', 'date', 'status', 
            'created_at', 'updated_at', 'comments'
        ]
        read_only_fields = ['created_at', 'updated_at']

# === Клиенты ===

class ClientSerializer(serializers.ModelSerializer):
    """
    Полный профиль клиента.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    attributes = ClientAttributeSerializer(many=True, read_only=True)
    
    categories_details = CategorySerializer(source='categories', many=True, read_only=True)
    tags_details = TagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'coach', 'name', 'photo', 'email', 
            'gender', 'birth_date',  # <--- Добавлено
            'categories', 'categories_details',
            'tags', 'tags_details',
            'attributes',
            'is_active', 'created_at'
        ]
        read_only_fields = ['coach', 'created_at']

class ClientCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания: Email -> User + Client + Password Email.
    """
    email = serializers.EmailField(write_only=True)
    generated_password = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'photo', 'categories', 'tags', 
            'gender', 'birth_date', # <--- Добавлено, теперь их можно слать при создании
            'email', 'generated_password'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует."})

        password = User.objects.make_random_password(length=10)

        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            
            client = Client.objects.create(
                user=user,
                coach=self.context['request'].user, 
                **validated_data
            )
            
            client.categories.set(categories)
            client.tags.set(tags)

            try:
                send_mail(
                    subject='Доступ к платформе FitCare',
                    message=f'Ваш тренер создал для вас аккаунт.\nЛогин: {email}\nПароль: {password}',
                    from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@fitcare.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Ошибка отправки письма: {e}")

            client.generated_password = password
            return client