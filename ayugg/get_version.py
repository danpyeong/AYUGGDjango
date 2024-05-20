from main.models import Version, Champion, ChampionBasicInfo
import requests

version_url = "https://ddragon.leagueoflegends.com/api/versions.json"

# api 호출
def get_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


# 버전
# Version.objects.all().delete()
versions = get_data(version_url)
Version.objects.get_or_create(version = versions[0])
version = Version.objects.values_list('version', flat=True).first()

champ_info_data_url_list = []
champ_eng_name_list = []

# # 전체 챔피언
# Champion.objects.all().delete()
def get_champions_all_data():
    champions_url = "https://ddragon.leagueoflegends.com/cdn/" + version + "/data/ko_KR/champion.json"
    champions_rawdata = get_data(champions_url)
    champions = champions_rawdata['data']

    for data in champions:
        champions_name = data # 영어 이름
        champ_eng_name_list.append(champions_name)
        champ_data = champions[str(data)]
        
        ver = Version.objects.get(version=version)
        id = champ_data['id']
        key = champ_data['key']
        kr_name = champ_data['name']
        img = champ_data['image']
        img_full = img['full']
        
        Champion.objects.get_or_create(
            champion_version = ver, champion_id = id, champion_key = key, champion_name = kr_name, champion_img = img_full)
        
        champ_info_data_url = "https://ddragon.leagueoflegends.com/cdn/" + str(ver) +"/data/ko_KR/champion/" + data + ".json"
        champ_info_data_url_list.append(champ_info_data_url)
        
    print("Get Champions All Data End")
    
get_champions_all_data()

# ChampionBasicInfo.objects.all().delete()
def get_champion_info_data():
    for index, url in enumerate(champ_info_data_url_list):
        rawdata = get_data(url)
        rawdata = rawdata['data']
        data = rawdata[champ_eng_name_list[index]]

        ver = Version.objects.get(version=version)
        
        # 챔피언 패시브
        passive = data['passive']
        p_name = passive['name']
        p_info = passive['description']
        p_img = passive['image']
        p_img = p_img['full']
        
        # 챔피언 스킬 데이터
        spells = data['spells']
        
        spell_name = []
        spell_info = []
        spell_img = []
        
        for spell in spells:
            spell_name.append(spell['id'])
            spell_info.append(spell['description'])
            img = spell['image']
            img = img['full']
            spell_img.append(img)
        
        # 챔피언 이미지(full 버전)
        champ_img = data['image']
        champ_img = champ_img['full']
        
        ChampionBasicInfo.objects.get_or_create(
            champ_version = ver,
            champ_id = data['id'],
            champ_key = data['key'],
            champ_name = data['name'],
            champ_img = champ_img,
            champion_passive_name = p_name, champion_passive_info = p_info, champion_passive_img = p_img,
            champion_q_name = spell_name[0], champion_q_info = spell_info[0], champion_q_img = spell_img[0],
            champion_w_name = spell_name[1], champion_w_info = spell_info[1], champion_w_img = spell_img[1],
            champion_e_name = spell_name[2], champion_e_info = spell_info[2], champion_e_img = spell_img[2],
            champion_r_name = spell_name[3], champion_r_info = spell_info[3], champion_r_img = spell_img[3],
            )
        
        print("Basic Data End :" + str(index + 1))
        
get_champion_info_data()