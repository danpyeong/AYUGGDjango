from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from main.calc_game_data import statics_data
from .models import MatchInfoData, Version, Champion, MatchData, StaticsChampionMiddleData
from django.db.models import Q
import json
from django.core.serializers import serialize

# get 요청 시
def version(request):
    if request.method == 'GET':
        version = Version.objects.values_list('version', flat=True).first()
        return JsonResponse(version, safe=False)

def champion_list(request):
    if request.method == 'GET':
        champions = Champion.objects.all().order_by('champion_name')
        data = list(champions.values('champion_key', 'champion_name', 'champion_img', 'champion_version', 'champion_id'))
        return JsonResponse(data, safe=False)

@csrf_exempt   
def champion_statics(request):
    if request.method == 'GET':
        get_data = StaticsChampionMiddleData.objects.all()
        serialized_data = serialize('json', get_data)
        return JsonResponse(serialized_data, safe=False)
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # data[버전][티어][라인]
        tier = body_data['info']['tier']
        line = body_data['info']['line']
        ver = body_data['info']['ver']
        
        conditions = Q(champ_middle_data_version=str(ver))
        conditions.add(Q(champ_middle_data_tier = tier), Q.AND)
        conditions.add(Q(champ_middle_data_line = line), Q.AND)
        
        filter_data = StaticsChampionMiddleData.objects.filter(conditions)
        serialized_data = serialize('json', filter_data)
        
        print(f'Tier: {tier}, Line: {line}, Ver: {ver}')
        
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)