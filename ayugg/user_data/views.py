from django.shortcuts import render

# Create your views here.

from .models import userModel

userModel = userModel.objects.get(pk=1)
for match in userModel.matchList:
    print(match.raw_data)