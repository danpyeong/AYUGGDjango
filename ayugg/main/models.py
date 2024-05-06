from django.db import models

class Version(models.Model):
    version = models.CharField(max_length=10)
    
    def __str__(self):
        return self.version

class Champion(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name = 'champion_version')
    champion_key = models.CharField(max_length=5)
    champion_name = models.CharField(max_length=20)
    champion_img = models.TextField()
    
    def __str__(self):
        return self.champion

class ChampionBasicInfo(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name = 'basic_info_version')
    champion_key = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name = 'basic_info_champion_key')
    champion_name = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name = 'basic_info_champion_name')
    champion_img = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name = 'basic_info_champion_img')
    champion_passive_name = models.CharField(max_length=25)
    champion_passive_img = models.TextField()
    champion_passive_info = models.TextField()
    champion_q_name = models.CharField(max_length=25)
    champion_q_img = models.TextField()
    champion_q_info = models.TextField()
    champion_w_name = models.CharField(max_length=25)
    champion_w_img = models.TextField()
    champion_w_info = models.TextField()
    champion_e_name = models.CharField(max_length=25)
    champion_e_img = models.TextField()
    champion_e_info = models.TextField()
    champion_r_name = models.CharField(max_length=25)
    champion_r_img = models.TextField()
    champion_r_info = models.TextField()
    
    def __str__(self):
        return self.champion_name
    
class MatchData(models.Model):
    match_id = models.CharField(max_length=30)
    
    def __str__(self):
        return self.champion_name