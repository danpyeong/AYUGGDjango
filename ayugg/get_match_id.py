from main.models import MatchData, Version
import requests
import time
from django.db import transaction

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

api_key = "api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

common_url = "https://kr.api.riotgames.com/lol/"

# api 호출
def get_data(url):
    try:
        response = requests.get(url, headers= request_headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            if response.status_code == 429:
                for i in range(30):
                    time.sleep(1)
                    print(i)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# 특정 티어의 유저 id 추출하는 api
league_api_url = "league/v4/entries/RANKED_SOLO_5x5/"
user_tier = ["IRON/", "BRONZE/", "SILVER/", "GOLD/", "PLATINUM/", "EMERALD/", "DIAMOND/"]
tier_division = ["I?", "II?", "III?", "IV?"]

# - 다이아몬드까지 티어별 url
def get_league_url(user_tier, tier_division):
    url_list = []
    url = common_url + league_api_url

    tier_url = []
    for tier in user_tier:
        tier_url.append(url + tier)
        
    for t_url in tier_url:
        for division in tier_division:
            url_list.append(t_url + division)
    return url_list

url_list = get_league_url(user_tier, tier_division)

select_url_list = []
# 여기만 수정하면됨
# range를 수정함에 따라 티어가 달라짐
# 0~5 : iron / 5~10: bronze ... 
for i in range(10):
    # 각 티어당 4개의 division이 있음. 0~5 / 5~10 ...
    for index, url_ in enumerate(url_list):
        if index > 12:
            url = url_ + "page=" + str(i+20) + "&" + api_key
            select_url_list.append(url)

# https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/GOLD/II?page=1&api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94

for url in select_url_list:
    #  - 데이터 추출 완료
    data = get_data(url)
    
    # 티어
    tier = url.split("/")[8]
    
    #  - summonerId 모으기
    summoner_id_list = []
    for index, d in enumerate(data):
        if index <= 30:
            summoner_id_list.append(d['summonerId'])
        # puuid 모으기
    
    #  - summonerId 로 puuid 추출하기
    puuid_api_url = "summoner/v4/summoners/"

    puuid_list = []
    for summ_id in summoner_id_list:
        url = common_url + puuid_api_url + summ_id + "?" + api_key
        # https://kr.api.riotgames.com/lol/summoner/v4/summoners/raNafr_iALNJPZLMKqv4cpOSfbpVqRPVS5OlK2ok0QhOcAG4?api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94
        data = get_data(url)
        if data:
            puuid_list.append(data['puuid'])

    # puuid로 matchid 모으기
    start_match_api_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"

    match_id_list = []
    for p_id in puuid_list:
        match_id_url = start_match_api_url + p_id + "/ids?type=ranked&start=0&count=15&" + api_key
        data = get_data(match_id_url)
        
        if data:
            match_id_list += data
            
    version = Version.objects.values_list('version', flat=True).first()
    ver = Version.objects.get(version=version)
    for list in match_id_list:
        try:
            with transaction.atomic():
                # match_id가 이미 존재하는지 확인
                if not MatchData.objects.filter(match_id=list).exists():
                    # 존재하지 않으면 데이터 생성
                    MatchData.objects.create(match_version=ver, match_id=list, tier=tier)
                else:
                    print(f"MatchData with match_id={list} already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")
    print("push Data End : " + str(MatchData.objects.all().count()) + " / " + tier)
    
    
print("push Data End : " + str(MatchData.objects.all().count()))
