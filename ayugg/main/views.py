from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Version, Champion, ChampionBasicInfo, MatchData

# get 요청 시
def champion_list(request):
    if request.method == 'GET':
        champions = Champion.objects.all().order_by('champion_name')
        data = list(champions.values('champion_key', 'champion_name', 'champion_img', 'champion_version', 'champion_id'))
        return JsonResponse(data, safe=False)