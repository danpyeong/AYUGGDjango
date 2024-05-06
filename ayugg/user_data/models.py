from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

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

    # matchList = ArrayField(
    #     models.CharField(max_length=50),
    #     blank=True,
    #     default=list
    # )
    
    matches = JSONField()
    
    # matches = ListJSONField()

    def __str__(self):
        return self.puuid
    
# class ListJSONField(models.Field):
#     """
#     리스트 안에 JSONField를 포함하는 커스텀 필드
#     """
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def db_type(self, connection):
#         return 'jsonb'  # PostgreSQL의 JSONB 형식을 사용하고 있는 예시입니다.

#     def from_db_value(self, value, expression, connection):
#         if value is None:
#             return value
#         return [JSONField().to_python(item) for item in value]

#     def to_db_value(self, value, connection):
#         if value is None:
#             return value
#         return [JSONField().get_prep_value(item) for item in value]
