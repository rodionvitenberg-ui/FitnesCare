# clients/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, WorkSessionViewSet, SessionCommentViewSet,
    CategoryViewSet, TagViewSet, AttributeViewSet, ClientAttributeViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'sessions', WorkSessionViewSet, basename='sessions')
router.register(r'comments', SessionCommentViewSet, basename='comments')
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'client-attributes', ClientAttributeViewSet, basename='client-attributes')

urlpatterns = router.urls