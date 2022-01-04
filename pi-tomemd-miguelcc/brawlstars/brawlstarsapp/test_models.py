from django.test import TestCase
from django.contrib.auth.models import User
import pendulum
from .models import *

class ModelsTestCase(TestCase):
    # Crear jugadores
    def setUp(self):
        User.objects.create_user(username="test", password="testpasswd")
        Club.objects.create(tag = "#000000000", name = "nombre club", desc = "descripción", type = "open", reqTrophies = 1000, trophies = 15000)

        club = Club.objects.get(tag="#000000000")
        Player.objects.create(tag = "#00000001", name = "nombre jugador", trophies = 5000, soloVictories = 50, duoVictories = 100, trioVictories = 150, club = club)
        Player.objects.create(tag = "#00000002", name = "nombre jugador", trophies = 5000, soloVictories = 50, duoVictories = 100, trioVictories = 150, club = club)

        dt = pendulum.parse("20210525T172708.000Z", tz='Europe/Madrid')
        player1 = Player.objects.get(tag="#00000001")
        player2 = Player.objects.get(tag="#00000002")
        OnlyBattle.objects.create(eventId = 0, dateTime = dt, mode = "modo", map = "mapa", trophyChange = 10)
        GroupBattle.objects.create(eventId = 1, dateTime = dt, mode = "modo", map = "mapa", mvp =player2 , duration = 100)

        onlyBattle = OnlyBattle.objects.get(id=1)
        groupBattle = GroupBattle.objects.get(id=1)
        PlayerOnlyBattle.objects.create(onlyBattle = onlyBattle, player = player1, rank = 1, brawler = 'NITA')
        PlayerGroupBattle.objects.create(groupBattle = groupBattle, player = player2, result = 'victory', brawler = 'SHELLY', starPlayer=True)

    def test_get_player(self):
        player = Player.objects.get(tag="#00000001")
        
        self.assertEquals(player.tag, "#00000001")
        self.assertEquals(player.name, "nombre jugador")
        self.assertEquals(player.trophies, 5000)
        self.assertEquals(player.soloVictories, 50)
        self.assertEquals(player.duoVictories, 100)
        self.assertEquals(player.trioVictories, 150)
        self.assertEquals(player.club, Club.objects.get(tag="#000000000"))

    def test_get_club(self):
        club = Club.objects.get(tag = "#000000000")

        self.assertEquals(club.tag, "#000000000")
        self.assertEquals(club.name, "nombre club")
        self.assertEquals(club.desc, "descripción")
        self.assertEquals(club.type, "open")
        self.assertEquals(club.reqTrophies, 1000)
        self.assertEquals(club.trophies, 15000)
    
    def test_get_only_battle(self):
        battle = OnlyBattle.objects.get(id=1)

        self.assertEquals(battle.eventId, 0)
        self.assertEquals(battle.dateTime, pendulum.parse("20210525T172708.000Z", tz='Europe/Madrid'))
        self.assertEquals(battle.mode, "modo")
        self.assertEquals(battle.map, "mapa")
        self.assertEquals(battle.trophyChange, 10)

    def test_get_group_battle(self):
        battle = GroupBattle.objects.get(id=1)

        self.assertEquals(battle.eventId, 1)
        self.assertEquals(battle.dateTime, pendulum.parse("20210525T172708.000Z", tz='Europe/Madrid'))
        self.assertEquals(battle.mode, "modo")
        self.assertEquals(battle.map, "mapa")
        self.assertEquals(battle.duration, 100)
        self.assertEquals(battle.mvp, Player.objects.get(tag="#00000002"))

    def test_get_player_only_battle(self):
        playerBattle = PlayerOnlyBattle.objects.get(id=1)

        self.assertEquals(playerBattle.onlyBattle, OnlyBattle.objects.get(id=1))
        self.assertEquals(playerBattle.player, Player.objects.get(tag="#00000001"))
        self.assertEquals(playerBattle.rank, 1)
        self.assertEquals(playerBattle.brawler, "NITA")

    def test_get_player_group_battle(self):
        playerBattle = PlayerGroupBattle.objects.get(id=1)

        self.assertEquals(playerBattle.groupBattle, GroupBattle.objects.get(id=1))
        self.assertEquals(playerBattle.player, Player.objects.get(tag="#00000002"))
        self.assertEquals(playerBattle.result, "victory")
        self.assertEquals(playerBattle.brawler, "SHELLY")
        self.assertEquals(playerBattle.starPlayer, True)

    def test_login(self):
        login = self.client.login(username='test', password='testpasswd')
        self.assertEquals(login, True)