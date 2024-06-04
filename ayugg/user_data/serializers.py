from rest_framework import serializers
from .models import userModel

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = '__all__'
