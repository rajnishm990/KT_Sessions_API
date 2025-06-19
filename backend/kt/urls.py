from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'kt', views.KTSessionViewSet, basename='kt')

urlpatterns = [
    path('', include(router.urls)),
    path('sessions/shared/<uuid:share_token>/', views.shared_session_view, name='shared-session'),
    path('attachments/<uuid:attachment_id>/', views.attachment_detail, name='attachment-detail'),
]