from main.models import Champion, MatchInfoData, MatchData, Version
import requests
import time

# https://asia.api.riotgames.com/lol/match/v5/matches/KR_6876572610?api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

api_key = "?api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

common_url = "https://asia.api.riotgames.com/lol/match/v5/matches/"

# "KR_7054643931" << 문제 없음
# "KR_6876572610" << 문제 있음 아레나도 5:5 랭크게임으로 잡아서 문제가 있음
# 아레나는 라인도 invalid로 잡히고 룬도 없기 때문에 게임 데이터를 이용하여 통계를 낼 때는 라인이 invalid 인 것을 제외하면 될 듯함.

# 미리 뽑아 둔 matchid 수집
def get_match_id():
    ids = MatchData.objects.all()
    match_ids = []
    for id in ids:
        match_ids.append(id.match_id)
        
    return match_ids
    
ids = get_match_id()

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

# 필요한 데이터만 추출하는 함수
def data_extract(match_id, data, data_ban):
    # 불필요한 데이터 제외 후 필요한 데이터만 정리
    extract = []
    
    bans = []
    blue_ban = data_ban[0]['bans']
    red_ban = data_ban[1]['bans']
    
    for ban in blue_ban:
        ban_name = Champion.objects.filter(champion_key = ban['championId']).values_list('champion_name', flat=True).first()
        bans.append(ban_name)
    
    for ban in red_ban:
        ban_name = Champion.objects.filter(champion_key = ban['championId']).values_list('champion_name', flat=True).first()
        bans.append(ban_name)
    
    tier = MatchData.objects.filter(match_id = match_id).values_list('tier', flat=True).first()
    
    # versus를 구하기 위한 dict
    role_dict = {}
    for info in data:
        # 챔피언 key
        champ_key = info['championId']
        # 영문 이름 (id)
        champ_id = info['championName']
        # 한글 이름 (name)
        champ = Champion.objects.get(champion_key = champ_key)
        champ_name = champ.champion_name
        # 라인 TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
        role = info['individualPosition']
        
        if role not in role_dict:
            role_dict[role] = [{'key': champ_key, 'name': champ_name, 'id': champ_id}]
        else:
            role_dict[role] += [{'key': champ_key, 'name': champ_name, 'id': champ_id}]
        
        # 7개의 아이템을 담을 리스트
        item = []
        
        # 아이템 0~6, 값이 0인 경우는 하위템인 것으로 추측됨
        item.append(info['item0'])
        item.append(info['item1'])
        item.append(info['item2'])
        item.append(info['item3'])
        item.append(info['item4'])
        item.append(info['item5'])
        item.append(info['item6'])
        
        # 룬 특성
        perks = info['perks']
        
        # teamId 100:블루팀 / 200:레드팀
        tema_id = info['teamId']
        
        # 승리여부
        win = info['win']
        
        # 정보 종합
        extract.append({'key': champ_key, 'id': champ_id, 'name': champ_name, 'role': role,
                'item': item, 'team_id': tema_id, 'win': win, 'perks': perks, 'versus': [], 
                'bans': bans, 'tier': tier})
    
    
    for data in extract:
        # print(role_dict[data['role']])
        if role_dict[data['role']][0]['name'] == data['name']:
            data['versus'] = role_dict[data['role']][1]
        else:
            data['versus'] = role_dict[data['role']][0]
    
    return extract

# DB에 저장하는 함수
def push_data(match_id, game_data):
    version = Version.objects.values_list('version', flat=True).first()
    ver = Version.objects.get(version=version)
    for data in game_data:
        MatchInfoData.objects.get_or_create(
            match_data_version = ver,
            match_id = match_id, team_id = data['team_id'], champion_name = data['name'],
            champion_key = data['key'], champion_id = data['id'], versus_name = data['versus']['name'],
            versus_key = data['versus']['key'], versus_id = data['versus']['id'], win = data['win'],
            line = data['role'], perks = data['perks'], item = data['item'], bans = data['bans'], game_tier=data['tier'])
        
for index, id in enumerate(ids):
    if index > -1 :
        try:
            if index > -1:
                url = common_url + id + api_key

                response = requests.get(url, headers= request_headers)
                if response.status_code == 200:
            
                    rawdata = get_data(url)
                    
                    match_id = rawdata['metadata']['matchId']
                    data = rawdata['info']['participants']
                    
                    data_ban = rawdata['info']['teams']
                    
                    game_data = data_extract(match_id, data, data_ban)
                    
                    push_data(match_id, game_data)
                    print("Push Data End: " + str(id) + " / " + str(index))
                    if index == len(ids) - 1:
                        print(" - End - ")
                    
                else:
                    print("Error:", response.status_code)
                    if response.status_code == 429:
                        for i in range(80):
                            time.sleep(1)
                            if i%10 == 0:
                                print("sleep: ", i)
    
        except Exception as e:
            print("An error occurred:", e)
        
# 5040까지 했음
