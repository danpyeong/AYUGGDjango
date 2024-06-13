from rest_framework import serializers
from .models import SoloRankModel, FlexRankModel

class SoloRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloRankModel
        fields = '__all__'

class FlexRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexRankModel
        fields = '__all__'
