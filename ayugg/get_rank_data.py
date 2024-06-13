from rank_data.models import SoloRankModel, FlexRankModel
import requests

# cd AYUGGDjango/ayugg
# python manage.py shell
# exec(open("get_rank_data.py", encoding="utf-8").read())

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}
# api수정
# api_key = "api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

api_key = 'api_key=RGAPI-8a273e3c-4974-4b30-9e39-11b6aa832270'
# https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94
solo_rank_url = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&"
# https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_FLEX_SR/CHALLENGER/I?page=1&api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94
flex_rank_url = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_FLEX_SR/CHALLENGER/I?page=1&"


encrypted_puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
id_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"
puuid_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/"
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
    

class ranking_data():
    @staticmethod
    def solo_get():
        result_solo_data = []

        solo_rank_data = get_data(solo_rank_url + api_key)
        # print(solo_rank_data[0])
        for i in range(20):
            person_data = {}
            person_data['place'] = i+1
            person_data['tier'] = solo_rank_data[i]['tier']
            person_data['rank'] = solo_rank_data[i]['rank']
            person_data['id'] = solo_rank_data[i]['summonerId']
            person_data['leaguePoints'] = solo_rank_data[i]['leaguePoints']
            person_data['wins'] = solo_rank_data[i]['wins']
            person_data['losses'] = solo_rank_data[i]['losses']

            id_data = get_data(id_url + person_data['id'] + "?" + api_key)
            person_data['puuid'] = id_data['puuid']
            person_data['profileIconId'] = id_data['profileIconId']
            person_data['summonerLevel'] = id_data['summonerLevel']

            puuid_data = get_data(puuid_url + person_data['puuid'] + "?" + api_key)
            person_data['gameName'] = puuid_data['gameName']
            person_data['tagLine'] = puuid_data['tagLine']

            result_solo_data.append(person_data)
        return result_solo_data
    
    @staticmethod
    def flex_get():
        result_flex_data = []

        flex_rank_data = get_data(flex_rank_url + api_key)
        # print(solo_rank_data[0])
        for i in range(20):
            person_data = {}
            person_data['place'] = i+1
            person_data['tier'] = flex_rank_data[i]['tier']
            person_data['rank'] = flex_rank_data[i]['rank']
            person_data['id'] = flex_rank_data[i]['summonerId']
            person_data['leaguePoints'] = flex_rank_data[i]['leaguePoints']
            person_data['wins'] = flex_rank_data[i]['wins']
            person_data['losses'] = flex_rank_data[i]['losses']

            id_data = get_data(id_url + person_data['id'] + "?" + api_key)
            person_data['puuid'] = id_data['puuid']
            person_data['profileIconId'] = id_data['profileIconId']
            person_data['summonerLevel'] = id_data['summonerLevel']

            puuid_data = get_data(puuid_url + person_data['puuid'] + "?" + api_key)
            person_data['gameName'] = puuid_data['gameName']
            person_data['tagLine'] = puuid_data['tagLine']

            result_flex_data.append(person_data)
        # print(result_flex_data[0])
        return result_flex_data
    
    @staticmethod
    def save_rank_data(result_data):
        for v in result_data[0]:
            solo_data = SoloRankModel(
                place=v['place'],
                puuid=v['puuid'],
                gameName=v['gameName'],
                tagLine=v['tagLine'],
                profileIconId=v['profileIconId'],
                id=v['id'],
                summonerLevel=v['summonerLevel'],
                rank=v['rank'],
                tier=v['tier'],
                leaguePoints=v['leaguePoints'],
                wins=v['wins'],
                losses=v['losses'],
            )
            flex_data = FlexRankModel(
                place=v['place'],
                puuid=v['puuid'],
                gameName=v['gameName'],
                tagLine=v['tagLine'],
                profileIconId=v['profileIconId'],
                id=v['id'],
                summonerLevel=v['summonerLevel'],
                rank=v['rank'],
                tier=v['tier'],
                leaguePoints=v['leaguePoints'],
                wins=v['wins'],
                losses=v['losses'],
            )
            solo_data.save()
            flex_data.save()
    
    data = [solo_get(), flex_get()]
    save_rank_data(data)