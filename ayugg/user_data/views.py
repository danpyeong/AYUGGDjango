from rest_framework import viewsets, generics
from .models import userModel
from .serializers import ItemSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = userModel.objects.all()
    serializer_class = ItemSerializer

class UserDetailView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        gameName = self.kwargs['gameName']
        tagLine = self.kwargs['tagLine']
        return userModel.objects.filter(gameName=gameName, tagLine=tagLine)