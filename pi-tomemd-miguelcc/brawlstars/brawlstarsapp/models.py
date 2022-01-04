from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Club(models.Model):
    tag = models.CharField(max_length= 10, primary_key= True)
    name = models.CharField(max_length= 30)
    desc = models.CharField(max_length= 100, null=True, blank=True)
    type = models.CharField(max_length= 15)
    reqTrophies = models.IntegerField()
    trophies = models.IntegerField()

class Player(models.Model):
    tag = models.CharField(max_length= 10, primary_key= True)
    name = models.CharField(max_length= 30)
    trophies = models.IntegerField()
    soloVictories = models.IntegerField()
    duoVictories = models.IntegerField()
    trioVictories = models.IntegerField()
    club = models.ForeignKey(Club, on_delete = models.CASCADE, null=True)

class GroupBattle(models.Model):
    eventId = models.IntegerField()
    dateTime = models.DateTimeField()
    mode = models.CharField(max_length= 15)
    map = models.CharField(max_length= 20, null=True)
    type = models.CharField(max_length= 20)
    duration = models.IntegerField()
    mvp = models.ForeignKey(Player, on_delete = models.CASCADE, null=True)

class OnlyBattle(models.Model):
    eventId = models.IntegerField()
    dateTime = models.DateTimeField()
    mode = models.CharField(max_length= 15)
    map = models.CharField(max_length= 20, null=True)
    type = models.CharField(max_length= 20)
    trophyChange = models.IntegerField(null=True)

class PlayerGroupBattle(models.Model):
    groupBattle = models.ForeignKey('GroupBattle', on_delete = models.CASCADE)
    player = models.ForeignKey('Player', on_delete = models.CASCADE)
    result = models.CharField(max_length= 10)
    brawler = models.CharField(max_length=20, null=True)
    starPlayer = models.BooleanField()

class PlayerOnlyBattle(models.Model):
    onlyBattle = models.ForeignKey('OnlyBattle', on_delete = models.CASCADE)
    player = models.ForeignKey('Player', on_delete = models.CASCADE)
    rank = models.IntegerField()
    brawler = models.CharField(max_length=20, null=True)