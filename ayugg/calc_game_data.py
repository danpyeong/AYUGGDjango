import copy
import operator
from django.db import transaction
from main.models import MatchInfoData, Version, Champion, MatchData, StaticsChampionMiddleData

def statics_data():
    version = Version.objects.values_list('version', flat=True).first()
    match_data = MatchInfoData.objects.filter(match_data_version=version).exclude(line='invalid')
    champ_data = Champion.objects.all().order_by("champion_name")

    def data_set_champions():
        structure_data = {}
        for data in champ_data:
            counter_champ = {strc_data.champion_name: {"win": 0, "lose": 0} for strc_data in champ_data}
            structure_data[data.champion_name] = {
                "tier": "", 'line': "", "total": 0, "win": 0, "lose": 0, "ban": 0, "counter": counter_champ
            }
        return structure_data

    line_dict = {"TOP": [], "JUNGLE": [], "MIDDLE": [], "BOTTOM": [], "UTILITY": []}
    tier_dict = {tier: {line: copy.deepcopy(data_set_champions()) for line in line_dict} for tier in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']}

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

        for game_ver, game_ver_data in game_data.items():
            for tier, tier_data in game_ver_data.items():
                for line, line_data in tier_data.items():
                    for champ_name, data_ in line_data.items():
                        play_total = data_['total']
                        win = data_['win']
                        counter = data_['counter']
                        ban = data_['ban']
                        
                        if play_total != 0:
                            pick_rate = round(play_total / total_pick, 4) * 100
                            win_rate = round(win / play_total, 4) * 100
                            ban_rate = round(ban / total_pick, 4) * 100

                            counter_dict = {}
                            for name, counter_data in counter.items():
                                win_ = counter_data['win']
                                lose_ = counter_data['lose']
                                game_ = win_ + lose_

                                if game_ != 0:
                                    counter_win_rate = round(win_ / game_, 4) * 100
                                    counter_dict[name] = counter_win_rate

                            counter_dict_sorted = sorted(counter_dict.items(), key=operator.itemgetter(1))

                            # res['version'] = game_ver
                            # res['line'] = data_['line']
                            # res['tier'] = data_['tier']
                            # res['name'] = champ_name
                            img_db = Champion.objects.filter(champion_name=champ_name).values_list('champion_img', flat=True).first()
                            # res['img'] = img_db
                            # res['pick'] = pick_rate
                            # res['win'] = win_rate
                            # res['ban'] = ban_rate

                            counter_res = []
                            none = {'name': 'N/A', 'img': 'N/A'}

                            for i in range(3):
                                if i < len(counter_dict_sorted):
                                    counter_name = counter_dict_sorted[i][0]
                                    counter_img = Champion.objects.filter(champion_name=counter_name).values_list('champion_img', flat=True).first()
                                    counter_res.append({'name': counter_name, 'img': counter_img})
                                else:
                                    counter_res.append(none)

                            # res['counter1'], res['counter2'], res['counter3'] = counter_res
                
                            match_version[game_ver][tier][line][champ_name] = copy.deepcopy(res)

                            StaticsChampionMiddleData.objects.get_or_create(
                                champ_middle_data_version = game_ver,
                                champ_middle_data_line = line,
                                champ_middle_data_tier = tier,
                                champ_middle_data_name = champ_name,
                                champ_middle_data_img = img_db,
                                champ_middle_data_pick = pick_rate,
                                champ_middle_data_win = win_rate,
                                champ_middle_data_ban = ban_rate,
                                champ_middle_data_counter1 = counter_res[0],
                                champ_middle_data_counter2 = counter_res[1],
                                champ_middle_data_counter3 = counter_res[2],)
                    
                    print(line + " , " + tier)
        
        return match_version

    data = calc_data(game_data)
    return data

data = statics_data()
