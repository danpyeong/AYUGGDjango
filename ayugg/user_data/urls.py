from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserDetailView


router = DefaultRouter()
router.register(r'userModel', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:gameName>/', UserDetailView.as_view()),
]
