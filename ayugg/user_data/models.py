from django.db import models

class userModel(models.Model):
    gameName = models.CharField(max_length=16)
    tagLine = models.CharField(max_length=5, default='KR1')
    puuid = models.CharField(max_length=78)
    id = models.CharField(max_length=63, primary_key=True)
    profileIconId = models.IntegerField()
    summonerLevel = models.CharField(max_length=50)
    rank = models.CharField(max_length=50, default='NONE')
    tier = models.CharField(max_length=50, default=' ')
    leaguePoints = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    
    #입력시 [] 
    matchList = models.JSONField()
    # 입력시 [{},{}]
    matches = models.JSONField()
    #입력시 [] 
    matchNum = models.JSONField()


    def __str__(self):
        return self.puuid
    