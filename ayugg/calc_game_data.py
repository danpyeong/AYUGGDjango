from main.models import MatchInfoData, Version, Champion
import requests


version = Version.objects.values_list('version', flat=True).first()
match_data = MatchInfoData.objects.filter(match_data_version = version).exclude(line = 'invalid')

def data_set_champions():
    try:
        champ_data = Champion.objects.all().order_by("champion_name")
        
        calc_data = {}
        
        # 카운터 승률 계산을 위한 자료구조 초기화 
        counter_champ = {}
        for data in champ_data:
            counter_champ[data.champion_name] = { "win": 0, "lose": 0 }
        
        for data in champ_data:
            calc_data[data.champion_name] = { "total" : 0, "win": 0, "lose": 0, "counter": counter_champ }
        
        return calc_data
    
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
        
        print("-" * 20)
        print("Play : " + str(data.champion_name) + " / Versus : " + str(vs_champ))
        print("토탈 : " + str(play_champ['total']) + 
              " / 승리 : " + str(play_champ['win']) + " / 패배 : " + str(play_champ['lose']))
        print("카운터 : " + str(versus))
        print("-" * 20)
                
        if index == 49:
            break

input_data(champ_data)    


# "가렌" : {
#         "total" : 10,
#         "win" : 0,
#         "lose" : 0,
#         "counter" : {
#             "아리" : { "win" : 20, "lose" : 0 }
            
#         }
# }