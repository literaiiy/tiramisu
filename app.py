
# ! Importing
from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory
import json
from mojang import MojangAPI
from wtforms import TextField
from datetime import datetime
import requests
import math
import time
import re
import os
import logging
import copy
from flask_talisman import Talisman
# from flask_sslify import SSLify
#import httpx
#from itertools import cycle, islice
#from num2words import num2words
import requests_cache
#from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
#from livereload import Server
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ! Initialization & Constants
app = Flask(__name__)
Talisman(app)
# app._static_folder = '/build'
# if 'DYNO' in os.environ: # only trigger SSLify if the app is running on Heroku
#     sslify = SSLify(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

app.secret_key = 'a34w7tfyner9ryhzrbfw7ynhhcdtg78as34'
HAPIKEY = '1e5f6a57-6327-4888-886a-590c39861a6a'
HAPIKEY2 = '645eb55b-1550-400e-a5a3-31a2cfe0a806'
# ADMINS = ['35a178c0c37043aea959983223c04de0']
# FLOWERS = ['27bcc1547423484683fd811155d8c472']
# SPARKLES = ['903100946468408aaf2462365389059c', '35bb69ce904a4380a03ffd55acbc2331']
# PENGUINS = ['cfc42e543d834b4f9f7a23c059783ba5']
swearList = [
    'anal','anus','bastard','bitch','blowjob','buttplug','clitoris','cock','cunt','dick','dildo','fag','fuck','jizz','kkk','nigger','nigga','penis','piss','pussy','scrotum','sex','shit','slut','vagina']
sweetHeadsRanks = ['HELPER', 'MOD', 'ADMIN', 'OWNER']

# Translate list for rank colors
rankColorList = {
    '0':'blank',
    '1':'dark_blue',
    '2':'dark_green',
    '3':'dark_aqua',
    '4':'dark_red',
    '5':'dark_purple',
    '6':'gold',
    '7':'gray',
    '8':'dark_gray',
    '9':'blue',
    'a':'green',
    'b':'aqua',
    'c':'red',
    'd':'light_purple',
    'e':'yellow',
    'f':'white'}
dumbassHypixelRanks = {
    'VIP':['green','gold'],
    'HELPER':['blue',''],
    'MOD':['dark_green',''],
    'ADMIN':['red',''],
    'OWNER':['red',''],
    'SLOTH':['red',''],
    'MCP':['red',''],
    'MOJANG':['gold',''],
    'EVENTS':['gold','']
}

# Player's username & uuid initialization
username = ''
uuid = ''

config = {
    "DEBUG": True,          # some Flask specific configs
    'CACHE_TYPE': 'filesystem', # Flask-Caching related configs
     'CACHE_DIR': '/tmp',  # Flask-Caching directory
    "CACHE_DEFAULT_TIMEOUT": 15
}

# some config stuff
app.config.from_mapping(config)
cache = Cache(app)
logging.basicConfig(level=logging.DEBUG)
requests_cache.install_cache('req_cache', backend='sqlite', expire_after=10)

# reqses
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
reqses = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 429, 500, 502, 503, 504 ])
reqses.mount('http://', HTTPAdapter(max_retries=retries))

# class searchBar():
#     query = TextField("Search...")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ! Routing for homepage
@app.route('/', methods=['POST', 'GET'], defaults={'path':''})
def queryt(path):
    
    gameDict = []
    try:
        hs = reqses.get('https://api.hypixel.net/gameCounts?key=' + HAPIKEY2)
    except:
        return render_template('index.html', gameDict={}, totalPlayers=-1)
    hsjaysonn = hs.json()
    gameCount = hsjaysonn['games']
    gameList = [
        #('Total Players', hsjaysonn['playerCount']),
        ('SkyWars 🏹', 'SKYWARS'),
        ('SkyBlock 🌎', 'SKYBLOCK'),
        ('BedWars 🛌', 'BEDWARS'),
        ('Duels ⚔️', 'DUELS'),
        ('Super Smash Mobs 🦸', 'SUPER_SMASH'),
        ('Speed UHC 💨', 'SPEED_UHC'),
        ('Cops and Crims 🔫', 'MCGO'),
        ('The Pit 🕳️', 'PIT'),
        ('UHC Champions 🍎', 'UHC'),
        ('Build Battle 🛠️', 'BUILD_BATTLE'),
        ('Murder Mystery 🕵️‍♂️', 'MURDER_MYSTERY'),
        ('Warlords 🏇', 'BATTLEGROUND'),
        ('Housing 🏠', 'HOUSING'),
        ('Arcade 🕹️', 'ARCADE'),
        ('Blitz SG 🗡️', 'SURVIVAL_GAMES'),
        ('Mega Walls 🧱', 'WALLS3'),
        ('Prototype 🏗️', 'PROTOTYPE'),
        ('TNT Games 💣', 'TNTGAMES'),
        ('Main Lobby', 'MAIN_LOBBY'),
        ('Watching a replay', 'REPLAY'),
        ('In limbo', 'LIMBO'),
        ('Idle', 'IDLE'),]

    arcadeGameList = [
        ('Party Games 🎉', 'PARTY'),
        # ('🧟 Zombies - Dead End', gameCount['ARCADE']['modes']['ZOMBIES_DEAD_END'] + gameCount['ARCADE']['modes']['ZOMBIES_ALIEN_ARCADIUM'] + gameCount['ARCADE']['modes']['ZOMBIES_BAD_BLOOD']),
        # ('🙈 Hide and Seek', gameCount['ARCADE']['modes']['HIDE_AND_SEEK_PROP_HUNT'] + gameCount.get('ARCADE',{}).get('modes',{}).get('HIDE_AND_SEEK_PARTY_POOPER',{})),
        ('Mini Walls 🛩️', 'MINI_WALLS'),
        ('Hypixel Says 📢', 'SIMON_SAYS'),
        ('Capture the Wool 🏁', 'PVP_CTW'),
        ('Zombies - Dead End 🧟‍♂️' , 'ZOMBIES_DEAD_END'),
        ('Farm Hunt 🐖', 'FARM_HUNT')]

    gameDict = []
    totalPlayers = hsjaysonn['playerCount']
    for item in gameList:
        try:
            #if item[0] == 'Total Players': gameDict.append({'game':'Total Players','playerCount':hsjaysonn['playerCount']})
            #else:
            gameDict.append({'game':item[0],'playerCount':gameCount[item[1]]['players']})
        except:
            gameDict.append({'game':item[0],'playerCount':0,})
    
    for item in arcadeGameList:
        try:
            gameDict.append({'game':item[0],'playerCount':gameCount['ARCADE']['modes'][item[1]]})
        except:
            gameDict.append({'game':item[0],'playerCount':0,})

    gameDict = sorted(gameDict, reverse=True, key=lambda k: k['playerCount'])
    for enum, game in enumerate(gameDict, 1):
        game['pos'] = enum
    # form = searchBar()
    if request.method == 'POST':
        session['req'] = request.form
        if not session['req']['content'] == '':
            return redirect(url_for('compute', q=str(session['req']['content'])))
    return render_template('index.html', gameDict=gameDict, totalPlayers=totalPlayers)

# ! Redirect /<k> to /p/<k>
@app.route('/<k>', methods=['POST', 'GET'])
def reddorect(k):
    return redirect(url_for('compute', q=k))

# ! Privacy Policy
@app.route('/privacy')
#@cache.cached(timeout=0)
def privacy():
    return render_template('privacy.html')

# ! Sitemap
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

# ! Filters
# Thousands separator no decimals
@app.template_filter()
def those(n):
    try:
        return f'{int(n):,}'
    except: return n

# Thousands separator raw
@app.template_filter()
def thraw(n):
    return f'{n:,}'

# Floor number
@app.template_filter()
def floor(n):
    return math.floor(n)

# Split
@app.template_filter()
def split(l):
    return l.split()


# ! Routing for search page
@app.route('/p/<q>', methods=['POST','GET'])
@cache.cached(timeout=15)
def compute(q):
    q = q.strip()
    start_time = time.time()
    if len(q) == 32 or len(q) == 36:
        q = q.replace('-','')
        try:
            if q == MojangAPI.get_uuid(MojangAPI.get_username(q)):
                username = MojangAPI.get_username(q)
                uuid = q
            else:
                return render_template('user404.html', q=q, screwup="That UUID doesn't exist. Try again with a different UUID.", noAutocorrect=True )
        except:
            return render_template('user404.html', q=q, screwup="That UUID doesn't exist. Try again with a different UUID.", noAutocorrect=True)

    else:
        uuid = MojangAPI.get_uuid(q)
        username = MojangAPI.get_username(MojangAPI.get_uuid(q))
        #else:
        #    return "false uuid or username or smthing"
    print(uuid)
    if isinstance(uuid, str):
        username = MojangAPI.get_username(uuid)

# ! Retrieve from API and initialize
        print('right before requeas ',(time.time() - start_time), ' sec')
        try:
            r = reqses.get('https://api.hypixel.net/player?key=' + HAPIKEY + '&uuid=' + uuid)
        except: return render_template('404.html', error=500, text='API timeout', desc='The Hypixel API timed out.'), 500
        print('RIGHT AFTER REQAPI is being gotten. ',(time.time() - start_time), ' sec')
        reqAPI = r.json()
        print('json deserialized ',(time.time() - start_time), ' sec')
        try:
            karma = reqAPI['player'].get('karma',0)
        except: karma = 0

        # reqList = {}
        # try:
        #     reqListKarma = reqAPI['player']['karma']
        # except:
        #     reqListKarma = 0
        # reqList['karma']=int(reqListKarma)
        # try:
        #     hypixelUN = reqAPI['player']['displayname']
        # except:
        #     hypixelUN = username
        print('reqAPI is done. ',round(time.time() - start_time, 4), ' sec')

# ! Name history
        namehis = MojangAPI.get_name_history(uuid)
        namehispure = copy.deepcopy(namehis)
        
        nhutminus1 = 0
        nhutChangedToAt = 0
        nhutindex = 0
        nhut2unix = 0

        # Takes in seconds, returns list of Y, D, H, M, S
        def sec2format(namehisDiff):
            nhutdate[0] = math.floor(namehisDiff / 31536000)
            nhutdate[1] = math.floor(namehisDiff / 86400) - nhutdate[0] * 365
            nhutdate[2] = math.floor(namehisDiff / 3600) - nhutdate[1] * 24 - nhutdate[0] * 365 * 24
            nhutdate[3] = math.floor(namehisDiff / 60) -nhutdate[2] * 60 - nhutdate[1] * 24 * 60 - nhutdate[0] * 365 * 24 * 60
            nhutdate[4] = int(namehisDiff % 60)
            return [nhutdate[0],nhutdate[1],nhutdate[2],nhutdate[3],nhutdate[4]]
        
        # Takes in list of Y, D, H, M, S and formats it into a readable string
        def sec2format2ydhms(sec2formatted):
            if sec2formatted[0] > 0:
                return str(sec2formatted[0]) + 'y ' + str(sec2formatted[1]) + 'd ' + str(sec2formatted[2]) + 'h ' + str(sec2formatted[3]) + 'm ' + str(sec2formatted[4]) + 's'
            elif sec2formatted[0] == 0 and sec2formatted[1] == 0 and sec2formatted[2] == 0 and sec2formatted[3] == 0:
                return str(sec2formatted[4]) + 's'
            elif sec2formatted[0] == 0 and sec2formatted[1] == 0 and sec2formatted[2] == 0:
                return str(sec2formatted[3]) + 'm ' + str(sec2formatted[4]) + 's'
            elif sec2formatted[0] == 0 and sec2formatted[1] == 0:
                return str(sec2formatted[2]) + 'h ' + str(sec2formatted[3]) + 'm ' + str(sec2formatted[4]) + 's'
            elif sec2formatted[0] == 0:
                return str(sec2formatted[1]) + 'd ' + str(sec2formatted[2]) + 'h ' + str(sec2formatted[3]) + 'm ' + str(sec2formatted[4]) + 's'

        # If the person has played on Hypixel, the last column's changed_to_at should be their first login
        try:
            namehis[0]['changed_to_at'] = reqAPI['player']['firstLogin']
        except:
            namehis[0]['changed_to_at'] = ''

        # Iterate through dict to add changed_to_at & time_between columns
        nhutdate = [0,0,0,0,0]
        for namehisUnixTime in namehis:
            try:
                nhutChangedToAt = namehisUnixTime['changed_to_at']
                namehisUnixTime['changed_to_at'] = datetime.fromtimestamp(nhutChangedToAt/1000).strftime('%b %d, %Y @ %I:%M:%S %p')
                namehisDiff = (nhutChangedToAt - nhutminus1)/1000
                namehisUnixTime['time_between'] = sec2format2ydhms(sec2format(namehisDiff))
                nhutminus1 = nhutChangedToAt
                nhutindex += 1

                # This fixes it somehow
                if nhutindex == len(namehis):
                    nhut2unix = nhutChangedToAt

            except:
                pass

        # Gives time_between list
            

        # Shifts position of time_changed one over
        dhmclist = []
        try:
            for xd in namehis:
                dhmclist.append(xd['time_between'])
            del dhmclist[0]
            dhmclist.append(0)
            ranger = 0
            for xe in namehis:
                xe['time_between'] = dhmclist[ranger]
                ranger += 1
        except:
            pass
        namehis[0]['time_between'] = ''

        # Switches position of columns so that it goes #, Name, Time changed, Duration had
        value = 1
        for i in namehis:
            i['num'] = value
            value += 1
            i['name'] = i.pop('name')
            i['changed_to_at'] = i.pop('changed_to_at')
            i['time_between'] = i.pop('time_between')
        namehis[0]['changed_to_at'] = ''
        namehisrev = namehis.reverse()

        print('Name history is done. ',round(time.time() - start_time, 4), ' sec')

# ! Rank

        def getRank(reqapiplayer):
            if reqapiplayer:
                # prefix - for special guys with PIG+++/SLOTH and whatever
                if 'prefix' in reqapiplayer:
                    x = reqapiplayer['prefix']
                    rankParsed = re.sub('[a-z§0-9+\[\]]','',x)
                    rankPlusses = x.count('+')*'+'
                    rankTotal = re.sub('[A-Z§+\[\]]','',x)
                    rankParsedColor = rankColorList[rankTotal[0]]
                    rankPlussesColor = rankColorList.get(rankTotal.replace(rankTotal[0],''), 'red')
                    return (rankParsed, rankPlusses, rankParsedColor, rankPlussesColor)

                # rank - for staff and youtube
                if 'rank' in reqapiplayer:
                    x = reqapiplayer['rank']
                    if 'YOUTUBE' in x: return ('YOUTUBE', '', 'red', 'lightgray')
                    elif 'HELPER' in x: return ('HELPER', '', 'blue', 'blue')
                    elif 'MOD' in x: return ('MOD', '', 'dark_green', 'dark_green')
                    elif 'ADMIN' in x: return ('ADMIN', '', 'red', 'red')

                # monthlyPackageRank - for mvp++
                if 'monthlyPackageRank' in reqapiplayer:
                    if reqapiplayer['monthlyPackageRank'] == 'SUPERSTAR':
                        return ('MVP', '++', reqapiplayer.get('monthlyRankColor', 'gold').lower(), reqapiplayer.get('rankPlusColor', 'red').lower())

                #packageRank - pre EULA MVP/VIP/+/+
                if 'packageRank' in reqapiplayer:
                    x = reqapiplayer['packageRank']
                    try:
                        if x == 'MVP_PLUS': return ('MVP', '+', 'aqua', reqapiplayer.get('rankPlusColor', 'red').lower())
                    except: pass
                    if x == 'MVP': return ('MVP', '', 'aqua', '')
                    elif x == 'VIP_PLUS': return ('VIP', '+', 'green', 'gold')
                    elif x == 'VIP': return ('VIP', '', 'green', '')

                # newPackageRank - post EULA MVP/VIP/+/+
                if 'newPackageRank' in reqapiplayer:
                    x = reqapiplayer['newPackageRank']
                    if x == 'MVP_PLUS': return ('MVP', '+', 'aqua', reqapiplayer.get('rankPlusColor', 'red').lower())
                    if x == 'MVP': return ('MVP', '', 'aqua', '')
                    elif x == 'VIP_PLUS': return ('VIP', '+', 'green', 'gold')
                    elif x == 'VIP': return ('VIP', '', 'green', '')

            # non rank
            return False

        rankv3 = getRank(reqAPI['player'])
        print('rank is done. ',round(time.time() - start_time, 4), ' sec')

# ! Network Level, XP
        try:
            networkExp = int(reqAPI['player']['networkExp'])
        except:
            networkExp = 0
        levelRaw = (math.sqrt((2*networkExp)+30625)/50) - 2.5
        level = math.floor((math.sqrt((2*networkExp)+30625)/50) - 2.5)
        levelProgress = round(((levelRaw - level) * 100), 2)
        levelplusone = level + 1

        multiplier = ''
        if level >= 5 and level <= 9: multiplier = '(1.5×)'
        if level >= 10 and level <= 14: multiplier = '(2×)'
        if level >= 15 and level <= 19: multiplier = '(2.5×)'
        if level >= 20 and level <= 24: multiplier = '(3×)'
        if level >= 25 and level <= 29: multiplier = '(3.5×)'
        if level >= 30 and level <= 39: multiplier = '(4×)'
        if level >= 40 and level <= 49: multiplier = '(4.5×)'
        if level >= 50 and level <= 99: multiplier = '(5×)'
        if level >= 100 and level <= 124: multiplier = '(5.5×)'
        if level >= 125 and level <= 149: multiplier = '(6×)'
        if level >= 150 and level <= 199: multiplier = '(6.5×)'
        if level >= 200 and level <= 249: multiplier = '(7×)'
        if level >= 250: multiplier = '(8×)'

        print('network lvl/xp is done. ',round(time.time() - start_time, 4), ' sec')

# ! Login Times
        firstLogin = ''
        playedOnHypixel = True
        lastSession = False

        # Last login
        try:
            lastLoginUnix = int(reqAPI['player']['lastLogin']/1000)
        except:
            lastLoginUnix = 1
        lastLogin = datetime.fromtimestamp(lastLoginUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')

        # Last logout
        try:
            lastLogoutUnix = reqAPI['player']['lastLogout']/1000
        except:
            lastLogoutUnix = 1
        lastLogout = datetime.fromtimestamp(lastLogoutUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')
            
        # First login
        try:
            firstLoginUnix = int(reqAPI['player']['firstLogin']/1000)
        except:
            firstLoginUnix = 1
            playedOnHypixel = False
            #return render_template('base.html', playedOnHypixel=False)
        
        # Last session
        try:
            if lastLoginUnix < lastLogoutUnix: lastSession = sec2format2ydhms(sec2format(lastLogoutUnix-lastLoginUnix))
        except: pass
        
        # If played on Hypixel before, changes the user's 2nd time_between to between the first name change and their first log-on to Hypixel
        if playedOnHypixel:
            firstLogin = datetime.fromtimestamp(firstLoginUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')
            try:
                nhut3unix = namehispure[1]['changed_to_at']/1000 - firstLoginUnix
            except: nhut3unix = 0
            try:
                namehis[-1]['time_between'] = '>' + sec2format2ydhms(sec2format(nhut3unix))
            except: namehis[-1]['time_between'] = ''
        else:
            namehis[-1]['time_between'] = ''
        namehisDiffe = namehis[len(namehis)-2]['time_between']	

        #if firstLoginUnix > 1357027200:
        namehis[0]['time_between'] =sec2format2ydhms(sec2format(int(time.time()-namehispure[-1]['changed_to_at']/1000)))
        if len(namehis) == 1: namehis[0]['time_between'] = ''

        print('login times are done. ',round(time.time() - start_time, 4), ' sec')

# ! Quests, AP, Achievements

        try:
            achievements = len(reqAPI['player']['achievements'])+len(reqAPI['player']['achievementsOneTime'])
            achievements = format(achievements, ',')
        except:
            achievements = 0
        try:
            achpot = reqAPI['player']['achievementPoints']
        except:
            achpot = 0
        
        quests = 0
        try:
            for j in reqAPI['player']['quests']:
                try:
                    quests += len(reqAPI['player']['quests'][j]['completions'])
                except:
                    pass
        except:
            pass

        print('quests/ap/achievements is done. ',round(time.time() - start_time, 4), ' sec')

# ! Title and Seniority
        joinedAgo = 0
        joinedAgoText = ''
        seniority = ('☘', 'Newcomer', 'gray')

        # Time seniority
        try:
            joinedAgo = time.time() - firstLoginUnix
            joinedAgoText = sec2format2ydhms(sec2format(joinedAgo))
                
            if joinedAgo < 0.111*31536000: seniority = ('☘', 'Newcomer', 'gray')
            elif joinedAgo < 0.444*31536000: seniority = ('⛏', 'Rookie', 'green')
            elif joinedAgo < 1*31536000: seniority = ('➴', 'Novice', 'blue')
            elif joinedAgo < 1.778*31536000: seniority = ('⚝', 'Trainee', 'red')
            elif joinedAgo < 2.778*31536000: seniority = ('⚜', 'Expert', 'gold')
            elif joinedAgo < 4.000*31536000: seniority = ('♛', 'Master', 'master')
            elif joinedAgo < 5.444*31536000: seniority = ('❖', 'Elder', 'water')
            elif joinedAgo < 7.111*31536000: seniority = ('♗', 'Veteran', 'nebula')
            else: seniority = ('♆', 'Ancient', 'mirror')
        except: pass

        # Rank seniority
        boughtPastRank = ''
        boughtPastTime = 0
        newPackageRank = ''
        try:
            newPackageRank = reqAPI['player']['newPackageRank']
            boughtPastRank = sec2format2ydhms(sec2format(time.time() - reqAPI['player']['levelUp_' + newPackageRank]/1000))
            boughtPastTimeUnix = reqAPI['player']['levelUp_' + newPackageRank]/1000
            boughtPastTime = datetime.fromtimestamp(boughtPastTimeUnix).strftime('%b %d, %Y at %I:%M %p %z')
            #print('boughtPastTime')
        except: pass

        print('title and seniority are done. ',round(time.time() - start_time, 4), ' sec')

# ! Session Data
        def gameTranslate(game):
            try:
                if game == 'SKYWARS': return 'SkyWars'
                if game == 'SKYBLOCK': return 'SkyBlock'
                if game == 'BEDWARS': return 'BedWars'
                if game == 'SUPER_SMASH': return 'Smash Heroes'
                if game == 'SPEED_UHC': return 'Speed UHC'
                if game == 'MCGO': return 'Cops and Crims'
                if game == 'PIT': return 'The Pit'
                if game == 'UHC': return 'UHC Champions'
                if game == 'BATTLEGROUND': return 'Warlords'
                if game == 'SURVIVAL_GAMES': return 'Blitz SG'
                if game == 'WALLS3': return  'Mega Walls'
                if game == 'TNTGAMES': return  'TNT Games'
                if game == 'VAMPIREZ': return 'VampireZ'
                if game == 'ARENA': return 'Arena Brawl'
                else: return game.replace('_',' ').title()
            except: return ''
            
        currentSession = False
        sessionType = ''
        if playedOnHypixel:
            reqAPIsess = reqses.get('https://api.hypixel.net/status?key=' + HAPIKEY + '&uuid=' + uuid)
            sessionAPI = reqAPIsess.json()
            print('RIGHT AFTER HYPIXEL API SESSION DATA is being gotten. ',(time.time() - start_time), ' sec')
            try:
                if playedOnHypixel and sessionAPI['session']['online']:
                    currentSession = gameTranslate(sessionAPI['session']['gameType'])
                    try:
                        sessionType = sessionAPI['session']['mode'].replace('_',' ').title()
                    except:
                        sessionType = 'Lobby'
            except: pass

        print('session data is done. ',round(time.time() - start_time, 4), ' sec')

# ! Socials
        twitter = []
        instagram = []
        twitch = []
        discord = ''
        hypixelForums = []
        youtube = []
        try:
            socialsList = reqAPI['player']['socialMedia']['links']

            if "TWITTER" in socialsList:
                twitter = reqAPI['player']['socialMedia']['links']['TWITTER']
                if twitter[-1] == '/': twitter = twitter[:-1]
                twitter = [twitter.rsplit('/',1)[1], twitter]

            if "INSTAGRAM" in socialsList:
                instagram = reqAPI['player']['socialMedia']['links']['INSTAGRAM']
                if instagram[-1] == '/': instagram = instagram[:-1]
                instagram = [instagram.rsplit('/',1)[1], instagram]

            if "TWITCH" in socialsList:
                twitch = reqAPI['player']['socialMedia']['links']['TWITCH']
                if twitch[-1] == '/': twitch = twitch[:-1]
                twitch = [twitch.rsplit('/',1)[1], twitch]
            
            if 'DISCORD' in socialsList:
                discord = reqAPI['player']['socialMedia']['links']['DISCORD']

            if "HYPIXEL" in socialsList:
                hypixelForums = reqAPI['player']['socialMedia']['links']['HYPIXEL']
                if hypixelForums[-1] == '/': hypixelForums = hypixelForums[:-1]
                hypixelForums = [hypixelForums.rsplit('/',1)[1], hypixelForums]
                hypixelForums[0] = hypixelForums[0].rsplit('.',1)[0]
            
            if "YOUTUBE" in socialsList:
                youtube = reqAPI['player']['socialMedia']['links']['YOUTUBE']
                if youtube[-1] == '/': youtube = youtube[:-1]
                youtube = [youtube.rsplit('/',1)[1], youtube]
        except: pass

        print('social media is done. ',round(time.time() - start_time, 4), ' sec')

# ! Others

        def significantTimeDenom(list):
            if list[0] != 0: return str(list[0]) + 'y ' + str(list[1]) + 'd'
            elif list[1] != 0: return str(list[1]) + 'd ' + str(list[2]) + 'h'
            elif list[2] != 0: return str(list[2]) + 'h ' + str(list[3]) + 'm'
            elif list[3] != 0: return str(list[3]) + 'm ' + str(list[4]) + 's'
            else: return str(list[4]) + 's'

        try:
            userLanguage = reqAPI['player'].get('userLanguage', 'unspecified').title()
        except: userLanguage = 'unspecified'
        try:
            userVersion = reqAPI['player'].get('mcVersionRp') if reqAPI['player'].get('mcVersionRp') != None else 'unspecified version'
        except: userVersion = 'unspecified version'
        try:
            giftsMeta = reqAPI['player'].get('giftingMeta', {'bundlesGiven':0,'giftsGiven':0})
        except: giftsMeta = {'bundlesGiven':0,'giftsGiven':0}
        try:
            rewards = [reqAPI['player'].get('rewardStreak', 0), reqAPI['player'].get('rewardHighScore', 0), reqAPI['player'].get('totalRewards', 0), reqAPI['player'].get('totalDailyRewards', 0)]
        except: rewards = [0,0,0,0]
        try:
            lastPlayed = gameTranslate(reqAPI['player'].get('mostRecentGameType', False))
        except: lastPlayed = False

        lastSeenUnix = int(time.time()) - lastLogoutUnix
        lastSeen = significantTimeDenom(sec2format(lastSeenUnix))

        totalKillsPlaces = [
            ['Battleground', 'kills'],
            ['HungerGames', 'kills'],
            ['MCGO', 'kills'],
            ['Paintball', 'kills'],
            ['Quake', 'kills'],
            ['UHC', 'kills'],
            ['Walls', 'kills'],
            ['Walls3', 'kills'],
            ['SkyWars', 'kills'],
            ['TrueCombat', 'kills'],
            ['SuperSmash', 'kills'],
            ['SpeedUHC', 'kills'],
            ['SkyClash', 'kills'],
            ['MurderMystery', 'kills'],
            ['Duels', 'kills'],
            #['Pit', 'pit_stats_ptl', 'kills'],
            ['Bedwars', 'kills_bedwars'],
        ]
        totalCoinsPlaces = [
            ['Arcade', 'coins'],
            ['Arena', 'coins'],
            ['BuildBattle', 'coins'],
            ['Battleground', 'coins'],
            ['HungerGames', 'coins'],
            ['GingerBread', 'coins'],
            ['MCGO', 'coins'],
            ['Paintball', 'coins'],
            ['Quake', 'coins'],
            ['UHC', 'coins'],
            ['Walls', 'coins'],
            ['Walls3', 'coins'],
            ['SkyWars', 'coins'],
            ['TNTGames', 'coins'],
            ['TrueCombat', 'coins'],
            ['SuperSmash', 'coins'],
            ['SpeedUHC', 'coins'],
            ['SkyClash', 'coins'],
            ['VampireZ', 'coins'],
            ['MurderMystery', 'coins'],
            ['Duels', 'coins'],
            #['Pit', 'pit_stats_ptl', 'kills'],
            ['Bedwars', 'coins'],
        ]
        totalKills = 0
        totalWins = 0
        totalCoins = 0

        for i in totalKillsPlaces:
            try:
                totalKills += reqAPI['player']['stats'][i[0]][i[1]]
            except:
                pass
        
        try:
            for h, i in reqAPI['player']['achievements'].items():
                if 'wins' in h:
                    totalWins += i
        except: pass

        for i in totalCoinsPlaces:
            try:
                totalCoins += reqAPI['player']['stats'][i[0]][i[1]]
            except:
                pass

        print('other user stats are done. ',round(time.time() - start_time, 4), ' sec')

# ! SkyWars
        def weirdDiv(first, second, spaces=4):
            if second == 0:
                if first > 0: return math.inf
                else: return 0
            else: return round(first/second, spaces)

        try:
            swSTATSVAR = reqAPI['player']['stats']['SkyWars']
        except: swSTATSVAR = {}

        swStatsDict = {
            'success':True,
            'quits':0,
            'kills':0,
            'deaths':0,
            'assists':0,
            'wins':0,
            'losses':0,
            'survived_players':0,
            'win_streak':0,
            'souls':0,
            'heads':0,
            'coins':0,
            'blocks_broken':0,
            'blocks_placed':0,
            'egg_thrown':0,
            'arrows_shot':0,
            'arrows_hit':0,
            'enderpearls_thrown':0,
            'fastest_win':'N/A',
            'most_kills_game':0,
            'longest_bow_kill':0,
            'chests_opened':0,
            'refill_chest_destroy':0,
            'cosmetic_tokens':0,
            'skywars_experience':0,
            'angel_of_death_level':1,
        }

        swUnscannedDict = {
            'head_tastiness':('Eww!', 'darkgray'),
            'level':1,
            'prestige':('No','gray'),
            'xpRemainder':20,
            'winsRemainder':2,
            'presIcon':'☆',
            'games_played':0,
            'winrate':0,
            'arrow_hitrate':0,
            'KDA':0,
            'K/D':0,
            'W/L':0,
            'K/W':0,
            'K/L':0,
            'K/G':0,
            'blocks_placed_per_game':0,
            'eggs_per_game':0,
            'arrows_per_game':0,
            'arrows_hit_per_game':0,
            'pearls_per_game':0,
        }

        if 'wins' in swSTATSVAR or 'losses' in swSTATSVAR:

            # Get the automatable ones - these are already above, I think
            for x in swStatsDict:
                if x in swSTATSVAR: swStatsDict[x] = swSTATSVAR[x]
            
            # Fastest win formatting
            if isinstance(swStatsDict['fastest_win'], int): swStatsDict['fastest_win'] = sec2format2ydhms(sec2format(swStatsDict['fastest_win']))

            # Games played, K/D, W/L
            swUnscannedDict['games_played'] = swStatsDict['wins'] + swStatsDict['losses']
            swUnscannedDict['K/D'] = weirdDiv(swStatsDict['kills'], swStatsDict['deaths'])
            swUnscannedDict['W/L'] = weirdDiv(swStatsDict['wins'],swStatsDict['losses'])

            # Head tastiness
            if rankv3: 
                if rankv3[0] in sweetHeadsRanks and swStatsDict['kills'] < 10000: swUnscannedDict['head_tastiness'] = ('Sweet!', 'aqua')
            if swStatsDict['kills'] < 49: swUnscannedDict['head_tastiness'] = ('Eww!', 'darkgray')
            elif swStatsDict['kills'] < 200: swUnscannedDict['head_tastiness'] = ('Yucky!', 'gray')
            elif swStatsDict['kills'] < 500: swUnscannedDict['head_tastiness'] = ('Meh.','lightgray')
            elif swStatsDict['kills'] < 1000: swUnscannedDict['head_tastiness'] = ('Decent...','yellow')
            elif swStatsDict['kills'] < 2000: swUnscannedDict['head_tastiness'] = ('Salty.','lime')
            elif swStatsDict['kills'] < 5000: swUnscannedDict['head_tastiness'] = ('Tasty!','dark_aqua')
            elif swStatsDict['kills'] < 10000: swUnscannedDict['head_tastiness'] = ('Succulent!','light_purple')
            elif swStatsDict['kills'] < 25000: swUnscannedDict['head_tastiness'] = ('Divine!','gold')
            else: swUnscannedDict['head_tastiness'] = ('Heavenly..!', 'dark_purple')

            # Winrate, arrow hitrate, KDA, K/W, K/L, K/G, blocks/game, eggs/game, arrows/game, pearls/game
            swUnscannedDict['winrate'] = weirdDiv(100*swStatsDict['wins'], swUnscannedDict['games_played'], 2)
            swUnscannedDict['arrow_hitrate'] = weirdDiv(100*swStatsDict['arrows_hit'],swStatsDict['arrows_shot'],2)
            swUnscannedDict['KDA'] = weirdDiv((swStatsDict['kills']+swStatsDict['assists']),swStatsDict['deaths'])
            swUnscannedDict['K/W'] = weirdDiv(swStatsDict['kills'],swStatsDict['wins'])
            swUnscannedDict['K/L'] = weirdDiv(swStatsDict['kills'],swStatsDict['losses'])
            swUnscannedDict['K/G'] = weirdDiv(swStatsDict['kills'],swUnscannedDict['games_played'])
            swUnscannedDict['blocks_placed_per_game'] = weirdDiv(swStatsDict['blocks_placed'],swUnscannedDict['games_played'])
            swUnscannedDict['eggs_per_game'] = weirdDiv(swStatsDict['egg_thrown'],swUnscannedDict['games_played'])
            swUnscannedDict['arrows_per_game'] = weirdDiv(swStatsDict['arrows_shot'],swUnscannedDict['games_played'])
            swUnscannedDict['arrows_hit_per_game'] = weirdDiv(swStatsDict['arrows_hit'],swUnscannedDict['games_played'])
            swUnscannedDict['pearls_per_game'] = weirdDiv(swStatsDict['enderpearls_thrown'],swUnscannedDict['games_played'])

        # Leveling stuff
            # Function that takes in experience and spits out level as a floating point number
            def swexp2level(experience):
                expertest = 0
                level = 0
                if experience <= 15000:
                    if experience < 20: return (1 + (experience - 0) / 20, 20-experience)
                    elif experience < 70: return (2 + (experience - 20) / 50, 70-experience)
                    elif experience < 150: return (3 + (experience - 70) / 80, 150-experience)
                    elif experience < 250: return (4 + (experience - 150) / 100, 250-experience)
                    elif experience < 500: return (5 + (experience - 250) / 250, 500-experience)
                    elif experience < 1000: return (6 + (experience - 500) / 500, 1000-experience)
                    elif experience < 2000: return (7 + (experience - 1000) / 1000, 2000-experience)
                    elif experience < 3500: return (8 + (experience - 2000) / 2500, 3500-experience)
                    elif experience < 6000: return (9 + (experience - 3500) / 4000, 6000-experience)
                    elif experience < 10000: return (10 + (experience - 6000) / 5000, 10000-experience)
                    elif experience < 15000: return (11 + (experience - 10000) / 10000, 15000-experience)
                elif experience > 14999:
                    expertest = experience - 15000
                    toNextLevel = 10000 - expertest % 10000
                    return (expertest / 10000 + 12, toNextLevel)

            # Function that takes in level and spits out prestige and color as a tuple
            def getPrestige(level):
                try:
                    if level < 5: return ('No', 'gray')
                    if level < 10: return ('Iron', 'lightgray')
                    if level < 15: return ('Gold', 'gold')
                    if level < 20: return ('Diamond', 'aqua')
                    if level < 25: return ('Emerald', 'dark_green')
                    if level < 30: return ('Sapphire', 'blue')
                    if level < 35: return ('Ruby', 'dark_red')
                    if level < 40: return ('Crystal', 'light_purple')
                    if level < 45: return ('Opal', 'dark_blue')
                    if level < 50: return ('Amethyst', 'dark_purple')
                    if level >= 50: return ('Rainbow', 'chocolate')
                except:
                    return ('No', 'gray')
            
            swLevelStuffYes = swexp2level(swStatsDict['skywars_experience'])
            swUnscannedDict['level'] = swLevelStuffYes[0]
            swUnscannedDict['prestige'] = getPrestige(swUnscannedDict['level'])
            swUnscannedDict['xpRemainderPerc'] = round(100*(swUnscannedDict['level']-math.floor(swUnscannedDict['level'])),2)
            swUnscannedDict['xpRemainder'] = swLevelStuffYes[1]
            swUnscannedDict['winsRemainder'] = math.ceil(swLevelStuffYes[1]/10)
            if 'levelFormatted' in swSTATSVAR: swUnscannedDict['presIcon'] = re.sub('[0-9a-zA-Z§]', '', swSTATSVAR['levelFormatted'])
            swUnscannedDict['level'] = math.floor(swUnscannedDict['level'])

        else: swStatsDict['success']:False

        ########## SkyWars Mode Stats I
        STRML = ['solo','team','ranked','mega','lab']
        swBestGame = [0, False]
        def swModeStats(statsList, gamemoder):

            # Add main stats to all gamemodes
            statsList['kills'] = swSTATSVAR.get('kills_'+gamemoder,0)
            statsList['kills%'] = weirdDiv(100*statsList['kills'], swStatsDict['kills'], 4)
            statsList['deaths'] = swSTATSVAR.get('deaths_'+gamemoder,0)
            statsList['deaths%'] = weirdDiv(100*statsList['deaths'], swStatsDict['deaths'], 4)
            statsList['K/D'] = weirdDiv(statsList['kills'], statsList['deaths'])
            statsList['wins'] = swSTATSVAR.get('wins_'+gamemoder,0)
            statsList['wins%'] = weirdDiv(100*statsList['wins'], swStatsDict['wins'], 4)
            statsList['losses'] = swSTATSVAR.get('losses_'+gamemoder,0)
            statsList['losses%'] = weirdDiv(100*statsList['losses'], swStatsDict['losses'], 4)
            statsList['games_played'] = statsList['wins'] + statsList['losses']
            statsList['games_played%'] = weirdDiv(100*statsList['games_played'], swUnscannedDict['games_played'], 4)

            # Most played game
            if statsList['games_played'] > swBestGame[0] and gamemoder not in STRML: 
                swBestGame[0] = statsList['games_played']
                swBestGame[1] = gamemoder.replace('_',' ').title()

            statsList['W/L'] = weirdDiv(statsList['wins'], statsList['losses'],4)
            statsList['winperc'] = weirdDiv(100*statsList['W/L'], 1+statsList['W/L'], 2) 
            statsList['kdrel'] = round(statsList['K/D']-swUnscannedDict['K/D'],4)
            statsList['kdrelperc'] = round(100*(weirdDiv(statsList['K/D'], swUnscannedDict['K/D'])-1),2)
            statsList['wlrel'] = round(statsList['W/L']-swUnscannedDict['W/L'],4)
            statsList['wlrelperc'] = round(100*(weirdDiv(statsList['W/L'], swUnscannedDict['W/L'])-1),2)

            # Add special stats to main gamemodes
            if gamemoder in STRML:
                statsList['survived_players'] = swSTATSVAR.get('survived_players_'+gamemoder,0)
                statsList['survived_players%'] = weirdDiv(100*statsList['survived_players'], swStatsDict['survived_players'], 4)
                statsList['assists'] = swSTATSVAR.get('assists_'+gamemoder,0)
                statsList['assists%'] = weirdDiv(100*statsList['assists'], swStatsDict['assists'], 4)
                statsList['fastest_win'] =sec2format2ydhms(sec2format(swSTATSVAR.get('fastest_win_'+gamemoder,0)))
                statsList['most_kills_game'] = swSTATSVAR.get('most_kills_game_'+gamemoder,0)
                if gamemoder != 'lab':
                    statsList['kit'] = swSTATSVAR.get('activeKit_'+gamemoder.upper(), 'Default').split('_')[-1].replace('-',' ').title()

            # If team, add kit correctly, and correct ranked most_kills_game
            if gamemoder == 'team':
                statsList['kit'] = swSTATSVAR.get('activeKit_TEAMS','Default').split('_')[-1].title().replace('-',' ').title()
            if gamemoder == 'ranked' and statsList['most_kills_game'] > 3:
                statsList['most_kills_game'] = 3
            return statsList

        swSoloStatsList = {'games_played':0}
        swTeamStatsList = {'games_played':0}
        swRankedStatsList = {'games_played':0}
        swMegaStatsList = {'games_played':0}
        swLabStatsList = {'games_played':0}
        for x, y in zip([swSoloStatsList,swTeamStatsList,swRankedStatsList,swMegaStatsList,swLabStatsList], ['solo', 'team', 'ranked', 'mega', 'lab']):
            if 'losses_'+y in swSTATSVAR or 'wins_'+y in swSTATSVAR: x = swModeStats(x, y) 

        swSoloNormal = {'games_played':0}
        swSoloInsane = {'games_played':0}
        swTeamsNormal = {'games_played':0}
        swTeamsInsane = {'games_played':0}
        swMegaDoubles = {'games_played':0}
        swLabSolo = {'games_played':0}
        swLabTeams = {'games_played':0}
        for x, y in zip([swSoloNormal,swSoloInsane,swTeamsNormal,swTeamsInsane,swMegaDoubles, swLabSolo, swLabTeams], ['solo_normal', 'solo_insane', 'team_normal', 'team_insane', 'mega_doubles', 'lab_solo', 'lab_team']):
            if 'losses_'+y in swSTATSVAR or 'wins_'+y in swSTATSVAR: x = swModeStats(x, y)

        ########## SkyWars Kill Types
        swKillTypeList = {}
        swKTLList = []
        otherSwKills = 0
        for killType in ['melee', 'void', 'bow', 'mob', 'fall']:
            try:
                localKTL = swSTATSVAR[killType + '_kills']
                swKillTypeList[killType] = (localKTL, round(100*weirdDiv(localKTL, swStatsDict['kills']),2))
                swKillTypeList['success'] = True
                swKTLList.append(swKillTypeList[killType][0])
                otherSwKills += localKTL
            except:
                swKillTypeList[killType] = (0, 0)
        actualOtherSwKills = swStatsDict['kills']-otherSwKills
        swKillTypeList['other'] = (actualOtherSwKills, round(100*weirdDiv(actualOtherSwKills, swStatsDict['kills']),2))
        swKTLList.append(actualOtherSwKills)

        ########## Time Wasted
        try:
            TIMEOVERALL = swSTATSVAR['time_played']-swSTATSVAR['time_played_mega_doubles']+swSTATSVAR['time_played_lab'] if 'time_played_mega_doubles' in swSTATSVAR and 'time_played_lab' in swSTATSVAR else swSTATSVAR['time_played']
        except:
            TIMEOVERALL = 0
        try:
            swPercPlayedLife = round(100*TIMEOVERALL/(time.time()-firstLoginUnix),4)
        except: swPercPlayedLife = 0
        swTimeList = []
        swTimeListPerc = []
        swTimeModeList = ['Solo', 'Teams', 'Mega', 'Ranked', 'Laboratory']
        swTimeColorList = ['soloe','teamse','megae','rankede','laboratorye']
        for mode in ['_solo', '_team','_mega','_ranked','_lab']:
            try:
                timePlayedForThisMode = swSTATSVAR['time_played'+mode]
                swTimeList.append(sec2format2ydhms(sec2format(timePlayedForThisMode)))
                swTimeListPerc.append(round(100*(timePlayedForThisMode/TIMEOVERALL), 2))
            except:
                swTimeList.append('0s')
                swTimeListPerc.append(0)
        swTimeList.append(sec2format2ydhms(sec2format(TIMEOVERALL)))
        swTimeListPercMinusOverall = swTimeListPerc#[:-1]

        swUnitConvList = []
        swUnitConvList.append((round(TIMEOVERALL/31536000, 4), 'years'))
        swUnitConvList.append((round(TIMEOVERALL/2628000, 4), 'months'))
        swUnitConvList.append((round(TIMEOVERALL/604800, 4), 'weeks'))
        swUnitConvList.append((round(TIMEOVERALL/86400, 4), 'days'))
        swUnitConvList.append((round(TIMEOVERALL/3600, 3), 'hours'))
        swUnitConvList.append((round(TIMEOVERALL/60, 2), 'minutes'))
        swUnitConvList.append((TIMEOVERALL, 'seconds'))

        swUnitConvList2 = []
        swUnitConvList2.append(('Run ', round(TIMEOVERALL/570, 2), ' miles'))
        swUnitConvList2.append(('Written out ', round(TIMEOVERALL/750, 2), ' essays'))
        swUnitConvList2.append(('Eaten ', round(TIMEOVERALL/1800, 2), ' meals'))
        swUnitConvList2.append(('Watched ', round(TIMEOVERALL/6600, 2), ' feature-length films'))
        swUnitConvList2.append(("Charged your phone's battery ", math.floor(TIMEOVERALL/79.2), '%'))
        swUnitConvList2.append(('Flown the longest international flight ', round(TIMEOVERALL/66600, 2), ' times'))
        swUnitConvList2.append(('Watched Law and Order ', round(TIMEOVERALL/1.148e+6, 2), ' times'))
        swUnitConvList2.append(('Driven across the United States ', round(TIMEOVERALL/1.2038e+06, 2), ' times'))
        swUnitConvList2.append(('Earned ', round(TIMEOVERALL/1829088, 4), '% of a PhD'))

        swKperList = []
        swWperList = []
        for kw in ('year', 31536000),('day', 86400), ('hour', 3600), ('minute', 60), ('second', 1):
            try:
                if kw[0] == 'second' or kw[0] == 'minute':
                    swKperList.append((round(swStatsDict['kills']/TIMEOVERALL * kw[1],4), kw[0]))
                else:
                    swKperList.append((round(swStatsDict['kills']/TIMEOVERALL * kw[1],2), kw[0]))
            except: swKperList.append((0, kw[0]))

            try:
                if kw[0] == 'second' or kw[0] == 'minute':
                    swWperList.append((round(swStatsDict['wins']/TIMEOVERALL * kw[1],4), kw[0]))
                else:
                    swWperList.append((round(swStatsDict['wins']/TIMEOVERALL * kw[1],2), kw[0]))
            except: swWperList.append((0, kw[0]))
        # Souls
        swSoulList = {}
        for i in ['souls','souls_gathered','paid_souls','souls_gathered_lab','soul_well_legendaries','soul_well_rares','soul_well']:
            try:
                swSoulList[i] = swSTATSVAR[i]
            except: swSoulList[i] = 0
        
        try:
            swSoulList['souls_nonlab'] = swSoulList['souls_gathered']-swSoulList['souls_gathered_lab']
        except: swSoulList['souls_nonlab'] = 0
        try:
            swSoulList['soul_well_commons'] = (swSTATSVAR['soul_well']-swSTATSVAR['soul_well_legendaries']-swSTATSVAR['soul_well_rares'])
        except: swSoulList['soul_well_commons'] = 0
        try:
            swSoulList['labperc'] = (round(100*swSoulList['souls_gathered_lab']/swSoulList['souls_gathered'], 2), round(100*swSoulList['souls_nonlab']/swSoulList['souls_gathered'], 2))
        except: swSoulList['labperc'] = (0,0)
        swSoulsRaritiesList = [swSoulList['soul_well_commons'], swSoulList['soul_well_rares'], swSoulList['soul_well_legendaries']]

        # Heads
        swHeads = []
        swHeadsSolo = []
        swHeadsTeam = []
        swHeadsImpBool = [False,False,False]

        for x in [('eww','darkgray'),('yucky','gray'),('meh','lightgray'),('decent','yellow'),('salty','green'),('tasty','dark_aqua'),('succulent','pink'), ('sweet','aqua'), ('divine','gold'),('heavenly','dark_purple')]:
            try:
                swHeads.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]], x[1], round(100*swSTATSVAR['heads_'+x[0]]/int(swStatsDict['heads']),2)])
            except: swHeads.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsSolo.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]+'_solo'], x[1], round(100*swSTATSVAR['heads_'+x[0]+'_solo']/int(swStatsDict['heads']),2)])
            except: swHeadsSolo.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsTeam.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]+'_team'], x[1], round(100*swSTATSVAR['heads_'+x[0]+'_team']/int(swStatsDict['heads']),2)])
            except: swHeadsTeam.append([x[0].capitalize(), 0, x[1], 0])

            if 'heads' in swSTATSVAR:
                swHeadsImpBool[0] = swSTATSVAR['heads']
                try:
                    swHeadsImpBool[1] = swSTATSVAR['heads_solo'] 
                except: pass
                try:
                    swHeadsImpBool[2] = swSTATSVAR['heads_team'] 
                except: pass

        swHeads.reverse()
        swHeadsSolo.reverse()
        swHeadsTeam.reverse()

        # Angel's Descent
        swOpals = {}
        swOpals['opals'] = swSTATSVAR.get('opals',0)
        swOpals['shards'] = swSTATSVAR.get('shard',0)
        swOpals['until next opal'] = swOpals['shards'] % 20000
        swOpals['shardsTilNextPerc'] = 100*weirdDiv(swOpals['until next opal'], 20000, 2) #round(100*swOpals['until next opal']/20000,2)
        swOpals['opals from prestige'] = int(swUnscannedDict['level']/5)
        swOpals['shard_solo'] = swSTATSVAR.get('shard_solo',0)
        swOpals['shard_solo_perc'] = weirdDiv(100*swOpals['shard_solo'], swOpals['shards'],2)
        swOpals['shard_team'] = swSTATSVAR.get('shard_team',0)
        swOpals['shard_team_perc'] = weirdDiv(100*swOpals['shard_team'], swOpals['shards'],2)
        swOpals['shards per kill'] = weirdDiv(swOpals['shards'], int(swStatsDict['kills']),2)
        swOpals['shards per game'] = weirdDiv(swOpals['shards'], int(swUnscannedDict['games_played']),2)

        # Favorite maps & cages
        swMapsList = []
        swCagesList = []

        try:
            swPackagesVAR = swSTATSVAR['packages']
            for x in swPackagesVAR:
                if 'favoritemap' in x:
                    swMapsList.append(x.replace('favoritemap_','').title())
                elif 'cage' in x:
                    swCagesList.append(x.replace('cage_','').replace('-cage','').replace('-',' ').replace('_',' ').title())
        except: pass
        swMapsList = re.sub("[\[\]']",'',str(swMapsList))
        swCagesList = re.sub("[\[\]']",'',str(swCagesList))

        # Cosmetics
        swCosmetics = {}
        swCosList = ['balloon','cage','killeffect','killmessages','projectiletrail','sprays','victorydance']
        for i in swCosList:
            if 'active_'+i in swSTATSVAR: swCosmetics[i] = swSTATSVAR['active_'+i].replace(i+'_',r'').replace('-', r' ').replace('_',r' ').title()
        
        # Challenge attempts
        swChalAtt = {}
        swChalAttNum = {}
        try:
            swChalAtt['overall'] = swSTATSVAR['challenge_attempts']
        except: swChalAtt['overall'] = 0
        for i in ['archer','half_health','no_block','no_chest','paper','rookie','uhc','ultimate_warrior']:
            try:
                swChalAtt[i] = swSTATSVAR['challenge_attempts_'+i]
            except KeyError: swChalAtt[i] = 0
        
        for i in range(2,9):
            try:
                swChalAttNum[i] = swSTATSVAR['challenge_attempts_'+str(i)]
            except KeyError: swChalAttNum[i] = 0

        # Challenge wins
        swChalWins = {}
        swChalWinsNum = {}
        try:
            swChalWins['overall'] = swSTATSVAR['challenge_wins']
        except: swChalWins['overall'] = 0
        for i in ['archer','half_health','no_block','no_chest','paper','rookie','uhc','ultimate_warrior']:
            try:
                swChalWins[i] = swSTATSVAR['challenge_wins_'+i]
            except KeyError: swChalWins[i] = 0
        
        for i in range(2,9):
            try:
                swChalWinsNum[i] = swSTATSVAR['challenge_wins_'+str(i)]
            except KeyError: swChalWinsNum[i] = 0

        ########## Printing!

        print('SkyWars is done. ',round(time.time() - start_time, 4), ' sec')

# ! BedWars

    # Overall Stats
        bwOverallStats = {}
        try:
            bwSTATVAR = reqAPI['player']['stats']['Bedwars']
        except: bwSTATVAR = {}

        # Add the stats retrieved from the API
        bwStatsChooseList = [
            'Experience', 
            'games_played_bedwars',
            'kills_bedwars',
            'deaths_bedwars',
            'final_kills_bedwars',
            'final_deaths_bedwars',
            'winstreak',
            'wins_bedwars',
            'losses_bedwars',
            'beds_broken_bedwars',
            'beds_lost_bedwars',
            '_items_purchased_bedwars',
            'resources_collected_bedwars'
            ]

        # Add through iteration
        for item in bwStatsChooseList:
            try:
                bwOverallStats[item] = bwSTATVAR[item]
            except:
                bwOverallStats[item] = 0

        
        # Add 4 criss cross final kill death crap, W/L, and B/L
        for x in [['K/D','kills_bedwars','deaths_bedwars'], ['finK/D','final_kills_bedwars','final_deaths_bedwars'], ['K/FD', 'kills_bedwars', 'final_deaths_bedwars'], ['FK/D', 'final_kills_bedwars', 'deaths_bedwars'], ['W/L', 'wins_bedwars', 'losses_bedwars'], ['B/L', 'beds_broken_bedwars', 'beds_lost_bedwars'], ['items/game', '_items_purchased_bedwars', 'games_played_bedwars'], ['resources/game', 'resources_collected_bedwars', 'games_played_bedwars']]:
            # try:
            bwOverallStats[x[0]] = weirdDiv(bwOverallStats[x[1]], bwOverallStats[x[2]],4)
            # except ZeroDivisionError:
            #     if bwOverallStats[x[1]] == bwOverallStats[x[2]]:
            #         bwOverallStats[x[0]] = 0
            #     else: bwOverallStats[x[0]] = math.inf
            # except:
            #     bwOverallStats[x[0]] = 0
        
        # Add winrate
        try:
            bwOverallStats['winrate'] = round(100*bwOverallStats['wins_bedwars']/bwOverallStats['games_played_bedwars'], 4)
        except ZeroDivisionError:
            if bwOverallStats['wins_bedwars'] == bwOverallStats['games_played_bedwars']:
                bwOverallStats['winrate'] = 0
            else: bwOverallStats['winrate'] = 100
        except:
            bwOverallStats['winrate'] = 0
        
    # Stuff with leveling
        def bwxp2level(xp):
            if xp == 0:
                return 1
            if xp < 486500: #FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK
                if xp < 1500: return 1 + (xp-500)/1000
                elif xp < 3500: return 2 + (xp-1500)/2000
                elif xp < 7000: return 3 + (xp-3500)/3500
                else: return 4 + (xp-7000)/5000
            else: #FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK FIX THIS SHIT IT DOESN"T WORK
                xp4pres = xp % 487000
                pres = xp // 487000
                if xp4pres < 500: return pres*100 + xp4pres/500
                elif xp4pres < 1500: return pres*100 + 1 + (xp4pres-500)/1000
                elif xp4pres < 3500: return pres*100 + 2 + (xp4pres-1500)/2000
                elif xp4pres < 7000: return pres*100 + 3 + (xp4pres-3500)/3500
                else: return pres*100 + 4 +(xp4pres-7000)/5000
        bwOverallStats['level'] = round(bwxp2level(bwOverallStats['Experience']),4)

    # Prestige
        def rlmfl(level):
            return round(100*(level-math.floor(level)),2)

        def lvl2prestige(level):
            try:
                if level < 100: return ('No', 'gray', rlmfl(level))
                if level < 200: return ('Iron', 'lightgray', rlmfl(level))
                if level < 300: return ('Gold', 'gold', rlmfl(level))
                if level < 400: return ('Diamond', 'aqua', rlmfl(level))
                if level < 500: return ('Emerald', 'dark_green', rlmfl(level))
                if level < 600: return ('Sapphire', 'dark_aqua', rlmfl(level))
                if level < 700: return ('Ruby', 'dark_red', rlmfl(level))
                if level < 800: return ('Crystal', 'light_purple', rlmfl(level))
                if level < 900: return ('Opal', 'dark_blue', rlmfl(level))
                if level < 1000: return ('Amethyst', 'dark_purple', rlmfl(level))
                if level < 1100: return ('Rainbow', 'chocolate', rlmfl(level))

                if level < 1200: return ('Iron Prime', 'lightgray', rlmfl(level))
                if level < 1300: return ('Gold Prime', 'gold', rlmfl(level))
                if level < 1400: return ('Diamond Prime', 'aqua', rlmfl(level))
                if level < 1500: return ('Emerald Prime', 'dark_green', rlmfl(level))
                if level < 1600: return ('Sapphire Prime', 'dark_aqua', rlmfl(level))
                if level < 1700: return ('Ruby Prime', 'dark_red', rlmfl(level))
                if level < 1800: return ('Crystal Prime', 'light_purple', rlmfl(level))
                if level < 1900: return ('Opal Prime', 'dark_blue', rlmfl(level))
                if level < 2000: return ('Amethyst Prime', 'dark_purple', rlmfl(level))

                if level < 2100: return ('Mirror', 'mirror', rlmfl(level))
                if level < 2200: return ('Light', 'light', rlmfl(level))
                if level < 2300: return ('Dawn', 'dawn', rlmfl(level))
                if level < 2400: return ('Dusk', 'dusk', rlmfl(level))
                if level < 2500: return ('Air', 'air', rlmfl(level))
                if level < 2600: return ('Wind', 'wind', rlmfl(level))
                if level < 2700: return ('Nebula', 'nebula', rlmfl(level))
                if level < 2800: return ('Thunder', 'thunder', rlmfl(level))
                if level < 2900: return ('Earth', 'earth', rlmfl(level))
                if level < 3000: return ('Water', 'water', rlmfl(level))
                if level >= 3000: return ('Fire', 'fire', rlmfl(level))
                #elif level >= 1000: return ('Rainbow', 'chocolate', rlmfl(level))
            except:
                return ('No', 'gray')

        bwOverallStats['prestige'] = lvl2prestige(bwOverallStats['level'])
        #bwOverallStats['prestige'].append(lvl2prestige(bwOverallStats['level'][1]))
        bwOverallStats['level'] = math.floor(bwOverallStats['level'])

    # Per mode stats
        bwTheStatsList =  [
            'kills_bedwars',
            'deaths_bedwars',
            'final_kills_bedwars',
            'final_deaths_bedwars',
            'iron_resources_collected_bedwars',
            'gold_resources_collected_bedwars',
            'diamond_resources_collected_bedwars',
            'emerald_resources_collected_bedwars',
            'games_played_bedwars',
            'winstreak',
            'wins_bedwars',
            'losses_bedwars',
            'beds_broken_bedwars',
            'beds_lost_bedwars',
            '_items_purchased_bedwars',
            'resources_collected_bedwars']
        bwTranslateList = {
            'eight_one':'Solo',
            'eight_two':'Duos',
            'four_three':'3\'s',
            'four_four':'4\'s',
            'two_four':'4v4',
            'eight_two_armed':'Duos Armed',
            'four_four_armed':'4\'s Armed',
            'castle':'Castle',
            'eight_one_rush':'Solo Rush',
            'eight_two_rush': 'Duos Rush',
            'four_four_rush': '4\'s Rush',
            'eight_one_ultimate':'Solo Ultimate',
            'eight_two_ultimate':'Duos Ultimate',
            'four_four_ultimate':'4\'s Ultimate',
            'eight_two_lucky':'Duos Lucky',
            'four_four_lucky': '4\'s Lucky',
            'eight_two_voidless':'Duos Voidless',
            'four_four_voidless':'4\'s Voidless',
            'tourney_bedwars4s_1':'Tournament (4\'s)',
            'tourney_bedwars_two_four_0':'Tournament (4v4)'}
        bwMKWList = [0,0,0,'','','']
        bwModeStats = {}
        bwCompList = {}
        bwKillsPerMode = {}
        bwFinKillsPerMode = {}
        bwModeLabels = [[],[]]
        for mode in [
            'eight_one','eight_two','four_three','four_four','two_four',
            'eight_two_armed','four_four_armed',
            'castle',
            'eight_one_rush','eight_two_rush','four_four_rush',
            'eight_one_ultimate','eight_two_ultimate','four_four_ultimate',
            'eight_two_lucky','four_four_lucky',
            'eight_two_voidless','four_four_voidless',
            'tourney_bedwars4s_1','tourney_bedwars_two_four_0']:
            bwModeStats[mode] = {}
            for stat in bwTheStatsList:
                if stat in ['eight_one','eight_two','four_three','four_four','two_four']:
                    try:
                        bwModeStats[mode][stat] = (bwSTATVAR[mode][stat], round(100*bwSTATVAR[mode][stat]/bwSTATVAR[stat],2))
                    except: bwModeStats[mode][stat] = (0,0)
                else:
                    try:
                        bwModeStats[mode][stat] = (bwSTATVAR[mode+'_'+stat], round(100*bwSTATVAR[mode+'_'+stat]/bwSTATVAR[stat],2))
                    except: bwModeStats[mode][stat] = (0,0)
                try:
                    bwKillsPerMode[bwTranslateList[mode]] = bwModeStats[mode]['kills_bedwars'][0]
                    bwModeLabels[0].append(bwTranslateList[mode])
                except: pass
                try:
                    bwFinKillsPerMode[bwTranslateList[mode]] = bwModeStats[mode]['final_kills_bedwars'][0]
                    bwModeLabels[1].append(bwTranslateList[mode])
                except: pass
            
        # Kills per deaths with some final mixing in calculations
            bwModeStats[mode]['K/D'] = weirdDiv(bwModeStats[mode]['kills_bedwars'][0], bwModeStats[mode]['deaths_bedwars'][0],4)
            bwModeStats[mode]['finK/D'] = weirdDiv(bwModeStats[mode]['final_kills_bedwars'][0], bwModeStats[mode]['final_deaths_bedwars'][0],4)
            bwModeStats[mode]['K/FD'] = weirdDiv(bwModeStats[mode]['kills_bedwars'][0], bwModeStats[mode]['final_deaths_bedwars'][0],4)
            bwModeStats[mode]['FK/D'] = weirdDiv(bwModeStats[mode]['final_kills_bedwars'][0], bwModeStats[mode]['deaths_bedwars'][0],4)

        # Win/loss ratio & winrate
            bwModeStats[mode]['W/L'] = weirdDiv(bwModeStats[mode]['wins_bedwars'][0], bwModeStats[mode]['losses_bedwars'][0],4)
            bwModeStats[mode]['winrate'] = weirdDiv(100*bwModeStats[mode]['wins_bedwars'][0], bwModeStats[mode]['games_played_bedwars'][0],2)
            
            # Bed break/lose
            bwModeStats[mode]['B/L'] = weirdDiv(bwModeStats[mode]['beds_broken_bedwars'][0], bwModeStats[mode]['beds_lost_bedwars'][0],4)
            
            # Items and resources per game
            bwModeStats[mode]['purc/game'] = weirdDiv(bwModeStats[mode]['_items_purchased_bedwars'][0], bwModeStats[mode]['games_played_bedwars'][0],4)
            bwModeStats[mode]['resc/game'] = weirdDiv(bwModeStats[mode]['resources_collected_bedwars'][0],bwModeStats[mode]['games_played_bedwars'][0],4)

        # Comparative skills
            bwCompList[mode] = {}
            try:
                bwCompList[mode]['compkd'] = (round(bwModeStats[mode]['K/D'] - bwOverallStats['K/D'],4), round(100*(bwModeStats[mode]['K/D']/bwOverallStats['K/D'] - 1),2))
            except: bwCompList[mode]['compkd'] = (0,0)
            try:
                bwCompList[mode]['compfkd'] = (round(bwModeStats[mode]['finK/D'] - bwOverallStats['finK/D'],4), round(100*(bwModeStats[mode]['finK/D']/bwOverallStats['finK/D'] - 1),2))
            except: bwCompList[mode]['compfkd'] = (0,0)
            try:
                bwCompList[mode]['compwl'] = (round(bwModeStats[mode]['W/L'] - bwOverallStats['W/L'],4), round(100*(bwModeStats[mode]['W/L']/bwOverallStats['W/L'] - 1),2))
            except: bwCompList[mode]['compwl'] = (0,0)
        
        # Most, Best, Worst
            if bwModeStats[mode]['games_played_bedwars'][0] > bwMKWList[0]:
                bwMKWList[0] = bwModeStats[mode]['games_played_bedwars'][0]
                bwMKWList[3] = bwTranslateList[mode]
            if bwModeStats[mode]['K/D'] > bwMKWList[1]: 
                bwMKWList[1] =bwModeStats[mode]['K/D']
                bwMKWList[4] = bwTranslateList[mode]
            if bwModeStats[mode]['W/L'] > bwMKWList[2]: 
                bwMKWList[2] = bwModeStats[mode]['W/L']
                bwMKWList[5] = bwTranslateList[mode]

    # Kills via
        bwKillsVia = {
            'Projectile':'projectile',
            'Void':'void',
            'Magic':'magic',
            'Entity':'entity',
            'Entity explosion':'entity_explosion',
            'Fire':'final_tick',
            'Fall damage':'fall',
        }
        bwTakeKillsCount = 0
        bwPureKillsVia = []
        for x, y in bwKillsVia.items():
            try:
                bwKillsVia[x] = (bwSTATVAR[y+'_kills_bedwars'], round(100*bwSTATVAR[y+'_kills_bedwars']/bwOverallStats['kills_bedwars'],2))
                bwTakeKillsCount += bwKillsVia[x][0]
                bwPureKillsVia.append(bwKillsVia[x][0])
            except: 
                bwKillsVia[x] = [0,0]
                bwPureKillsVia.append(0)
        try:
            bwKillsVia['Melee'] = (bwOverallStats['kills_bedwars'] - bwTakeKillsCount, round(100*(bwOverallStats['kills_bedwars'] - bwTakeKillsCount)/bwOverallStats['kills_bedwars'],2))
            bwPureKillsVia.append(bwKillsVia['Melee'][0])
        except: 
            bwKillsVia['Melee'] = (0,0)
            bwPureKillsVia.append(0)

    # Final kills via
        bwFinKillsVia = {
            'Projectile':'projectile',
            'Void':'void',
            'Magic':'magic',
            'Entity':'entity',
            'Entity explosion':'entity_explosion',
            'Fire':'final_tick',
            'Fall damage':'fall',
        }
        bwTakeFinKillsCount = 0
        bwPureFinKillsVia = []
        for x, y in bwFinKillsVia.items():
            try:
                bwFinKillsVia[x] = (bwSTATVAR[y+'_final_kills_bedwars'], round(100*bwSTATVAR[y+'_final_kills_bedwars']/bwOverallStats['final_kills_bedwars'],2))
                bwTakeFinKillsCount += bwFinKillsVia[x][0]
                bwPureFinKillsVia.append(bwFinKillsVia[x][0])
            except: 
                bwFinKillsVia[x] = [0,0]
                bwPureFinKillsVia.append(0)
        try:
            bwFinKillsVia['Melee'] = (bwOverallStats['final_kills_bedwars'] - bwTakeFinKillsCount, round(100*(bwOverallStats['final_kills_bedwars'] - bwTakeFinKillsCount)/bwOverallStats['final_kills_bedwars'],2))
            bwPureFinKillsVia.append(bwFinKillsVia['Melee'][0])
        except: 
            bwFinKillsVia['Melee'] = (0,0)
            bwPureFinKillsVia.append(0)
    
    # Loot crates
        bwLootBoxes = {} # boxes opened, legendaries, epics, rares, commons, lunar, easter, halloween, christmas
        bwLootPure = []
        try:
            bwLootBoxes['bedwars_box'] = bwSTATVAR['bedwars_box']
        except: bwLootBoxes['bedwars_box'] = 0
        for x in ['bedwars_boxes','bedwars_box_legendaries','bedwars_box_epics','bedwars_box_rares','bedwars_box_commons', 'bedwars_lunar_boxes','bedwars_easter_boxes','bedwars_halloween_boxes','bedwars_christmas_boxes']:
            try:
                bwLootBoxes[x] = (bwSTATVAR[x], round(100*(bwSTATVAR[x]/bwLootBoxes['bedwars_box']),2))
                bwLootPure.append(bwLootBoxes[x][0])
            except:
                bwLootBoxes[x] = (0,0)
                bwLootPure.append(0)
    
    # Resources collected
        bwResCol = [] # Iron, Gold, Diamonds, Emeralds, Wrapped Presents
        bwItemsPurchased = bwSTATVAR['_items_purchased_bedwars'] if '_items_purchased_bedwars' in bwSTATVAR else 0
        bwTotalResources = bwSTATVAR['resources_collected_bedwars'] if 'resources_collected_bedwars' in bwSTATVAR else 0
        bwResColPerc = []
        for x in ['iron','gold','diamond','emerald','wrapped_present']:
            if x+'_resources_collected_bedwars' in bwSTATVAR:
                bwResCol.append(bwSTATVAR[x+'_resources_collected_bedwars'])
                bwResColPerc.append(weirdDiv(100*bwSTATVAR[x+'_resources_collected_bedwars'], bwTotalResources,2))
            else:
                bwResCol.append(0)
    
    # Cosmetics
        bwCosmetics = {}
        if 'activeBedDestroy' in bwSTATVAR: bwCosmetics['Bed Destroy'] = bwSTATVAR['activeBedDestroy'].replace('beddestroy_','').replace('_',' ').title()
        if 'activeDeathCry' in bwSTATVAR: bwCosmetics['Death Cry'] = bwSTATVAR['activeDeathCry'].replace('deathcry_','').replace('_',' ').title()
        if 'activeGlyph' in bwSTATVAR: bwCosmetics['Glyph'] = bwSTATVAR['activeGlyph'].replace('glyph_','').replace('_',' ').title()
        if 'activeIslandTopper' in bwSTATVAR: bwCosmetics['Island Topper'] = bwSTATVAR['activeIslandTopper'].replace('islandtopper_','').replace('_',' ').title()
        if 'activeKillEffect' in bwSTATVAR: bwCosmetics['Kill Effect'] = bwSTATVAR['activeKillEffect'].replace('killeffect_','').replace('_',' ').title()
        if 'activeKillMessages' in bwSTATVAR: bwCosmetics['Kill Messages'] = bwSTATVAR['activeKillMessages'].replace('killmessages_','').replace('_',' ').title()
        if 'activeNPCSkin' in bwSTATVAR: bwCosmetics['NPC Shop Skin'] = bwSTATVAR['activeNPCSkin'].replace('npcskin_','').replace('_',' ').title()
        if 'activeProjectileTrail' in bwSTATVAR: bwCosmetics['Projectile Trail'] = bwSTATVAR['activeProjectileTrail'].replace('projectiletrail_','').replace('_',' ').title()
        if 'activeSprays' in bwSTATVAR: bwCosmetics['Spray'] = bwSTATVAR['activeSprays'].replace('sprays_','').replace('_',' ').title()
        if 'activeVictoryDance' in bwSTATVAR: bwCosmetics['Victory Dance'] = bwSTATVAR['activeVictoryDance'].replace('victorydance_','').replace('_',' ').title()
        if 'activeWoodType' in bwSTATVAR: bwCosmetics['Wood Skin'] = bwSTATVAR['activeWoodType'].replace('woodSkin_','').replace('_',' ').title()
        # return 'fu'

        print('BedWars is done. ',round(time.time() - start_time, 4), ' sec')

# ! Guild PLEASE FIX THIS YOU GOTTA USE 25KARMA API
        guildDict = {'success':False,'selfGuildRank':'Member'}
        def guildLevel(exp):
            # A list of amount of XP required for leveling up in each of the beginning levels (1-15).
            EXP_NEEDED = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 2000000, 2500000, 2500000, 2500000, 2500000, 2500000, 3000000]
            level = 0

            for i in range(1000):
            # Increment by one from zero to the level cap.
                need = 0
                if  i >= len(EXP_NEEDED):
                    need = EXP_NEEDED[len(EXP_NEEDED) - 1]
                else:
                    need = EXP_NEEDED[i]
                # Determine the current amount of XP required to level up,
                # in regards to the "i" variable.
        
                if (exp - need) < 0:
                    return [((level + (exp / need)) * 100) / 100, need]
                # If the remaining exp < the total amount of XP required for the next level,
                # return their level using this formula.

                level += 1
                exp -= need
                # Otherwise, increase their level by one,
                # and subtract the required amount of XP to level up,
                # from the total amount of XP that the guild had.

            return [1000, 3000000]
            # This should never happen...

        if playedOnHypixel:
            variable_name = reqses.get('https://api.hypixel.net/guild?key='+ HAPIKEY2 + '&player=' + uuid)
            greqAPI = variable_name.json()
            print('RIGHT AFTER GUILD DATA is being gotten. ',(time.time() - start_time), ' sec')
            guildListAPI = greqAPI.get('guild', False)

            if greqAPI['guild']:

            # Guild info
                # Gets the automatable ones
                for x in ['exp','joinable','tag', '_id', 'name', 'coins','coinsEver', 'publiclyListed','legacyRanking', 'preferredGames', 'achievements']:
                    guildDict[x] = guildListAPI.get(x, False)
                
                # Extension to those above who have some special thing they need changed
                guildDict['created'] = datetime.fromtimestamp(guildListAPI.get('created',False)/1000).strftime('%b %d, %Y @ %I:%M:%S %p')
                guildDict['tagColor'] = guildListAPI.get('tagColor', 'gray')
                guildDict['description'] = guildListAPI.get('description', False)

                # Preferred games
                guildDict['preferredGamesTL'] = []
                if guildDict['preferredGames']:
                    for i in guildDict['preferredGames']:
                        guildDict['preferredGamesTL'].append(gameTranslate(i))
                guildDict['preferredGamesTL'] = re.sub("[\[\]']",'',str(guildDict['preferredGamesTL']))

                # Guild ranks
                guildDict['theGuildRanks'] = {}
                if guildListAPI.get('ranks'):
                    for x in guildListAPI.get('ranks'):
                        try:
                            listenGuild = []
                            listenGuild.append(x.get('default', False))
                            listenGuild.append(x.get('tag', ''))
                            listenGuild.append(datetime.fromtimestamp(x.get('created', 0)/1000).strftime('%b %d, %Y @ %I:%M:%S %p'))
                            guildDict['theGuildRanks'][x.get('name', 'Unnamed rank')] = listenGuild
                        except: 
                            guildDict['theGuildRanks'][x.get('name', 'Unnamed rank')] = [False, None, 'Unknown date']

                # GXP by game
                guildDict['GXPBG'] = {}
                try:
                    for x,y in guildListAPI['guildExpByGameType'].items():
                        if y:
                            guildDict['GXPBG'][gameTranslate(x)] = y 
                    guildDict['GXPBG'] = {k: v for k, v in sorted(guildDict['GXPBG'].items(), reverse=True, key=lambda item: item[1])}
                except: pass

                # Guild level
                guildLevelTempVar = guildLevel(guildDict['exp'])
                guildDict['level'] = guildLevelTempVar[0]
                guildDict['levelLeft'] = round(guildLevelTempVar[0] % 1 * guildLevelTempVar[1],2)
                guildDict['levelPercThere'] = round(100*(guildLevelTempVar[0] % 1),2)

                print('guild info done. ', (time.time() - start_time), ' sec')

            # remnants
                for i in guildListAPI['members']:
                    if i['uuid'] == uuid: guildDict['selfGuildRank'] = i['rank'] 
                guildDict['success'] = True

        print('Guild is done. ',round(time.time() - start_time, 4), ' sec')

# ! Render base.html        
        print("--- %s seconds ---" % (time.time() - start_time))

        # Designated Crapification
        #print('firstLogin')
        #print(firstLoginUnix)
        
        return render_template('base.html', uuid=uuid, username=username, namehis=namehis, profile='reqAPI', reqList=karma, achpot=achpot, achievements=achievements, level=level, levelProgress=levelProgress, levelplusone=levelplusone, lastLogin=lastLogin, lastLoginUnix=lastLoginUnix, firstLogin=firstLogin, firstLoginUnix=firstLoginUnix, lastLogoutUnix=lastLogoutUnix, lastLogout=lastLogout, lastSession=lastSession, rankv3=rankv3, multiplier=multiplier, swStatsDict=swStatsDict, swUnscannedDict=swUnscannedDict, joinedAgoText=joinedAgoText, seniority=seniority, boughtPastRank=boughtPastRank, quests=quests, currentSession=currentSession, sessionType=sessionType, boughtPastTime=boughtPastTime, twitter=twitter, instagram=instagram, twitch=twitch, discord=discord, hypixelForums=hypixelForums, youtube=youtube, gamemodes={'Solo':swSoloStatsList,'Teams':swTeamStatsList,'Ranked':swRankedStatsList,'Mega':swMegaStatsList, 'Laboratory':swLabStatsList},gamemodes2={'Solo Normal':swSoloNormal, 'Solo Insane':swSoloInsane, 'Teams Normal':swTeamsNormal, 'Teams Insane':swTeamsInsane, 'Mega Doubles':swMegaDoubles, 'Laboratory Solo':swLabSolo, 'Laboratory Teams':swLabTeams}, swKillTypeList=swKillTypeList, swKTLList=json.dumps(swKTLList), swTimeLists=[swTimeList, swTimeListPerc, swTimeColorList], swTimeModeList=swTimeModeList, swTimeListPercMinusOverall=swTimeListPercMinusOverall, swUnitConvList=swUnitConvList, swUnitConvList2=swUnitConvList2, swSoulList=swSoulList, swSoulsRaritiesList=swSoulsRaritiesList, swHeadsListList=(swHeads,swHeadsSolo,swHeadsTeam), swHeadsRaw=[swHeads[0][1],swHeads[1][1],swHeads[2][1],swHeads[3][1],swHeads[4][1],swHeads[5][1],swHeads[6][1],swHeads[7][1],swHeads[8][1],swHeads[9][1]], swHeadsRawSolo=[swHeadsSolo[0][1],swHeadsSolo[1][1],swHeadsSolo[2][1],swHeadsSolo[3][1],swHeadsSolo[4][1],swHeadsSolo[5][1],swHeadsSolo[6][1],swHeadsSolo[7][1],swHeadsSolo[8][1],swHeadsSolo[9][1]], swHeadsRawTeam=[swHeadsTeam[0][1],swHeadsTeam[1][1],swHeadsTeam[2][1],swHeadsTeam[3][1],swHeadsTeam[4][1],swHeadsTeam[5][1],swHeadsTeam[6][1],swHeadsTeam[7][1],swHeadsTeam[8][1],swHeadsTeam[9][1]], swKWperLists=(swKperList, swWperList, swPercPlayedLife), swOpals=swOpals, swBestGame = swBestGame, bwOverallStats=bwOverallStats, bwModeStats=bwModeStats, bwTranslateList=bwTranslateList, bwCompList=bwCompList, bwMKWList=bwMKWList, bwKillsList=(bwKillsVia, bwKillsPerMode, bwFinKillsVia, bwFinKillsPerMode), bwPureKillsLists=[bwPureKillsVia, bwPureFinKillsVia], bwLootBoxes=bwLootBoxes, bwLootPure=bwLootPure, bwResCol=bwResCol, bwResColPerc=bwResColPerc, bwItemsPurchased=bwItemsPurchased, bwTotalResources=bwTotalResources, bwCosmetics=bwCosmetics, userLanguage=userLanguage, userVersion=userVersion, totalKills=totalKills, totalWins=totalWins, totalCoins=totalCoins, giftsMeta=giftsMeta, rewards=rewards, lastPlayed=lastPlayed, lastSeen=lastSeen, lastSeenUnix=lastSeenUnix, swMapsList=swMapsList, swCagesList=swCagesList, swCosmetics=swCosmetics, swHeadsImpBool=swHeadsImpBool, swChalAtt=swChalAtt, swChalAttNum=swChalAttNum, swChalWins=swChalWins, swChalWinsNum=swChalWinsNum, guildDict=guildDict)
    
# ! Invalid username exception
    else:
        noAutocorrect = True
        screwup = 'Oops! This player doesn\'t exist.'
        if len(q) < 3 or len(q) > 16:
            screwup = "A Minecraft username has to be between 3 and 16 characters (with a few special exceptions), and can only contain alphanumeric characters and underscores."
        elif q != re.sub(r'\W+', '', q): 
            screwup = 'Username contains invalid characters. A Minecraft username can only contain alphanumeric characters and underscores.'
            noAutocorrect = re.sub(r'\W+', '', q)
        if any(swear in q.lower() for swear in swearList):
            screwup = "Username might be blocked by Mojang- username contains a blacklisted word. If this is a derivtive of the Scunthorpe problem, sorry about that." #\nhttps://paste.ee/p/RYo2C. \nIf this is a derivative of the Scunthorpe problem, sorry about that."
        return render_template('user404.html', q=q, screwup=screwup, noAutocorrect=noAutocorrect)
        #except:
        #    return "Errored out. Lol"

# ! Friends list (Deprecated & removed)

# ! Friends list (Deprecated & removed)

# ! Actual Guild (Deprecated & removed)

# ! Error handling
@app.errorhandler(404)
def four04(e):
    return render_template('404.html', error=404, text='Page not found', desc='Someone ate all of the tiramisu... is this a broken link?'), 404

@app.errorhandler(400)
def four00(e):
    return render_template('404.html', error=400, text='Bad request', desc='Bad request... try again?'), 400

@app.errorhandler(401)
def four01(e):
    return render_template('404.html', error=401, text='Unauthorized', desc='You can\'t do this. Sorry about that.'), 401

@app.errorhandler(403)
def four03(e):
    return render_template('404.html', error=403, text='Request forbidden', desc='This is an unauthorized request. You cannot access this resource. Apparently.'), 403

@app.errorhandler(500)
def five00(e):
    return render_template('404.html', error=500, text='Internal server error', desc='Oops. Something went wrong trying to fetch this username.'), 500

@app.errorhandler(502)
def five02(e):
    return render_template('404.html', error=502, text='Bad gateway', desc='Hm, something went wrong with the server\'s gateway.'), 502

@app.errorhandler(503)
def five03(e):
    return render_template('404.html', error=503, text='Service unavailable', desc='The server is unavailable at the moment. Check back later.'), 503

# ! Flask initialization
if __name__ == "__main__":
    app.run(debug=True)
    # server = Server(app.wsgi_app)
    # server.serve()