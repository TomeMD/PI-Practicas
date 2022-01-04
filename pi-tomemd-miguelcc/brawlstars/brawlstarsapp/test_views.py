import json
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
import requests
from .views import getClub, build_battlelist, search_brawlers_results, pick_win_rates

brawlToken= '<paste-your-token>'


class ViewsTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username="test", password="testpasswd")

    def test_get_player_from_api(self):
        try:
            playerInfo = requests.get('https://api.brawlstars.com/v1/players/%239P2JLPCR', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'}).json()
            club = getClub(playerInfo.get("club").get("tag"))
            player = Player(tag = playerInfo['tag'], name = playerInfo['name'], trophies = playerInfo['trophies'], \
                soloVictories = playerInfo['soloVictories'], duoVictories = playerInfo['duoVictories'], \
                trioVictories = playerInfo['3vs3Victories'], club = club)
            player.save()

            self.assertEquals(player, Player.objects.get(tag="#9P2JLPCR"))

        except requests.exceptions.ConnectionError:
            pass

    def test_get_club_from_api(self):
        try:
            clubInfo = requests.get('https://api.brawlstars.com/v1/clubs/%232QGPUJV82', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'}).json()
            club = Club(tag = clubInfo['tag'], name = clubInfo['name'], desc = clubInfo.get('description'), \
                type = clubInfo['type'], reqTrophies = clubInfo['requiredTrophies'], \
                trophies = clubInfo['trophies'])
            club.save()

            self.assertEquals(club, Club.objects.get(tag="#2QGPUJV82"))

        except requests.exceptions.ConnectionError:
            pass

    
    def test_pick_win_rates(self):
        battleLog = '''[{
            "battleTime": "20210612T181302.000Z",
            "event": {
                "id": 15000025,
                "mode": "brawlBall",
                "map": "Triple Dribble"
            },
            "battle": {
                "mode": "brawlBall",
                "type": "challenge",
                "result": "victory",
                "duration": 60,
                "trophyChange": 1,
                "starPlayer": {
                    "tag": "#98Q9UQJ9G",
                    "name": "torchy",
                    "brawler": {
                        "id": 16000009,
                        "name": "DYNAMIKE",
                        "power": 10,
                        "trophies": 800
                    }
                },
            "teams": [
            [
                {
                "tag": "#28U8V0YCQ",
                "name": "P_R0V_3N",
                "brawler": {
                    "id": 16000004,
                    "name": "RICO",
                    "power": 10,
                    "trophies": 802
                }
                },
                {
                "tag": "#8PPCY08RC",
                "name": "nathan112207",
                "brawler": {
                    "id": 16000045,
                    "name": "STU",
                    "power": 10,
                    "trophies": 802
                }
                },
                {
                "tag": "#2YQRLLP9G",
                "name": "Killer",
                "brawler": {
                    "id": 16000009,
                    "name": "DYNAMIKE",
                    "power": 10,
                    "trophies": 803
                }
                }
            ],
            [
                {
                "tag": "#282CUJ99",
                "name": "❄️MrPears❄️",
                "brawler": {
                    "id": 16000004,
                    "name": "RICO",
                    "power": 10,
                    "trophies": 800
                }
                },
                {
                "tag": "#98Q9UQJ9G",
                "name": "torchy",
                "brawler": {
                    "id": 16000009,
                    "name": "DYNAMIKE",
                    "power": 10,
                    "trophies": 800
                }
                },
                {
                "tag": "#2PR2QRCC",
                "name": "Tribe | Raz",
                "brawler": {
                    "id": 16000006,
                    "name": "BARLEY",
                    "power": 10,
                    "trophies": 800
                }
                }
            ]
            ]
            }},{
            "battleTime": "20210612T181147.000Z",
            "event": {
                "id": 15000025,
                "mode": "brawlBall",
                "map": "Triple Dribble"
            },
            "battle": {
                "mode": "brawlBall",
                "type": "challenge",
                "result": "victory",
                "duration": 58,
                "trophyChange": 1,
                "starPlayer": {
                "tag": "#282CUJ99",
                "name": "❄️MrPears❄️",
                "brawler": {
                    "id": 16000004,
                    "name": "RICO",
                    "power": 10,
                    "trophies": 700
                }
                },
                "teams": [
                [
                    {
                    "tag": "#V28V9ULJ",
                    "name": "fizzicist",
                    "brawler": {
                        "id": 16000026,
                        "name": "BIBI",
                        "power": 10,
                        "trophies": 702
                    }
                    },
                    {
                    "tag": "#8GRYJ9LQ",
                    "name": "Dan",
                    "brawler": {
                        "id": 16000032,
                        "name": "MAX",
                        "power": 10,
                        "trophies": 702
                    }
                    },
                    {
                    "tag": "#JP0UJVC",
                    "name": "PlSSANDSHlT",
                    "brawler": {
                        "id": 16000028,
                        "name": "SANDY",
                        "power": 10,
                        "trophies": 703
                    }
                    }
                ],
                [
                    {
                    "tag": "#282CUJ99",
                    "name": "❄️MrPears❄️",
                    "brawler": {
                        "id": 16000004,
                        "name": "RICO",
                        "power": 10,
                        "trophies": 700
                    }
                    },
                    {
                    "tag": "#98Q9UQJ9G",
                    "name": "torchy",
                    "brawler": {
                        "id": 16000009,
                        "name": "DYNAMIKE",
                        "power": 10,
                        "trophies": 700
                    }
                    },
                    {
                    "tag": "#2PR2QRCC",
                    "name": "Tribe | Raz",
                    "brawler": {
                        "id": 16000006,
                        "name": "BARLEY",
                        "power": 10,
                        "trophies": 700
                    }
                    }
                ]
                ]
            }
            }]
            '''
        
        battleLog = json.loads(battleLog)
        player = Player.objects.create(tag = "#2PR2QRCC", name = "nombre jugador", trophies = 5000, soloVictories = 50, duoVictories = 100, trioVictories = 150, club = None)

        build_battlelist(battleLog, player)
        brawlers, starPlaysList = search_brawlers_results(player)
        pickRates, winRates = pick_win_rates(brawlers)
        self.assertEquals([{'name': "BARLEY", "pickrate": "100.00"}], pickRates)
        self.assertEquals([{'name': "BARLEY", "winrate": "100.00"}], winRates)

    @unittest.expectedFailure
    def test_login_error(self):
        login = self.client.login(username='test', password ='1234')
        self.assertEquals(login, True)
    
    @unittest.expectedFailure
    def test_player(self):
        Player.objects.get(tag="0")