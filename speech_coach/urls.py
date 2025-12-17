from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpeechAnalysisViewSet

router = DefaultRouter()
router.register(r'speech-analysis', SpeechAnalysisViewSet, basename='speech-analysis')

urlpatterns = [
    path('', include(router.urls)),
]
