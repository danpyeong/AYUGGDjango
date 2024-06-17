from rest_framework import viewsets, generics
from .models import SoloRankModel, FlexRankModel
from .serializers import SoloRankSerializer, FlexRankSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

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
    


request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

api_key = 'api_key=RGAPI-8a273e3c-4974-4b30-9e39-11b6aa832270'
solo_rank_url = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&"
flex_rank_url = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_FLEX_SR/CHALLENGER/I?page=1&"
id_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"
puuid_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/"

def get_data(url):
    try:
        response = requests.get(url, headers=request_headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

class RankingData:
    @staticmethod
    def fetch_rank_data(rank_url):
        result_data = []

        rank_data = get_data(rank_url + api_key)
        for i in range(20):
            person_data = {}
            person_data['place'] = i + 1
            person_data['tier'] = rank_data[i]['tier']
            person_data['rank'] = rank_data[i]['rank']
            person_data['id'] = rank_data[i]['summonerId']
            person_data['leaguePoints'] = rank_data[i]['leaguePoints']
            person_data['wins'] = rank_data[i]['wins']
            person_data['losses'] = rank_data[i]['losses']

            id_data = get_data(id_url + person_data['id'] + "?" + api_key)
            person_data['puuid'] = id_data['puuid']
            person_data['profileIconId'] = id_data['profileIconId']
            person_data['summonerLevel'] = id_data['summonerLevel']

            puuid_data = get_data(puuid_url + person_data['puuid'] + "?" + api_key)
            person_data['gameName'] = puuid_data['gameName']
            person_data['tagLine'] = puuid_data['tagLine']

            result_data.append(person_data)

        return result_data

    @staticmethod
    def save_rank_data(result_data, rank_model):
        for v in result_data:
            rank_model.objects.update_or_create(
                id=v['id'],
                defaults={
                    'place': v['place'],
                    'puuid': v['puuid'],
                    'gameName': v['gameName'],
                    'tagLine': v['tagLine'],
                    'profileIconId': v['profileIconId'],
                    'summonerLevel': v['summonerLevel'],
                    'rank': v['rank'],
                    'tier': v['tier'],
                    'leaguePoints': v['leaguePoints'],
                    'wins': v['wins'],
                    'losses': v['losses'],
                }
            )

    @staticmethod
    def fetch_and_save():
        solo_data = RankingData.fetch_rank_data(solo_rank_url)
        flex_data = RankingData.fetch_rank_data(flex_rank_url)
        
        RankingData.save_rank_data(solo_data, SoloRankModel)
        RankingData.save_rank_data(flex_data, FlexRankModel)

@api_view(['POST'])
def fetch_and_save_rank_data(request):
    if request.method == 'POST':
        try:
            # 기존 데이터 삭제
            SoloRankModel.objects.all().delete()
            FlexRankModel.objects.all().delete()

            # 새로운 데이터 가져오기 및 저장
            data = RankingData.fetch_and_save()
            
            return Response({'message': 'Data fetched and saved successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)