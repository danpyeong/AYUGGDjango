from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Version, Champion, ChampionBasicInfo, StaticsChampionMiddleData, ChampionDetails, AllStaticsData
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
    
def champion_basic_info(request):
    if request.method == 'GET':
        champions = ChampionBasicInfo.objects.all()
        data = list(champions.values('champ_id', 'champ_name', 'champ_img', 'champ_version_id'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        id = body_data['info']['id']
        
        conditions = Q(champ_id=str(id))
        
        filter_data = ChampionBasicInfo.objects.filter(conditions)
        serialized_data = serialize('json', filter_data)
        
        print(f'BasicId: {id}')
        
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
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
    
@csrf_exempt   
def champion_all_statics(request):
    if request.method == 'GET':
        get_data = AllStaticsData.objects.all()
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
        
        conditions = Q(statics_tier=str(tier))
        conditions.add(Q(statics_position = line), Q.AND)
        
        filter_data = AllStaticsData.objects.filter(conditions)
        serialized_data = serialize('json', filter_data)
        
        print(f'Tier: {tier}, Line: {line}')
        
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
@csrf_exempt   
def champion_details(request):
    if request.method == 'GET':
        get_data = ChampionDetails.objects.all()
        serialized_data = serialize('json', get_data)
        return JsonResponse(serialized_data, safe=False)
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        id = body_data['info']['id']
        
        conditions = Q(detail_champ_id=str(id))
        
        filter_data = ChampionDetails.objects.filter(conditions)
        serialized_data = serialize('json', filter_data)
        
        print(f'id: {id}')
        
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)