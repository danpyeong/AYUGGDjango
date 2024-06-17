import copy
import json
from main.models import AllGameData, Version, Champion, ChampionDetails, AllStaticsData
import requests
import time
import sqlite3
import os

def post_data():
    # 데이터베이스 파일 경로 설정
    db_path = os.path.join('myfrontend', 'server', 'crawling', 'dbData', 'championsDetails.db')

    # 경로와 파일이 존재하는지 확인
    if not os.path.exists(db_path):
        print(f"Error: The database file at {db_path} does not exist.")
    else:
        # SQLite 데이터베이스 연결
        try:
            champ_data = Champion.objects.all().order_by("champion_name")
            
            for champ in champ_data:
                champ_id = champ.champion_id
                
                conn = sqlite3.connect(db_path)
                
                # 커서 생성
                cursor = conn.cursor()
                
                table_name = champ_id.lower()
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                rows = rows[0]
                # 데이터 출력
                print(f"Data from {table_name} table :")
                
                counter_data = json.loads(rows[5])                
                rune_data = json.loads(rows[6])
                
                ChampionDetails.objects.get_or_create(
                                detail_champ_id = champ_id,
                                detail_champ_name = champ.champion_name,
                                detail_win_counter_1 = {'name': counter_data['winCounter'][0]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['winCounter'][0]['winRate']},
                                detail_win_counter_2 = {'name': counter_data['winCounter'][1]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['winCounter'][1]['winRate']},
                                detail_win_counter_3 = {'name': counter_data['winCounter'][2]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['winCounter'][2]['winRate']},
                                detail_lose_counter_1 = {'name': counter_data['loseCounter'][0]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['loseCounter'][0]['winRate']},
                                detail_lose_counter_2 = {'name': counter_data['loseCounter'][1]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['loseCounter'][1]['winRate']},
                                detail_lose_counter_3 = {'name': counter_data['loseCounter'][2]['championImg'].split("/")[7].split(".")[0], 'winRate': counter_data['loseCounter'][2]['winRate']},
                                detail_rune_1 = rune_data['version1'],
                                detail_rune_2 = rune_data['version2'],
                                detail_skill_master = json.loads(rows[10]),
                                detail_skill_build = json.loads(rows[11]),
                                detail_spell = json.loads(rows[7]),
                                detail_start = json.loads(rows[8]),
                                detail_shoes = json.loads(rows[9]),
                                detail_item_build = json.loads(rows[12]),
                                detail_use_legend = json.loads(rows[13]),)
                
                # 연결 종료
                conn.close()
                
        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}")

# post_data()

def statiacs_data():
    # 데이터베이스 파일 경로 설정
    db_path = os.path.join('myfrontend', 'server', 'crawling', 'dbData', 'data.db')

    # 경로와 파일이 존재하는지 확인
    if not os.path.exists(db_path):
        print(f"Error: The database file at {db_path} does not exist.")
    else:
        # SQLite 데이터베이스 연결
        try:
            conn = sqlite3.connect(db_path)
                
            # 커서 생성
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM cham;")
            rows = cursor.fetchall()
            # 데이터 출력
            print(f"Data from cham table :")
            for index, row in enumerate(rows):
                ranking, champ_name, play, kda, win, pick, ban, cs, gold, img, position, tier = row 
                data = Champion.objects.filter(champion_name = champ_name)
                for i in data:
                    img = i.champion_img
                    id = i.champion_id
                    
                AllStaticsData.objects.get_or_create(
                                    statics_tier = tier,
                                    statics_position = position,
                                    statics_ranking = ranking,
                                    statics_champ_name = champ_name,
                                    statics_champ_img = img,
                                    statics_champ_id = id,
                                    statics_play = play,
                                    statics_kda = kda,
                                    statics_win = win,
                                    statics_pick = pick,
                                    statics_ban = ban,
                                    statics_cs = cs,
                                    statics_gold = gold,)
            
            # 연결 종료
            conn.close()
                
        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}")

statiacs_data()

# ----------------------------------------------------------------------

request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

api_key = "api_key=RGAPI-d7f2268a-7c6a-4551-b4bd-092cb9d35f94"

# api 호출
def get_data(url):
    try:
        response = requests.get(url, headers= request_headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            if response.status_code == 429:
                for i in range(60):
                    time.sleep(1)
                    if i % 10 == 0:
                        print(i)
            return None 
    except Exception as e:
        print("An error occurred:", e)
        return None

# 대표 룬 이미지 얻기
def get_title_rune_img(rune_id):
    get_rune_data = get_data('https://ddragon.leagueoflegends.com/cdn/14.11.1/data/ko_KR/runesReforged.json')
    
    for rune_data in get_rune_data:
        if rune_id == rune_data['id']:
            return rune_data['icon']

# 하위 룬 이미지 얻기
def get_rune_img(rune_id, line_id):
    get_rune_data = get_data('https://ddragon.leagueoflegends.com/cdn/14.11.1/data/ko_KR/runesReforged.json')
    
    for rune_data in get_rune_data:
        if rune_id == rune_data['id']:
            for slot in rune_data['slots']:
                for rune in slot['runes']:
                    if line_id == rune['id']:
                        return rune['icon']
                        
# 챔피언 자료구조 초기화
def get_detail_data():
    game_all_data = AllGameData.objects.all()
    now_version = Version.objects.values_list('version', flat=True).first()
        
    def data_set_champions():
        champ_data = Champion.objects.all().order_by("champion_name")
        structure_data = {}
        for data in champ_data:
            structure_data[data.champion_id] = {
                "name": data.champion_name, "id": data.champion_id, "tier": "", 'line': "", "total": 0, "win": '', "lose": '', "ban": '',"perk": { }, "gold": 0, "kda": 0.0
            }
        return structure_data
    
    champ_dict = data_set_champions()
    # print(champ_dict)
    
    # line_dict = {"TOP": [], "JUNGLE": [], "MIDDLE": [], "BOTTOM": [], "UTILITY": []}
    # tier_dict = {tier: {line: copy.deepcopy(data_set_champions()) for line in line_dict} for tier in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']}

    for index, all_data in enumerate(game_all_data):
        # print(all_data.all_game_data)
        
        if all_data.all_game_version == str(now_version):
            user_game_data = all_data.all_game_data['info']['participants']
            
            # 유저별 이므로 총 10번 반복됨
            for index, game_data in enumerate(user_game_data):
                # print(game_data)
                # kda _평점 (통계용)
                kda = game_data['challenges']['kda']
                # 사용한 전설 아이템 _배열형태 (디테일용)
                legend_items = game_data['challenges']['legendaryItemUsed']
                
                # 챔피언 이름 (통계용, 디테일용)
                champ_name = game_data['championName']
                # 골드 획득량 (통계용)
                gold = game_data['goldEarned']
                # 라인 (통계용)
                line = game_data['teamPosition']
                
                # 룬 id 추출 (디테일용)
                #  https://ddragon.leagueoflegends.com/cdn/14.11.1/data/ko_KR/runesReforged.json
                #  해당 룬 아이디는 위 주소를 통해 api를 호출하여 img src 를 얻어낼 예정
                perks = game_data['perks']
                # 정복자 라인 (주룬)
                main_id = perks['styles'][0]['style']
                main_id_img = get_title_rune_img(main_id)
                # 기발 라인
                main_title = perks['styles'][0]['selections'][0]['perk']
                main_title_img = get_rune_img(main_id, main_title)
                # 승전보
                main_line_1 = perks['styles'][0]['selections'][1]['perk']
                main_line_1_img = get_rune_img(main_id, main_line_1)
                # 강인함
                main_line_2 = perks['styles'][0]['selections'][2]['perk']
                main_line_2_img = get_rune_img(main_id, main_line_2)
                # 최후의 일결
                main_line_3 = perks['styles'][0]['selections'][3]['perk']
                main_line_3_img = get_rune_img(main_id, main_line_3)
                # (부룬)
                sub_title = perks['styles'][1]['style']
                main_title_img = get_title_rune_img(sub_title)
                sub_line_1 = perks['styles'][1]['selections'][0]['perk']
                sub_line_1_img = get_rune_img(sub_title, sub_line_1)
                sub_line_2 = perks['styles'][1]['selections'][1]['perk']
                sub_line_2_img = get_rune_img(sub_title, sub_line_2)
                
                # (디테일용)
                #  해당 룬 및 전설 아이템 승률을 위하여 추출
                win = game_data['win']
                
                # 통계 내기
                if "total" in champ_dict[champ_name]:
                    champ_dict[champ_name]['total'] += 1
                else:
                    champ_dict[champ_name]['total'] = 1
                    
                if index == 0:
                    break
            
        
        if index == 0:
            break
    
# get_detail_data()



# ------------------------------------아래 함수는 전체 게임 데이터를 db에 저장하는 함수

# def get_game_data():
#     start_url = "https://asia.api.riotgames.com/lol/match/v5/matches/"
    
#     match_id_all = MatchData.objects.all()
    
#     for index, m_id in enumerate(match_id_all):
#         url = start_url + str(m_id) + "?" + api_key
        
#         try:
#             match_data = get_data(url)
            
#             ver_data = match_data['info']['gameVersion']
#             ver_split = ver_data.split('.')
#             ver = ver_split[0] + "." + ver_split[1] + ".1"
            
#             AllGameData.objects.get_or_create(all_game_version = ver, all_game_data = match_data)

#             print(str(m_id) + " End")
#         except TypeError as e:
#             if "'NoneType' object is not subscriptable" in str(e):
#                 print("NoneType 에러 발생.")
#                 continue  # 예외 발생 시 None 반환 또는 원하는 동작 수행
        
# get_game_data()

