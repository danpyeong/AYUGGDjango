from main.models import MatchData
import requests

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
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# 특정 티어의 유저 id 추출하는 api
league_api_url = "league/v4/entries/RANKED_SOLO_5x5/"
user_tier = ["IRON/", "BRONZE/", "SILVER/", "GOLD/", "PLATINUM/", "EMERALD/", "DIAMOND/"]
tier_division = ["I?", "II?", "III?", "IV?"]

league_url = common_url + league_api_url + user_tier[0] + tier_division[0] + "page=1&" + api_key

# - 다이아몬드까지 티어별 url
def get_league_url(user_tier, tier_division):
    url_list = []
    url = common_url + league_api_url

    tier_url = []
    for t in user_tier:
        tier_url.append(url + t)
        
    for t_u in tier_url:
        for division in tier_division:
            url_list.append(t_u + division)
    return url_list

url_list = get_league_url(user_tier, tier_division)

#  - 데이터 추출 완료
data = get_data(league_url)

#  - summonerId 모으기
def get_match_id(data):
    id_list = []
    for index, d in enumerate(data):
        if index <= 10:
            id_list.append(d['summonerId'])
        
        # id_list.append(d['summonerId'])
    
    return id_list

id_list = get_match_id(data)

# puuid 모으기
puuid_api_url = "summoner/v4/summoners/"

puuid_url = common_url + puuid_api_url + "summonerId?" + api_key

#  - summonerId 로 puuid 추출하기
def get_puuid(id_list):
    pid_list = []
    for id in id_list:
        url = common_url + puuid_api_url + id + "?" + api_key
        data = get_data(url)
        if data:
            pid_list.append(data['puuid'])
    
    return pid_list
    
puuid_list = get_puuid(id_list)

# puuid로 matchid 모으기
start_match_api_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"

def get_match_id(puuid_list):
    p_list = []
    for index, p_id in enumerate(puuid_list):
        match_id_url = start_match_api_url + p_id + "/ids?type=ranked&start=0&count=10&" + api_key
        data = get_data(match_id_url)
        if data:
            p_list += data
            
    return p_list

match_id_list = get_match_id(puuid_list)

# print(match_id_list)

def push_data(match_id_list):
    for list in match_id_list:
        m = MatchData(match_id = list)
        m.save()

push_data(match_id_list)
# 문제시 삭제
# m = MatchData.objects.all().delete()
print("End")
# m = MatchData(match_id="123")
# m.save()