from rest_framework import viewsets, generics
from .models import SoloRankModel, FlexRankModel
from .serializers import SoloRankSerializer, FlexRankSerializer

class SoloRankViewSet(viewsets.ModelViewSet):
    queryset = SoloRankModel.objects.all()
    serializer_class = SoloRankSerializer

class FlexRankViewSet(viewsets.ModelViewSet):
    queryset = FlexRankModel.objects.all()
    serializer_class = FlexRankSerializer


class RankView(generics.ListAPIView):
    def get_serializer_class(self):
        # 조건에 따라 시리얼라이저를 선택
        if self.request.query_params.get('type') == 'solo':
            return SoloRankSerializer
        return FlexRankSerializer

    def get_queryset(self):
        if self.request.query_params.get('type') == 'solo':
            return SoloRankModel.objects.all()
        return FlexRankModel.objects.all()