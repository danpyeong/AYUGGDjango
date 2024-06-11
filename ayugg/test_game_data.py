from django.db import connection
import copy
import operator
from django.db import transaction
from main.models import MatchInfoData, Version, Champion, MatchData


def statics_data():
    connection.close_if_unusable_or_obsolete()  # 기존 연결을 닫아 새로운 연결을 맺기 위한 초기화
    version = Version.objects.values_list('version', flat=True).first()
    match_data = MatchInfoData.objects.filter(match_data_version=version).exclude(line='invalid')
    champ_data = Champion.objects.all().order_by("champion_name")

    def data_set_champions():
        try:
            structure_data = {}
            for data in champ_data:
                counter_champ = {}
                for strc_data in champ_data:
                    counter_champ[strc_data.champion_name] = {"win": 0, "lose": 0}

                structure_data[data.champion_name] = {"tier": "", 'line': "", "total": 0, "win": 0, "lose": 0, "ban": 0, "counter": counter_champ}
            return structure_data

        except TypeError as e:
            print(f"TypeError occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    line_dict = {"TOP": [], "JUNGLE": [], "MIDDLE": [], "BOTTOM": [], "UTILITY": []}
    tier_dict = {tier: {line: data_set_champions() for line in line_dict} for tier in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']}

    match_version = {version: tier_dict}
    
    def input_data(match_version):
        ban_struct = []
        for data in match_data:
            champ_data = match_version[str(data.match_data_version)][data.game_tier][data.line]
            play_champ_name = champ_data[data.champion_name]
            vs_champ_name = data.versus_name
            versus = play_champ_name['counter'][vs_champ_name]

            play_champ_name['total'] += 1
            if data.win == "False":
                play_champ_name['lose'] += 1
                versus['lose'] += 1
            elif data.win == "True":
                play_champ_name['win'] += 1
                versus['win'] += 1

            if data.bans not in ban_struct:
                for ban_name in data.bans:
                    if str(ban_name) != 'None':
                        ban_champ_name = champ_data[ban_name]
                        ban_champ_name['ban'] += 1
                ban_struct.append(data.bans)

        return match_version

    game_data = input_data(match_version)

    def calc_data(game_data):
        res = {}
        total_pick = MatchData.objects.all().count()
        calc_match_data = copy.deepcopy(match_version)

        for game_ver in game_data:
            for tier in tier_dict:
                for line in line_dict:
                    for index, champ in enumerate(champ_data):
                        data_ = game_data[game_ver][tier][line][str(champ)]
                        play_total = data_['total']
                        win = data_['win']
                        counter = data_['counter']
                        ban = data_['ban']

                        if play_total != 0:
                            pick_rate = round(play_total / total_pick, 4) * 100
                            win_rate = round(win / play_total, 4) * 100
                            ban_rate = round(ban / total_pick, 4) * 100

                            counter_dict = {}
                            for name in champ_data:
                                name = str(name)
                                win_ = counter[name]['win']
                                lose_ = counter[name]['lose']
                                game_ = win_ + lose_

                                if win_ != 0 and game_ != 0:
                                    counter_win_rate = round(win_ / game_, 4) * 100
                                    counter_dict[name] = counter_win_rate

                            counter_dict_sorted = sorted(counter_dict.items(), key=operator.itemgetter(1))

                            res['version'] = game_ver
                            res['line'] = line
                            res['tier'] = tier
                            res['name'] = str(champ)
                            img_db = Champion.objects.filter(champion_name=str(champ)).values_list('champion_img', flat=True).first()
                            res['img'] = img_db
                            res['pick'] = pick_rate
                            res['win'] = win_rate
                            res['ban'] = ban_rate
                            counter1 = {}
                            counter2 = {}
                            counter3 = {}
                            none = {'name': 'N/A', 'img': 'N/A'}

                            if len(counter_dict_sorted) > 0:
                                counter1['name'] = counter_dict_sorted[0][0]
                                counter1_img_db = Champion.objects.filter(champion_name=counter_dict_sorted[0][0]).values_list('champion_img', flat=True).first()
                                counter1['img'] = counter1_img_db
                                res['counter1'] = counter1
                            else:
                                res['counter1'] = none

                            if len(counter_dict_sorted) > 1:
                                counter2['name'] = counter_dict_sorted[1][0]
                                counter2_img_db = Champion.objects.filter(champion_name=counter_dict_sorted[1][0]).values_list('champion_img', flat=True).first()
                                counter2['img'] = counter2_img_db
                                res['counter2'] = counter2
                            else:
                                res['counter2'] = none

                            if len(counter_dict_sorted) > 2:
                                counter3['name'] = counter_dict_sorted[2][0]
                                counter3_img_db = Champion.objects.filter(champion_name=counter_dict_sorted[2][0]).values_list('champion_img', flat=True).first()
                                counter3['img'] = counter3_img_db
                                res['counter3'] = counter3
                            else:
                                res['counter3'] = none

                            calc_match_data[game_ver][tier][line][str(champ)] = copy.deepcopy(res)
                            
                        if play_total == 0:
                            res['version'] = game_ver
                            res['line'] = line
                            res['tier'] = tier
                            res['name'] = str(champ)
                            img_db = Champion.objects.filter(champion_name=str(champ)).values_list('champion_img', flat=True).first()
                            res['img'] = img_db
                            res['pick'] = 0
                            res['win'] = 0
                            res['ban'] = 0
                            
                            res['counter1'] = {'name': 'N/A', 'img': 'N/A'}
                            res['counter2'] = {'name': 'N/A', 'img': 'N/A'}
                            res['counter3'] = {'name': 'N/A', 'img': 'N/A'}


        return calc_match_data

    data = calc_data(game_data)
    return data

data = statics_data()

p = data['14.11.1']['PLATINUM']['BOTTOM']
# 예상 결과값
# {'가렌': }
print(p)
