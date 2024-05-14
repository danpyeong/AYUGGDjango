from main.models import MatchData
import requests
import time

# python manage.py shell
# exec(open("get_user_info.py", encoding="utf-8").read())

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}
# api수정
api_key = "api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

# common_url = "https://kr.api.riotgames.com/lol/"
# 변수 수정해야됨
riot_id_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Hide%20on%20bush/KR1"
encrypted_puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
id_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
matches_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"
matchDataUrl = "https://asia.api.riotgames.com/lol/match/v5/matches/"

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



# print(get_data(encrypted_puuid_url + get_data(puuid_url)['puuid'] + api_key))

class search_data():
    
    result_data = {}

    result_data = get_data(riot_id_url + "?" + api_key)

    puuid_data = get_data(encrypted_puuid_url + result_data['puuid'] + "?" + api_key)
    result_data['profileIconId'] = puuid_data['profileIconId']
    result_data['summonerId'] = puuid_data['id']
    result_data['summonerLevel'] = puuid_data['summonerLevel']

    id_data = get_data(id_url + result_data['summonerId'] + "?" + api_key)
    result_data['rank'] = id_data[0]['rank']
    result_data['tier'] = id_data[0]['tier']
    result_data['leaguePoints'] = id_data[0]['rank']
    result_data['wins'] = id_data[0]['wins']
    result_data['losses'] = id_data[0]['losses']
    
    match_id_data = get_data(matches_url + result_data['puuid'] + "/ids?count=20&" + api_key)
    result_data['matchList'] = match_id_data
    
    match_num = 2
    result_data['matches'] = []
    for m in range(match_num):
        result_data['matches'].append(get_data(matchDataUrl + result_data['matchList'][m] + "?" + api_key))


    # print(match_id_data)
    print(result_data['matches'])

    # print(get_data((encrypted_puuid_url + result_data['puuid'] + api_key)))

# def get():
#     for i in range(10):
#         #  - 데이터 추출 완료
#         data = get_data(select_url_list[i])

#         #  - summonerId 모으기
#         def get_match_id(data):
#             id_list = []
#             for index, d in enumerate(data):
#                 if index <= 10:
#                     id_list.append(d['summonerId'])
                
#                 # id_list.append(d['summonerId'])
            
#             return id_list

#         id_list = get_match_id(data)

#         # puuid 모으기
#         puuid_api_url = "summoner/v4/summoners/"

#         puuid_url = common_url + puuid_api_url + "summonerId?" + api_key

#         #  - summonerId 로 puuid 추출하기
#         def get_puuid(id_list):
#             pid_list = []
#             for id in id_list:
#                 url = common_url + puuid_api_url + id + "?" + api_key
#                 data = get_data(url)
#                 if data:
#                     pid_list.append(data['puuid'])
            
#             return pid_list
            
#         puuid_list = get_puuid(id_list)

#         # puuid로 matchid 모으기
#         start_match_api_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"

#         def get_match_id(puuid_list):
#             p_list = []
#             for index, p_id in enumerate(puuid_list):
#                 match_id_url = start_match_api_url + p_id + "/ids?type=ranked&start=0&count=10&" + api_key
#                 data = get_data(match_id_url)
#                 if data:
#                     p_list += data
                    
#             return p_list

#         match_id_list = get_match_id(puuid_list)

#         # print(match_id_list)

#         def push_data(match_id_list):
#             for list in match_id_list:   
#                 MatchData.objects.get_or_create(match_id = list)

#         push_data(match_id_list)
#         # 문제시 삭제
#         # m = MatchData.objects.all().delete()

#         print("End : " + str(i))
#         if i != 9:
#             print(MatchData.objects.all().count())
#             time.sleep(10)
#             print("get Data start")

# get()
