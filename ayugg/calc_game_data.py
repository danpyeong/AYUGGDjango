from main.models import MatchInfoData, Version, Champion, MatchData
import requests


version = Version.objects.values_list('version', flat=True).first()
match_data = MatchInfoData.objects.filter(match_data_version = version).exclude(line = 'invalid')

def data_set_champions():
    try:
        champ_data = Champion.objects.all().order_by("champion_name")
        
        structure_data = {}
        
        for data in champ_data:
            # 카운터 승률 계산을 위한 자료구조 초기화 
            counter_champ = {}
            for strc_data in champ_data:
                counter_champ[strc_data.champion_name] = { "win": 0, "lose": 0 }
                
            structure_data[data.champion_name] = { "total" : 0, "win": 0, "lose": 0, "counter": counter_champ }
        
        return structure_data
    
    except TypeError as e:
        print(f"TypeError occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

champ_data = data_set_champions()

def input_data(champ_data):
    for index, data in enumerate(match_data):
        play_champ = champ_data[data.champion_name]
        vs_champ = data.versus_name
        versus = play_champ['counter'][vs_champ]

        if data.win == "False":
            play_champ['total'] += 1
            play_champ['lose'] += 1
            versus['lose'] += 1
        else:
            play_champ['total'] += 1
            play_champ['win'] += 1
            versus['win'] += 1
                
        # if index == 0:
        #     break
    return champ_data

data = input_data(champ_data)

# print(data)

def calc_data():
    total_pick = MatchData.objects.all().count()
    print(MatchData.objects.all().count())

calc_data()

# "가렌" : {
#         "total" : 10,
#         "win" : 0,
#         "lose" : 0,
#         "counter" : {
#             "아리" : { "win" : 20, "lose" : 0 }
            
#         }
# }