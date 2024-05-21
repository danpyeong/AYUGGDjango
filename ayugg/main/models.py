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
    match_id = models.CharField(max_length=30, primary_key = True)
    
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