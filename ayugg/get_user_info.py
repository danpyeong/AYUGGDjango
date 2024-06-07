from user_data.models import userModel
import requests

# cd AYUGGDjango/ayugg
# python manage.py shell
# exec(open("get_user_info.py", encoding="utf-8").read())

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}
# api수정
# api_key = "api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

api_key = 'api_key=RGAPI-8a273e3c-4974-4b30-9e39-11b6aa832270'

# hide on bush/KR1 league data(id값입력) [] 반환됨
# riot_id_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/hide on bush/KR1"
riot_id_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/NekoL/0214"
# riot_id_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/의심하지말고해/KR1"
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


class search_data():
    
    def get():
        result_data = {}

        riot_id_data = get_data(riot_id_url + "?" + api_key)
        result_data['puuid'] = riot_id_data['puuid']
        result_data['gameName'] = riot_id_data['gameName']
        result_data['tagLine'] = riot_id_data['tagLine']

        puuid_data = get_data(encrypted_puuid_url + result_data['puuid'] + "?" + api_key)
        result_data['profileIconId'] = puuid_data['profileIconId']
        result_data['id'] = puuid_data['id']
        result_data['summonerLevel'] = puuid_data['summonerLevel']

        # 예외처리 []로 할경우
        id_data = get_data(id_url + result_data['id'] + "?" + api_key)
        if len(id_data) != 0:
            if 'rank' in id_data[0]:            
                result_data['rank'] = id_data[0]['rank']
            else:
                result_data['rank'] = 'UNLANK'
            if 'tier' in id_data[0]:            
                result_data['tier'] = id_data[0]['tier']
            else:
                result_data['tier'] = ''
            if 'leaguePoints' in id_data[0]:            
                result_data['leaguePoints'] = id_data[0]['leaguePoints']
            else:
                result_data['leaguePoints'] = 0
            if 'wins' in id_data[0]:            
                result_data['wins'] = id_data[0]['wins']
            else:
                result_data['wins'] = 0
            if 'losses' in id_data[0]:            
                result_data['losses'] = id_data[0]['losses']
            else:
                result_data['losses'] = 0
        else:
            result_data['rank'] = 'UNLANK'
            result_data['tier'] = ''
            result_data['leaguePoints'] = 0
            result_data['wins'] = 0
            result_data['losses'] = 0

        
        match_id_data = get_data(matches_url + result_data['puuid'] + "/ids?count=20&" + api_key)
        result_data['matchList'] = match_id_data
        
        match_num = 10
        result_data['matches'] = []
        result_data['matchNum'] = []
        for m in range(match_num):
            match_data = get_data(matchDataUrl + result_data['matchList'][m] + "?" + api_key)
            tier_list = []

            for j in range(10):                 
                tier_data = get_data(id_url + match_data['info']['participants'][j]['summonerId'] + "?" + api_key)
                if len(tier_data) != 0:
                    if 'tier' in tier_data[0]:
                        tier_list.append(tier_data[0]['tier'] +" "+ tier_data[0]['rank'])
                    else:
                        tier_list.append('UNRANK')                        
                else:
                    tier_list.append('UNRANK')
            
            match_data['tierList'] = tier_list
            result_data['matches'].append(match_data)
            
            
            for i in range(10):
                if result_data['id'] == result_data['matches'][m]['info']['participants'][i]['summonerId']:
                    result_data['matchNum'].append(i)
                    

        # print(riot_id_url + "?" + api_key)
        # print(puuid_data)
        # print(result_data['matches'][0]['info']['queueId'])
        return(result_data)

    def save_user_data(result_data):
        user = userModel(
            puuid=result_data['puuid'],
            gameName=result_data['gameName'],
            tagLine=result_data['tagLine'],
            profileIconId=result_data['profileIconId'],
            id=result_data['id'],
            summonerLevel=result_data['summonerLevel'],
            rank=result_data['rank'],
            tier=result_data['tier'],
            leaguePoints=result_data['leaguePoints'],
            wins=result_data['wins'],
            losses=result_data['losses'],
            matchList=result_data['matchList'],
            matches=result_data['matches'],
            matchNum=result_data['matchNum']
        )
        user.save()

    data = get()
    save_user_data(data)

    # # more 버튼 이후
    # def moreMatch(data):
    #     match_num = 2
    #     match_start = len(data['matches'])
    #     for m in range(match_num):
    #         # print(m+match_start)
    #         match_data = get_data(matchDataUrl + data['matchList'][m+match_start] + "?" + api_key)
    #         tier_list = []
            
    #         for j in range(10):                 
    #             tier_data = get_data(id_url + match_data['info']['participants'][j]['summonerId'] + "?" + api_key)
    #             if len(tier_data) != 0:
    #                 if 'tier' in tier_data[0]:
    #                     tier_list.append(tier_data[0]['tier'] +" "+ tier_data[0]['rank'])
    #                 else:
    #                     tier_list.append('UNRANK')                        
    #             else:
    #                 tier_list.append('UNRANK')
            
    #         match_data['tierList'] = tier_list
    #         data['matches'].append(match_data)

    #         for i in range(10):
    #             if data['id'] == data['matches'][0]['info']['participants'][i]['summonerId']:
    #                 data['matchNum'].append(i)
    #                 # print(data['matchNum'])
        
    #     for i in range(10):
    #         if data['id'] == data['matches'][m]['info']['participants'][i]['summonerId']:
    #             data['matchNum'].append(i)

    #     return data
    
    # data = moreMatch(data)
    # # for i in range(len(data['matches'])):
    #     # print(data['matches'][i]['tierList'])
    # save_user_data(data)

     


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