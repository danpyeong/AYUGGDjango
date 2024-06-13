from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RankView, SoloRankViewSet, FlexRankViewSet


router = DefaultRouter()
router.register(r'SoloRankModel', SoloRankViewSet)
router.register(r'FlexRankModel', FlexRankViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ranking/', RankView.as_view()),
    path('ranking/<str:type>', RankView.as_view()),
]

