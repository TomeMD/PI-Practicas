import io
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
import requests
import random
import pendulum
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import base64
from .models import *
from .forms import YTForm, LoginForm, SignupForm
from .conf import *

ytToken='<paste-yt-token>'

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    return render(request, 'brawlstarsapp/signupError.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(request.GET['next'])

# Página inicial
def index(request):
    loginError=""
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            loginError="Error de login"
    
    loginForm = LoginForm()
    signupForm=SignupForm()
    if request.user.is_authenticated:
        context={'user':request.user,'login_form':loginForm,'signup_form':signupForm,'loginError':loginError}
    else:
        context={'login_form':loginForm,'signup_form':signupForm,'loginError':loginError}
    return render(request, 'brawlstarsapp/index.html', context)

# Ranking global de mejores jugadores
def players(request):
    try:
        playersInfo = requests.get('https://api.brawlstars.com/v1/rankings/global/players', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
        if playersInfo.status_code == 200:
            context = {
                'playersInfo' : playersInfo.json()['items']
            }
        else:
            context = {
                'errMsg' : "Global player ranking unavailable, can't connect to the Brawl Stars API."
            }
    except requests.exceptions.ConnectionError as e:
        playersInfo = []
        for player in Player.objects.all():
            playersInfo.append(player)
        context = {
            'warnMsg': "Can't connect to the Brawl Stars API, showing players from the local database.",
            'playersInfo': playersInfo
        }

    return render(request, 'brawlstarsapp/players.html', context)

# Ranking global de mejores clubes
def clubs(request):
    try:
        clubsInfo = requests.get('https://api.brawlstars.com/v1/rankings/global/clubs', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
        if clubsInfo.status_code == 200:
            context = {
                'clubsInfo' : clubsInfo.json()['items']
            }
        else:
            context = {
                'errMsg' : "Global clubs ranking unavailable, can't connect to the Brawl Stars API."
            }
    except requests.exceptions.ConnectionError as e:
        clubsInfo = []
        for club in Club.objects.all():
            clubsInfo.append(club)
        context = {
            'warnMsg': "Can't connect to the Brawl Stars API, showing clubs from the local database.",
            'clubsInfo': clubsInfo
        }
    return render(request, 'brawlstarsapp/clubs.html', context)

def getPlayer(tag):
    try:
        player = Player.objects.get(tag = tag)
    except Player.DoesNotExist:
        playerInfo = requests.get('https://api.brawlstars.com/v1/players/' + '%23' + tag.replace('#',''), \
            headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'}).json()
        if not playerInfo.get("club"):
            club = None
        else:
            club = getClub(playerInfo.get("club").get("tag"))
        player = Player(tag = playerInfo['tag'], name = playerInfo['name'], trophies = playerInfo['trophies'], \
        soloVictories = playerInfo['soloVictories'], duoVictories = playerInfo['duoVictories'], \
        trioVictories = playerInfo['3vs3Victories'], club = club)
        player.save()

    return player

def getClub(tag):
    if tag is None:
        return None
    try:
        club = Club.objects.get(tag = tag)
    except Club.DoesNotExist:
        clubInfo = requests.get('https://api.brawlstars.com/v1/clubs/' + '%23' + tag.replace('#',''), \
            headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'}).json()
        club = Club(tag = clubInfo['tag'], name = clubInfo['name'], desc = clubInfo.get('description'), \
            type = clubInfo['type'], reqTrophies = clubInfo['requiredTrophies'], trophies = clubInfo['trophies'])
        club.save()

    return club

def search_brawler(battle, player, group):
    brawler = None
    if group == True:
        for team in battle['battle']['teams']:
            for _player in team:
                if _player['tag'] == player.tag:
                    brawler = _player['brawler']['name']
    else:
        rank = battle["battle"]["rank"]
        brawler = battle["battle"]["players"][rank-1]["brawler"]["name"]    
    return brawler

def build_groupBattle(battle_json, player):

    event_id = battle_json["event"]["id"]
    dt = pendulum.parse(battle_json["battleTime"], tz='Europe/Madrid')

    try:
        battle = GroupBattle.objects.get(eventId=event_id, dateTime=dt)
    except GroupBattle.DoesNotExist:
        if battle_json["battle"]["starPlayer"] == None:
            mvp = None
        else:
            mvp = getPlayer(battle_json["battle"]["starPlayer"]["tag"])
        battle = GroupBattle(eventId=event_id, dateTime=dt, mode=battle_json["battle"]["mode"], map=battle_json["event"]["map"], type=battle_json["battle"]["type"], duration=battle_json["battle"]["duration"],
        mvp=mvp)
        battle.save()
    if PlayerGroupBattle.objects.filter(groupBattle=battle, player=player).exists() == False:
        brawler = search_brawler(battle_json, player, group=True)
        if battle_json["battle"]["starPlayer"] == None:
            PlayerGroupBattle.objects.create(groupBattle = battle, player = player, result = battle_json["battle"]["result"], brawler = brawler, starPlayer = False)
        else:
            PlayerGroupBattle.objects.create(groupBattle = battle, player = player, result = battle_json["battle"]["result"], brawler = brawler, starPlayer = (battle_json["battle"]["starPlayer"]["tag"] == player.tag))
        

    return battle

def build_onlyBattle(battle_json, player):

    event_id = battle_json["event"]["id"]
    dt = pendulum.parse(battle_json["battleTime"], tz='Europe/Madrid')

    try:
        battle = OnlyBattle.objects.get(eventId=event_id, dateTime=dt)
    except OnlyBattle.DoesNotExist:
        battle = OnlyBattle(eventId=event_id, dateTime=dt, mode=battle_json["battle"]["mode"], map=battle_json["event"]["map"], type=battle_json["battle"]["type"])
        battle.save()
    if PlayerOnlyBattle.objects.filter(onlyBattle=battle, player=player).exists() == False:
        brawler = search_brawler(battle_json, player, group=False)
        PlayerOnlyBattle.objects.create(onlyBattle = battle, player = player, rank = battle_json["battle"]["rank"], brawler = brawler)
    
    return battle

def build_battlelist(battlelog, player):
    battlelist = []
    for battle in battlelog:
        if battle["battle"]["mode"] in ["soloShowdown", "loneStar"]:
            battleObj = build_onlyBattle(battle, player)
            battlelist.append(battleObj)
        elif battle["battle"]["mode"] in ["bigGame",  "duoShowdown", "bossFight"]:
            pass # Modos no implementados
        else:
            battleObj = build_groupBattle(battle, player)
            battlelist.append(battleObj)    
    return battlelist   

def pick_win_rates(brawlers):
    pickRates = []
    winRates = []
    df = pd.DataFrame(brawlers, columns= ['name', 'result'])
    total = df.count()['name']
    for name in df['name'].unique().tolist():
        brawlerDf = df[df['name'] == name]
        battles = brawlerDf.count()['name']
        wins = (brawlerDf['result'] == 'victory').sum()
        winRates.append({'name': name, 'winrate': "{0:.2f}".format(wins/battles * 100)})
        pickRates.append({'name': name, 'pickrate': "{0:.2f}".format(battles/total * 100)})
    return pickRates, winRates      

def count_star_plays(starPlays):
    df = pd.DataFrame(starPlays, columns= ['name', 'starPlayer'])
    count = (df['starPlayer'] == True).sum()
    return (count, "{0:.2f}".format(count/df.count()['starPlayer'] * 100))

def search_brawlers_results(player):
    brawlers = []
    starPlaysList = []
    groupBattles = PlayerGroupBattle.objects.filter(player = player)
    for battle in groupBattles:
        brawlers.append({'name' : battle.brawler, 'result': battle.result})
        starPlaysList.append({'name' : battle.brawler, 'starPlayer': battle.starPlayer})
    onlyBattles = PlayerOnlyBattle.objects.filter(player = player)
    for battle in onlyBattles:
        if battle.rank <= 4: result = 'victory'
        else: result = 'defeat'
        brawlers.append({'name' : battle.brawler, 'result': result})
    return (brawlers, starPlaysList)

def createPlot(pickRates, winRates):
    for pick in pickRates:
        tmp = {'name': pick['name'], 'pickrate': float(pick['pickrate'])}
        pick.update(tmp)
    for win in winRates:
        tmp = {'name': win['name'], 'winrate': float(win['winrate'])}
        win.update(tmp)

    picks = pd.DataFrame(pickRates, columns=['name', 'pickrate'], index=(list(pick.values())[0] for pick in pickRates))
    wins = pd.DataFrame(winRates, columns=['name', 'winrate'], index=(list(pick.values())[0] for pick in winRates))
    picksFig = picks.plot.pie(y='pickrate', figsize=(4, 4), autopct='%1.1f%%', legend=False).get_figure()
    winsFig = wins.plot.bar(x='name', y='winrate', figsize=(4, 4), legend=False).get_figure()
    winsFig.tight_layout()
    picksFig.tight_layout()
    #encode base64 picksFig
    buf = io.BytesIO()
    picksFig.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    b2 = base64.b64encode(buffer)
    picksFig=b2.decode('utf-8')
    #encode base64 winsFig
    buf = io.BytesIO()
    winsFig.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    b2 = base64.b64encode(buffer)
    winsFig=b2.decode('utf-8')
    return picksFig, winsFig

def playerTag(request, player_id):
    player_id= player_id.replace("#","")
    
    try:
        playerInfo = requests.get('https://api.brawlstars.com/v1/players/' + '%23' + player_id, headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
    
        if playerInfo.status_code == 200:
            battlelog = requests.get('https://api.brawlstars.com/v1/players/' + '%23' + player_id + '/battlelog', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
            battlelog = battlelog.json()['items']
            playerInfo = playerInfo.json()
            stats = request.GET.get('stats', '')
            club = getClub(playerInfo.get("club").get("tag"))
            
            player = Player(tag = playerInfo['tag'], name = playerInfo['name'], trophies = playerInfo['trophies'], \
                soloVictories = playerInfo['soloVictories'], duoVictories = playerInfo['duoVictories'], \
                trioVictories = playerInfo['3vs3Victories'], club = club)
            player.save()

            battlelist = build_battlelist(battlelog, player)
            winRates = None
            pickRates = None
            starPlayerBattles = None
            starPlayerRate = None  
            picksFig = None
            winsFig = None 
            if stats == 'yes':
                brawlers, starPlaysList = search_brawlers_results(player)
                starPlayerBattles, starPlayerRate = count_star_plays(starPlaysList)
                pickRates, winRates = pick_win_rates(brawlers)
                picksFig, winsFig = createPlot(pickRates, winRates)
            else:
                stats = None
            context = {
                'playerInfo' : playerInfo,
                'battlelog' : battlelist,
                'winRates': winRates,
                'pickRates': pickRates,
                'starPlayerBattles': starPlayerBattles,
                'starPlayerRate': starPlayerRate,
                'stats': stats,
                'picksFig': picksFig,
                'winsFig': winsFig
            }

        elif playerInfo.status_code == 404:
            context = {
                'errMsg': "Error: no Brawl Stars player with tag #%s" % player_id 
            }
    except requests.exceptions.ConnectionError as e:
        try:
            player = Player.objects.get(tag="#"+player_id)
            playerInfo = model_to_dict(player)
            battlelist = []
            stats = request.GET.get('stats', '')
            for battle in PlayerOnlyBattle.objects.filter(player=player):
                battlelist.append(battle.onlyBattle)
            for battle in PlayerGroupBattle.objects.filter(player=player):
                battlelist.append(battle.groupBattle)

            battlelist.sort(key=lambda x: x.dateTime, reverse=True)
            winRates = None
            pickRates = None
            starPlayerBattles = None
            starPlayerRate = None  
            picksFig = None
            winsFig = None 
            if stats == 'yes':
                brawlers, starPlaysList = search_brawlers_results(player)
                starPlayerBattles, starPlayerRate = count_star_plays(starPlaysList)
                pickRates, winRates = pick_win_rates(brawlers)
                picksFig, winsFig = createPlot(pickRates, winRates)
            context = {
                'playerInfo': playerInfo,
                'battlelog' : battlelist,
                'winRates': winRates,
                'pickRates': pickRates,
                'starPlayerBattles': starPlayerBattles,
                'starPlayerRate': starPlayerRate,
                'stats': stats,
                'picksFig': picksFig,
                'winsFig': winsFig,
                'errMsg': "Can't connect to the Brawl Stars API, showing the most recent information from the local database."
            }
        except Player.DoesNotExist:
            context = {
                'errMsg': "Error: No player with tag #%s in the local database." % player_id 
            }          
    return render(request, 'brawlstarsapp/playerTag.html', context)


def clubTag(request, club_tag):
    try:
        club_tag = club_tag.replace("#","")
        clubInfo = requests.get('https://api.brawlstars.com/v1/clubs/' + '%23' + club_tag, headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
        if clubInfo.status_code == 200:
            members = requests.get('https://api.brawlstars.com/v1/clubs/' + '%23' + club_tag + '/members', headers={'authorization': 'Bearer %s' % brawlToken, 'Accept': 'application/json'})
            clubInfo = clubInfo.json()
            club = Club(tag = clubInfo['tag'], name = clubInfo['name'], desc = clubInfo.get('description'), \
                type = clubInfo['type'], reqTrophies = clubInfo['requiredTrophies'], \
                trophies = clubInfo['trophies'])
        
            club.save()
            context = {
                'clubInfo' : club,
                'members' : members.json()['items']
            }
        elif clubInfo.status_code == 404:
            context = {
                'errMsg': "Error: Brawl Stars club with tag #%s" % club_tag 
            }
    except requests.exceptions.ConnectionError as e:
        try:
            club = Club.objects.get(tag="#"+club_tag)
            clubInfo = model_to_dict(club)
            context = {
                'clubInfo' : clubInfo,
                'errMsg': "Can't connect to the Brawl Stars API, showing the most recent information from the local database."
            }
        except Club.DoesNotExist:
            context = {
                'errMsg': "Error: No club with tag #%s in the local database." % club_tag 
            } 

    return render(request, 'brawlstarsapp/clubTag.html', context)

def youtube(request):

    ytform = YTForm()
    if request.method == 'POST':
        SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
        query = request.POST['name'] + 'brawl stars'
        data = {
            'part': 'snippet',
            'q': query,
            'key': ytToken,
            'maxResults': 20
        }
        try:
            r = requests.get(SEARCH_URL, params=data)
            response_json = r.json()
            x=random.randint(0, 19) # Muestro un vídeo aleatorio de los 20 devueltos
            id = response_json['items'][x]['id']['videoId']
            video = 'https://www.youtube.com/embed/' + str(id)
            return render(request, 'brawlstarsapp/forms.html', {'ytform': ytform, 'video': video})
        except:
            return render(request, 'brawlstarsapp/forms.html', {'ytform': ytform, 'error': 'No related videos found'})
     # Si se hace un GET mostramos el formulario vacío           
    return render(request, 'brawlstarsapp/forms.html', {'ytform': ytform})