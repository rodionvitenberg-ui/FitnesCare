from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import (
    Client, Category, Tag, Attribute, ClientAttribute, 
    WorkSession, SessionComment
)
from .serializers import (
    ClientSerializer, ClientCreateSerializer, 
    CategorySerializer, TagSerializer, AttributeSerializer,
    ClientAttributeSerializer, WorkSessionSerializer, SessionCommentSerializer
)

class IsCoachOrClientOwner(permissions.BasePermission):
    """
    Разграничение прав:
    - Коуч имеет полный доступ к своим клиентам.
    - Клиент имеет доступ только к своему профилю и своим данным (Read/Update).
    """
    def has_object_permission(self, request, view, obj):
        # Если это объект Client
        if isinstance(obj, Client):
            return obj.coach == request.user or obj.user == request.user
        
        # Если это WorkSession
        if isinstance(obj, WorkSession):
            return obj.client.coach == request.user or obj.client.user == request.user

        return False

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'user__email', 'tags__name']
    filterset_fields = ['categories', 'tags']

    def get_queryset(self):
        user = self.request.user
        # Если юзер - коуч (у него есть поле is_coach или мы определяем это по связям)
        # В нашей модели: Коуч видит клиентов, где он coach. Клиент видит себя.
        
        # 1. Записи, где я тренер
        as_coach = Client.objects.filter(coach=user)
        # 2. Запись, где я клиент (мой профиль)
        as_client = Client.objects.filter(user=user)
        
        return (as_coach | as_client).distinct().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        # Принудительно ставим текущего юзера как тренера
        serializer.save(coach=self.request.user)


class WorkSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['status', 'client', 'date']

    def get_queryset(self):
        user = self.request.user
        # Коуч видит сессии своих клиентов. Клиент видит свои сессии.
        return WorkSession.objects.filter(
            Q(client__coach=user) | Q(client__user=user)
        ).distinct().order_by('-date')

    def perform_create(self, serializer):
        # Если клиент передается в теле запроса - ок, проверяем права.
        # Если создает коуч, он должен указать client_id.
        serializer.save() 


class SessionCommentViewSet(viewsets.ModelViewSet):
    """
    Отдельный вьюсет для комментариев, чтобы можно было удобно
    создавать их POST-запросом.
    """
    serializer_class = SessionCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session']

    def get_queryset(self):
        user = self.request.user
        return SessionComment.objects.filter(
            Q(session__client__coach=user) | Q(session__client__user=user)
        ).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# === Справочники (ReadOnly или AdminOnly, но пока делаем ModelViewSet для удобства) ===

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] # Или IsAuthenticated

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [permissions.AllowAny]

class ClientAttributeViewSet(viewsets.ModelViewSet):
    """
    Управление значениями атрибутов (CRUD).
    """
    serializer_class = ClientAttributeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ClientAttribute.objects.filter(
            Q(client__coach=user) | Q(client__user=user)
        )