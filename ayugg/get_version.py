from main.models import Version, Champion, ChampionBasicInfo
import requests

version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
champions_url = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/ko_KR/champion.json"


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
def get_version():
    versions = get_data(version_url)
    Version.objects.get_or_create(version = versions[0])
    now_version = Version.objects.all()
    
    print("Version Data End")
    return now_version[0]

now_ver = get_version()

champ_info_data_url_list = []
champ_eng_name_list = []
# # 전체 챔피언
def get_champions_all_data():
    champions_rawdata = get_data(champions_url)
    champions = champions_rawdata['data']

    for data in champions:
        champions_name = data # 영어 이름
        champ_eng_name_list.append(champions_name)
        champ_data = champions[str(data)]
        
        key = champ_data['key']
        kr_name = champ_data['name']
        img = champ_data['image']
        img_full = img['full']
        
        Champion.objects.get_or_create(
            version = now_ver, champion_key = key, champion_name = kr_name, champion_img = img_full)
        
        champ_info_data_url = "https://ddragon.leagueoflegends.com/cdn/" + str(now_ver) +"/data/ko_KR/champion/" + data + ".json"
        champ_info_data_url_list.append(champ_info_data_url)
        
        
    print("Get Champions All Data End")
    
get_champions_all_data()

def get_champion_info_data():
    for index, url in enumerate(champ_info_data_url_list):
        rawdata = get_data(url)
        rawdata = rawdata['data']
        data = rawdata[champ_eng_name_list[index]]
        
        print(Champion.objects.all())
        
        # key = Champion.objects.filter('champion_key')
        # kr_name = Champion.objects.filter('champion_name')
        # img = data['image']
        # img = Champion.objects.filter('champion_img')
        
        passive = data['passive']
        p_name = passive['name']
        p_info = passive['description']
        p_img = passive['image']
        p_img = p_img['full']
         
        spells = data['spells']
        
        spell_name = []
        spell_info = []
        spell_img = []
        
        for spell in spells:
            spell_name.append(spell['id'])
            # spell_info.append(spell['description'])
            # img = spell['image']
            # img = img['full']
            # spell_img.append(img)
        
        # ChampionBasicInfo.objects.get_or_create(
        #     version = now_ver, champion_key = key, champion_name = kr_name, champion_img = img,
        #     champion_passive_name = p_name, champion_passive_info = p_info, champion_passive_img = p_img,
        #     champion_q_name = spell_name[0], champion_q_info = spell_info[0], champion_q_img = spell_img[0],
        #     champion_w_name = spell_name[1], champion_w_info = spell_info[1], champion_w_img = spell_img[1],
        #     champion_e_name = spell_name[2], champion_e_info = spell_info[2], champion_e_img = spell_img[2],
        #     champion_r_name = spell_name[3], champion_r_info = spell_info[3], champion_r_img = spell_img[3],
        #     )
        
        print("Basic Data End :" + index)
        
        # print(data)
        if index == 0:
            break
        
get_champion_info_data()