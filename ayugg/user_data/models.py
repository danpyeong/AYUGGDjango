from django.db import models

class userModel(models.Model):
    gameName = models.CharField(max_length=16)
    tagLine = models.CharField(max_length=5)
    puuid = models.CharField(max_length=78)
    summonerId = models.CharField(max_length=63)
    profileIconId = models.IntegerField()
    summonerLevel = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    tier = models.CharField(max_length=50)
    leaguePoints = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    
    #입력시 [] 
    matchList = models.JSONField()
    # 입력시 [{},{}]
    matches = models.JSONField()


    def __str__(self):
        return self.puuid
    