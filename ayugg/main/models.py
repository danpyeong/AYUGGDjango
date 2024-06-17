import uuid
from django.db import models
# from jsonfield import JSONField

class Version(models.Model):
    version = models.CharField(max_length=10, primary_key=True)
    
    def __str__(self):
        return self.version

class Champion(models.Model):
    champion_version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='champion_version')
    champion_id = models.CharField(max_length=20)
    champion_key = models.CharField(max_length=5, primary_key=True)
    champion_name = models.CharField(max_length=20)
    champion_img = models.TextField()
    
    def __str__(self):
        return self.champion_name

class ChampionBasicInfo(models.Model):
    champ_version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='champ_version')
    champ_id = models.CharField(max_length=20)
    champ_key = models.CharField(max_length=5, primary_key=True)
    champ_name = models.CharField(max_length=20)
    champ_img = models.TextField()
    champion_passive_name = models.CharField(max_length=50)
    champion_passive_img = models.TextField()
    champion_passive_info = models.TextField()
    champion_q_name = models.CharField(max_length=50)
    champion_q_img = models.TextField()
    champion_q_info = models.TextField()
    champion_w_name = models.CharField(max_length=50)
    champion_w_img = models.TextField()
    champion_w_info = models.TextField()
    champion_e_name = models.CharField(max_length=50)
    champion_e_img = models.TextField()
    champion_e_info = models.TextField()
    champion_r_name = models.CharField(max_length=50)
    champion_r_img = models.TextField()
    champion_r_info = models.TextField()
    
    def __str__(self):
        return self.champ_name

class MatchData(models.Model):
    match_version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='match_version')
    tier = models.CharField(max_length=10)
    match_id = models.CharField(max_length=30)
    
    def __str__(self):
        return self.match_id

class MatchInfoData(models.Model):
    game_tier = models.CharField(max_length=30)
    match_data_version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='match_data_version')
    match_id = models.CharField(max_length=30)
    team_id = models.CharField(max_length=5)
    champion_name = models.CharField(max_length=30)
    champion_id = models.CharField(max_length=30)
    champion_key = models.CharField(max_length=5)
    versus_name = models.CharField(max_length=30)
    versus_id = models.CharField(max_length=30)
    versus_key = models.CharField(max_length=5)
    win = models.CharField(max_length=10)
    line = models.CharField(max_length=10)
    perks = models.TextField()
    item = models.JSONField(default=list)
    bans = models.JSONField(default=list)
    
    def __str__(self):
        return self.match_id
    

class StaticsChampionMiddleData(models.Model):
    champ_middle_data_version = models.CharField(max_length = 15)
    champ_middle_data_line = models.CharField(max_length = 20)
    champ_middle_data_tier = models.CharField(max_length = 20)
    champ_middle_data_name = models.CharField(max_length = 30)
    champ_middle_data_img = models.CharField(max_length = 30)
    champ_middle_data_pick = models.CharField(max_length = 30)
    champ_middle_data_win = models.CharField(max_length = 30)
    champ_middle_data_ban = models.JSONField()
    champ_middle_data_counter1 = models.JSONField()
    champ_middle_data_counter2 = models.JSONField()
    champ_middle_data_counter3 = models.JSONField()
    
    def __str__(self):
        data = [self.champ_middle_data_tier, self.champ_middle_data_line]
        return data
    
class AllGameData(models.Model):
    all_game_version = models.CharField(max_length = 15)
    all_game_data = models.JSONField()

# 수정 필요
# class AllGameData(models.Model):
#     all_game_version = models.CharField(max_length = 15)
#     all_game_tier = models.CharField(max_length = 15) -> 아마 유저 한 명의 티어를 뽑아내어 그 티어로 해야할 것 같음
#     all_game_data = models.JSONField() -> 해당 게임 총 데이터
#     all_timeline_data = models.JSONField() -> 해당 게임 총 타임라인별 데이터
    
# class AllStaticsData(models.Model):

class ChampionDetails(models.Model):
    detail_champ_id = models.CharField(max_length = 20)
    detail_champ_name = models.CharField(max_length = 20)
    detail_win_counter_1 = models.JSONField()
    detail_win_counter_2 = models.JSONField()
    detail_win_counter_3 = models.JSONField()
    detail_lose_counter_1 = models.JSONField()
    detail_lose_counter_2 = models.JSONField()
    detail_lose_counter_3 = models.JSONField()
    detail_rune_1 = models.JSONField()
    detail_rune_2 = models.JSONField()
    detail_skill_master = models.JSONField()
    detail_skill_build = models.JSONField()
    detail_spell = models.JSONField()
    detail_start = models.JSONField()
    detail_shoes = models.JSONField()
    detail_item_build = models.JSONField()
    detail_use_legend = models.JSONField()
    