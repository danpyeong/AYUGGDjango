from django.db import models

class ChampionBasicInfo(models.Model):
    champion_name = models.CharField(max_length=50)
    champion_img = models.TextField()
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