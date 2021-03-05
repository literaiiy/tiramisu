############################################################################ IMPORTING ############################################################################
from flask import Flask, render_template, request, url_for, redirect, flash, session
import json
from mojang import MojangAPI
from flask_wtf import Form
from wtforms import TextField
from datetime import datetime
import requests
import math
import time
import re
from itertools import cycle, islice
from num2words import num2words
import requests_cache
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

############################################################################ INITIALIZATION & CONSTANTS ############################################################################
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

app.secret_key = 'a34w7tfyner9ryhzrbfw7ynhhcdtg78as34'
HAPIKEY = '1e5f6a57-6327-4888-886a-590c39861a6a'
ADMINS = ['35a178c0c37043aea959983223c04de0']
FLOWERS = ['27bcc1547423484683fd811155d8c472']
swearList = ['anal','anus','ass','bastard','bitch','blowjob','blow job','buttplug','clitoris','cock','cunt','dick','dildo','fag','fuck','hell','jizz','nigger','nigga','penis','piss','pussy','scrotum','sex','shit','slut','turd','vagina']
sweetHeadsRanks = ['HELPER', 'MODERATOR', 'ADMIN', 'OWNER']

# requests_cache.install_cache('test_cache', backend='sqlite', expire_after=30)

username = ''
uuid = ''

config = {
    "DEBUG": True,          # some Flask specific configs
    'CACHE_TYPE': 'filesystem', # Flask-Caching related configs
     'CACHE_DIR': '/tmp',  # Flask-Caching directory
    "CACHE_DEFAULT_TIMEOUT": 60
}
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

requests_cache.install_cache('demo_cache', expire_after=3)

class searchBar():
    query = TextField("Search...")


############################################################################ ROUTING FOR HOMEPAGE ############################################################################
@app.route('/', methods=['POST', 'GET'], defaults={'path':''})
def queryt(path):
    gameDict = []
    hs = requests.Session().get('https://api.hypixel.net/gameCounts?key=' + HAPIKEY)
    gameCount = hs.json()['games']
    gameDict = [
        {
            'game':'Total Player Count',
            'playerCount':hs.json()['playerCount']
        },
        {
            'game':'🏹 SkyWars',
            'playerCount':gameCount['SKYWARS']['players']
        },
        {
            'game':'🌎 SkyBlock',
            'playerCount':gameCount['SKYBLOCK']['players']
        },
        {
            'game':'🛏️ BedWars',
            'playerCount':gameCount['BEDWARS']['players']
        },
        {
            'game':'⚔️ Duels',
            'playerCount':gameCount['DUELS']['players']
        },
        {
            'game':'🦸 Super Smash Mobs',
            'playerCount':gameCount['SUPER_SMASH']['players']
        },
        {
            'game':'💨 Speed UHC',
            'playerCount':gameCount['SPEED_UHC']['players']
        },
        {
            'game':'🔫 Cops and Crims',
            'playerCount':gameCount['MCGO']['players']
        },
        {
            'game':'🕳️ The Pit',
            'playerCount':gameCount['PIT']['players']
        },
        {
            'game':'🍎 UHC Champions',
            'playerCount':gameCount['UHC']['players']
        },
        {
            'game':'🛠️ Build Battle',
            'playerCount':gameCount['BUILD_BATTLE']['players']
        },
        {
            'game':'🕵️‍♂️ Murder Mystery',
            'playerCount':gameCount['MURDER_MYSTERY']['players']
        },
        {
            'game':'🏇 Warlords',
            'playerCount':gameCount['BATTLEGROUND']['players']
        },
        {
            'game':'🏠 Housing',
            'playerCount':gameCount['HOUSING']['players']
        },
        {
            'game':'🕹️ Arcade',
            'playerCount':gameCount['ARCADE']['players']
        },
        {
            'game':'🗡️ Blitz Survival Games',
            'playerCount':gameCount['SURVIVAL_GAMES']['players']
        },
        {
            'game':'🧱 Mega Walls',
            'playerCount':gameCount['WALLS3']['players']
        },
        {
            'game':'🏗️ Prototype',
            'playerCount':gameCount['PROTOTYPE']['players']
        },
        {
            'game':'💣 TNT Games',
            'playerCount':gameCount['TNTGAMES']['players']
        },
        {
            'game':'Main Lobby',
            'playerCount':gameCount['MAIN_LOBBY']['players']
        },
        {
            'game':'Watching a replay',
            'playerCount':gameCount['REPLAY']['players']
        },
        {
            'game':'In limbo',
            'playerCount':gameCount['LIMBO']['players']
        },
        {
            'game':'Idle',
            'playerCount':gameCount['IDLE']['players']
        },
        {
            'game':'🎉 Party Games',
            'playerCount':gameCount['ARCADE']['modes']['PARTY']
        },
        {
            'game':'🧟 Zombies',
            'playerCount':gameCount['ARCADE']['modes']['ZOMBIES_DEAD_END'] + gameCount['ARCADE']['modes']['ZOMBIES_ALIEN_ARCADIUM'] + gameCount['ARCADE']['modes']['ZOMBIES_BAD_BLOOD']
        },
        {
            'game':'🙈 Hide and Seek',
            'playerCount':gameCount['ARCADE']['modes']['HIDE_AND_SEEK_PROP_HUNT'] + gameCount['ARCADE']['modes']['HIDE_AND_SEEK_PARTY_POOPER']
        },
        {
            'game':'🛩️ Mini Walls',
            'playerCount':gameCount['ARCADE']['modes']['MINI_WALLS']
        },
        {
            'game':'📢 Hypixel Says',
            'playerCount':gameCount['ARCADE']['modes']['SIMON_SAYS']
        }
    ]
    gameDict = sorted(gameDict, reverse=True, key=lambda k: k['playerCount'])
    for enum, game in enumerate(gameDict):
        game['pos'] = enum
    form = searchBar()
    if request.method == 'POST':
        session['req'] = request.form
        if not session['req']['content'] == '':
            return redirect(url_for('compute', q=str(session['req']['content'])))
    return render_template('index.html', gameDict=gameDict)

@app.route('/<k>', methods=['POST', 'GET'])
def reddorect(k):
    return redirect(url_for('compute', q=k))

############################################################################ ROUTING FOR SEARCH PAGE ############################################################################
@app.route('/p/<q>', methods=['POST','GET'])
@cache.cached(timeout=15)
def compute(q):
    #try:
    start_time = time.time()
    if len(q) == 32 or len(q) == 36:
        q = q.replace('-','')
        try:
            if q == MojangAPI.get_uuid(MojangAPI.get_username(q)):
                username = MojangAPI.get_username(q)
                uuid = q
            else:
                return "That UUID doesn't exist. Try again with a different UUID."
        except:
            return "This UUID doesn't exist. Try again with a different UUID."

    else:
        uuid = MojangAPI.get_uuid(q)
        username = MojangAPI.get_username(MojangAPI.get_uuid(q))
        #else:
        #    return "false uuid or username or smthing"

    if isinstance(uuid, str):
        #username = MojangAPI.get_username(uuid)

############################################################################ JSON PARSING ############################################################################

############################################################################ RETRIEVE FROM API & INITIALIZE ############################################################################
        r = requests.get('https://api.hypixel.net/player?key=' + HAPIKEY + '&uuid=' + uuid)
        reqAPI = r.json()
        reqList = {}
        try:
            reqListKarma = reqAPI['player']['karma']
        except:
            reqListKarma = 0
        reqList['karma']=(f'{int(reqListKarma):,}')
        try:
            hypixelUN = reqAPI['player']['displayname']
        except:
            hypixelUN = username

############################################################################ NAME HISTORY ############################################################################
        namehis = MojangAPI.get_name_history(uuid)
        namehisLength = len(namehis)
        nhutminus1 = 0
        namehisUnix2 = 0
        nhutindex = 0
        nhut2unix = 0
        try:
            namehis[0]['changed_to_at'] = reqAPI['player']['firstLogin']
        except:
            namehis[0]['changed_to_at'] = ''

        # Iterate through dict to add changed_to_at & time_between columns
        for namehisUnixTime in namehis:
            try:
                namehisUnix2 = namehisUnixTime['changed_to_at']
                namehisUnixTime['changed_to_at'] = datetime.fromtimestamp(namehisUnix2/1000).strftime('%b %d, %Y @ %I:%M:%S %p')
                namehisDiff = (namehisUnix2 - nhutminus1)/1000
                namehisUnixTime['time_between'] = namehisDiff
                nhutminus1 = namehisUnix2
                nhutindex += 1
                if nhutindex == 2:
                    nhut2unix = namehisUnix2
                if nhutindex == (len(namehis)):
                    nhut2ndindex = int(time.time())-namehisUnix2/1000 
            except:
                True

        # Gives time_between list
            nhutdate = [0,0,0,0]
            def sec2format(namehisDiff):
                nhutdate[0] = math.floor(namehisDiff / 31536000)
                nhutdate[1] = math.floor(namehisDiff / 86400) - nhutdate[0] * 365
                nhutdate[2] = math.floor(namehisDiff / 3600) - nhutdate[1] * 24 - nhutdate[0] * 365 * 24
                nhutdate[3] = math.floor(namehisDiff / 60) -nhutdate[2] * 60 - nhutdate[1] * 24 * 60 - nhutdate[0] * 365 * 24 * 60
                return [nhutdate[0],nhutdate[1],nhutdate[2],nhutdate[3]]
            try:
                sec2format(namehisDiff)
            except:
                pass

        # Formats time_between list
            if nhutdate[0] > 0:
                namehisUnixTime['time_between'] = str(nhutdate[0]) + 'y ' + str(nhutdate[1]) + 'd ' + str(nhutdate[2]) + 'h ' + str(nhutdate[3]) + 'm'
            elif nhutdate[0] == 0:
                namehisUnixTime['time_between'] = str(nhutdate[1]) + 'd ' + str(nhutdate[2]) + 'h ' + str(nhutdate[3]) + 'm'

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
            True
        namehis[0]['time_between'] = ''

        # Switches position of columns
        value = 1
        for i in namehis:
            i['num'] = value
            value += 1
            i['name'] = i.pop('name')
            i['changed_to_at'] = i.pop('changed_to_at')
            i['time_between'] = i.pop('time_between')
        namehis[0]['changed_to_at'] = ''
        namehisrev = namehis.reverse()
        #key_list = list(namehis.keys())
        #val_list = list(namehis.values())

############################################################################ RANK ############################################################################
        rankParsed = ''
        rankcolor = 'darkgray'
        changerbc = False
        rankUnparsed = ''
        pluscolor = 'red'

        # Checks for MVP++
        try:
            rank = reqAPI['player']['newPackageRank']
        except:
            rank = ''
        
        # Very inefficiently checks for VIP / VIP+ / MVP / MVP+ / MVP++
        try:
            MVPplusplus = reqAPI['player']['monthlyPackageRank']
        except:
            MVPplusplus = 'NONE'            
        if MVPplusplus == 'SUPERSTAR':
            rankParsed = '[MVP++]'
            rankcolor = 'gold'
            try:
                pluscolor = reqAPI['player']['rankPlusColor'].lower()
            except: pass
        elif rank == 'MVP_PLUS': 
            rankParsed = '[MVP+]'
            rankcolor = 'mvpaqua'
            try:
                pluscolor = reqAPI['player']['rankPlusColor'].lower()
            except: pass
        elif rank == 'MVP': 
            rankParsed = '[MVP]'
            rankcolor = 'mvpaqua'
        elif rank == 'VIP_PLUS': 
            rankParsed = '[VIP+]'
            rankcolor = 'lime'
            pluscolor = 'gold'
        elif rank == 'VIP':
            rankParsed = '[VIP]'
            rankcolor = 'lime'
        else:
            rankParsed = ''
        rankUnparsed = rank
        
        if rankParsed !='[MVP++]':
            # Checks for normal ranks for PACKAGERANKers
            try:
                ranke = reqAPI['player']['packageRank']
                if ranke == 'MVP_PLUS': 
                    rankParsed = '[MVP+]'
                    rankcolor = 'mvpaqua'
                    try:
                        pluscolor = reqAPI['player']['rankPlusColor'].lower()
                    except: pass
                elif ranke == 'MVP': 
                    rankParsed = '[MVP]'
                    rankcolor = 'aqua'
                elif ranke == 'VIP_PLUS': 
                    rankParsed = '[VIP+]'
                    rankcolor = 'lime'
                    pluscolor = 'gold'
                elif ranke == 'VIP':
                    rankParsed = '[VIP]'
                    rankcolor = 'lime'
                else:
                    rankParsed = ''
                rankUnparsed = ranke
                
            except:
                pass
            
            # Checks for normal ranks for NEWPACKAGERANKers
            try:
                rankw = reqAPI['player']['newPackageRank']
                if rankw == 'MVP_PLUS': 
                    rankParsed = '[MVP+]'
                    rankcolor = 'mvpaqua'
                    try:
                        pluscolor = reqAPI['player']['rankPlusColor'].lower()
                    except: pass
                elif rankw == 'MVP': 
                    rankParsed = '[MVP]'
                    rankcolor = 'mvpaqua'
                elif rankw == 'VIP_PLUS': 
                    rankParsed = '[VIP+]'
                    rankcolor = 'lime'
                    pluscolor = 'gold'
                elif rankw == 'VIP':
                    rankParsed = '[VIP]'
                    rankcolor = 'lime'
                else:
                    rankParsed = ''
                rankUnparsed = rankw
            except:
                True

        # Looks for YOUTUBE rank and other ranks categorized under 'player' > 'rank'
        try:
            jona = reqAPI['player']['rank']
            if '[' not in jona:
                rankParsed = '[' + jona + ']'
            else:
                rankParsed = jona

            if 'MODERATOR' in rankParsed:
                rankcolor = 'dark_green'
            elif 'YOUTUBE' in rankParsed:
                changerbc = True
            elif 'HELPER' in rankParsed:
                rankcolor = 'blue'
            elif 'ADMIN' in rankParsed:
                rankcolor = 'red'
            elif 'BUILD' in rankParsed:
                rankcolor = 'cyan'
            else:
                rankParsed = ''
        except:
            True
        
        # Format rank if not 'normal' includes Admin
        try:
            rankParsed = re.sub("[§a-z1-9]+", '', reqAPI['player']['prefix'])
            if 'OWNER' in rankParsed:
                rankcolor = 'red'
            if 'MOJANG' in rankParsed or 'EVENTS' in rankParsed:
                rankcolor = 'gold'
            if 'SLOTH' in rankParsed:
                rankcolor = 'red'
            if 'PIG' in rankParsed or 'BETA TESTER' in rankParsed:
                rankcolor = 'pink'
        except:
            True
        
        # Only works for YouTube rank right now
        if changerbc:
            rankbracketcolor = 'red'
            rankcolor = 'darkgray'
        else:
            rankbracketcolor = rankcolor
        
        try:
            if reqAPI['player']['monthlyRankColor'] == 'AQUA':
                rankcolor = 'mvpaqua'
        except: pass

############################################################################ NETWORK LEVEL & XP ############################################################################
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

############################################################################ FIRST & LAST LOGINS ############################################################################
        firstLogin = ''
        playedOnHypixel = True
        lastSession = False

        # Last login
        try:
            lastLoginUnix = int(reqAPI['player']['lastLogin']/1000)
            lastLogoutUnix = reqAPI['player']['lastLogout']/1000
        except:
            lastLoginUnix = 1
            lastLogoutUnix = 1
        lastLogin = datetime.fromtimestamp(lastLoginUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')

        # Last logout
        lastLogout = datetime.fromtimestamp(lastLogoutUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')
            
        # First login
        try:
            firstLoginUnix = int(reqAPI['player']['firstLogin']/1000)
        except:
            firstLoginUnix = 1
            playedOnHypixel = False
        
        # Last session
        try:
            if lastLoginUnix < lastLogoutUnix: lastSession = time.strftime("%Hh %Mm %Ss",time.gmtime(lastLogoutUnix-lastLoginUnix))
        except: pass
        
        # If played on Hypixel before, changes the user's 2nd time_between to between the first name change and their first log-on to Hypixel
        if playedOnHypixel == True:
            firstLogin = datetime.fromtimestamp(firstLoginUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')
            nhut3unix = nhut2unix/1000 - firstLoginUnix
            jon = sec2format(nhut3unix)
            if jon[0] > 0:
                namehis[len(namehis)-1]['time_between'] = '>' + str(jon[0]) + 'y ' + str(jon[1]) + 'd ' + str(jon[2]) + 'h ' + str(jon[3]) + 'm'
            elif nhutdate[0] == 0:
                namehis[len(namehis)-1]['time_between'] = '>' + str(jon[1]) + 'd ' + str(jon[2]) + 'h ' + str(jon[3]) + 'm'
            if jon[0] > 10:
                namehis[len(namehis)-1]['time_between'] = ''
        else:
            namehis[len(namehis)-1]['time_between'] = ''
        namehisDiffe = namehis[len(namehis)-2]['time_between']
        
        # Converts from sec2format list to readable Yy Dd Hh Mm
        try:
            nhutdate3 = [0,0,0,0]
            nhutdate3[0] = math.floor(nhut2ndindex / 31536000)
            nhutdate3[1] = math.floor(nhut2ndindex / 86400) - nhutdate3[0] * 365
            nhutdate3[2] = math.floor(nhut2ndindex / 3600) - nhutdate3[1] * 24 - nhutdate3[0] * 365 * 24
            nhutdate3[3] = math.floor(nhut2ndindex / 60) -nhutdate3[2] * 60 - nhutdate3[1] * 24 * 60 - nhutdate3[0] * 365 * 24 * 60
        except:
            nhutdate3=[0,0,0,0]

        namehis[0]['time_between'] = nhutdate3

        # Takes in nhutdate3 and puts values in dict
        try:
            if nhutdate3[0] > 0:
                namehisUnixTime['time_between'] = str(nhutdate3[0]) + 'y ' + str(nhutdate3[1]) + 'd ' + str(nhutdate3[2]) + 'h ' + str(nhutdate3[3]) + 'm'
            elif nhutdate3[0] == 0:
                namehisUnixTime['time_between'] = str(nhutdate3[1]) + 'd ' + str(nhutdate3[2]) + 'h ' + str(nhutdate3[3]) + 'm'
            if nhutdate3 == [0,0,0,0]:
                namehisUnixTime['time_between'] = ''
        except:
            True

############################################################################ QUESTS, AP, & ACHIEVEMENTS ############################################################################
        try:
            achievements = len(reqAPI['player']['achievements'])+len(reqAPI['player']['achievementsOneTime'])
            achievements = format(achievements, ',')
        except:
            achievements = 0
        try:
            achpot = reqAPI['player']['achievementPoints']
            achpot = format(achpot, ',')
        except:
            achpot = 0
        
        quests = 0
        try:
            for j in reqAPI['player']['quests']:
                try:
                    quests += len(reqAPI['player']['quests'][j]['completions'])
                except:
                    pass
            quests = format(quests, ',')
        except:
            pass

############################################################################ TITLE ############################################################################

        joinedAgo = 0
        joinedAgoText = ''
        seniorityTimeTuple = (0, 8895953, 20301357, 34924098, 53671752, 77707908, 108524398, 148033875, 198688534, 263632309, 346896000)
        seniority = 'Freshie'
        try:
            joinedAgo = time.time() - firstLoginUnix
            joinedAgoText = sec2format(joinedAgo)
            if joinedAgoText[0] == 0: joinedAgoText = str(joinedAgoText[1]) + 'd ' + str(joinedAgoText[2]) + 'h ' + str(joinedAgoText[3]) + 'm'
            else: joinedAgoText = str(joinedAgoText[0]) + 'y ' + str(joinedAgoText[1]) + 'd ' + str(joinedAgoText[2]) + 'h ' + str(joinedAgoText[3]) + 'm'
            if joinedAgo < 8895953: seniority = '☘ Hypixel Newcomer'
            elif joinedAgo < 20301357: seniority = '☘ Hypixel Rookie'
            elif joinedAgo < 34924098: seniority = '➴ Hypixel Novice'
            elif joinedAgo < 53671752: seniority = '⚝ Hypixel Trainee'
            elif joinedAgo < 77707908: seniority = '⚜ Hypixel Expert'
            elif joinedAgo < 108524398: seniority = '➴ Hypixel Professional'
            elif joinedAgo < 148033875: seniority = '❖ Hypixel Elder'
            elif joinedAgo < 198688534: seniority = '♗ Hypixel Veteran'
            elif joinedAgo < 263632309: seniority = '♛ Hypixel Master'
            elif joinedAgo < 346896000: seniority = '♆ Hypixel Ancient'
        except: pass

        boughtPastRank = 0
        boughtPastTime = 0
        rankUnparsed2 = 0
        rankunparsedcolor = ''
        try:
            if rankUnparsed != 0:
                boughtPastRank = sec2format(time.time() - reqAPI['player']['levelUp_' + rankUnparsed]/1000)
                if boughtPastRank[0] != 0: boughtPastRank = str(boughtPastRank[0]) + 'y ' + str(boughtPastRank[1]) + 'd ' + str(boughtPastRank[2]) + 'h ' + str(boughtPastRank[3]) + 'm'
                else: boughtPastRank = str(boughtPastRank[1]) + 'd ' + str(boughtPastRank[2]) + 'h ' + str(boughtPastRank[3]) + 'm'
                boughtPastTimeUnix = reqAPI['player']['levelUp_' + rankUnparsed]/1000
                boughtPastTime = datetime.fromtimestamp(boughtPastTimeUnix).strftime('%b %d, %Y at %I:%M %p %z')
                if 'MVP_PLUS' in rankUnparsed: 
                    rankunparsedcolor = 'mvpaqua'
                    rankUnparsed2 = 'MVP+'
                elif rankUnparsed == 'MVP':
                    rankunparsedcolor = 'mvpaqua'
                    rankUnparsed2 = 'MVP'
                elif rankUnparsed == 'VIP_PLUS':
                    rankunparsedcolor ='lime'
                    rankUnparsed2 = 'VIP+'
                elif rankUnparsed == 'VIP':
                    rankunparsedcolor = 'lime'
                    rankUnparsed2 = 'VIP'
                else: pass
            else: boughtPastRank = 0
        except: pass

############################################################################ PLAYER SESSION DATA ##########################################################################################
        reqAPIsess = requests.get('https://api.hypixel.net/status?key=' + HAPIKEY + '&uuid=' + uuid)
        reqAPIsession = reqAPIsess.json()
        currentSession = ''
        sessionType = ''
        if reqAPIsession['success']:
            if reqAPIsession['session']['online'] == True:
                currentSession = reqAPIsession['session']['gameType'].replace('_',' ').upper()
                sessionType = reqAPIsession['session']['mode'].replace('_',' ').title()
            else: currentSession = False

############################################################################ SOCIALS ##########################################################################################
 
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

############################################################################ SKYWARS ##########################################################################################s
        
        swStatsList = []
        for i in range(33):
            swStatsList.append(0)
        # 0 - games played
        # 1 - games quit
        # 2 - kills
        # 3 - deaths
        # 4 - K/D
        # 5 - assists
        # 6 - wins
        # 7 - losses
        # 8 - W/L
        # 9 - survivedPlayers
        # 10 - winstreak
        # 11 - souls
        # 12 - heads count
        # 13 - kills to head tastiness
        # 14 - coins
        # 15 - blocks broken
        # 16 - eggs thrown
        # 17 - arrows shot
        # 18 - arrows hit
        # 19 - fastest win
        # 20 - highest kills in a game
        # 21 - chests opened
        # 22 - win rate
        # 23 - arrow hit rate
        # 24 - KDA
        # 25 - tastiness color
        # 26 - K/W
        # 27 - K/L
        # 28 - K/G
        # 29 - blocks per game
        # 30 - eggs per game
        # 31 - arrow shots per game

        swExpList = []
        # 0 - experience
        # 1 - level
        # 2 - prestige
        # 3 - next level
        # 4 - XP until next level

        # Adds 0 - 9 on swStatsList
        try:
            swgames = reqAPI['player']['stats']['SkyWars']['losses'] + reqAPI['player']['stats']['SkyWars']['wins']
            swStatsList[0]=swgames
            swStatsList[1]=reqAPI['player']['stats']['SkyWars']['quits']

            swkills = reqAPI['player']['stats']['SkyWars']['kills']
            swStatsList[2]=swkills
            swdeaths = reqAPI['player']['stats']['SkyWars']['deaths']
            swStatsList[3]=swdeaths
            swStatsList[4]=(round(swkills/swdeaths, 4))
            swassists = reqAPI['player']['stats']['SkyWars']['assists']
            swStatsList[5]=swassists

            swwins = reqAPI['player']['stats']['SkyWars']['wins']
            swStatsList[6]=swwins
            swlosses = reqAPI['player']['stats']['SkyWars']['losses']
            swStatsList[7]=swlosses
            swStatsList[8]=round(reqAPI['player']['stats']['SkyWars']['wins']/reqAPI['player']['stats']['SkyWars']['losses'],4)
            swStatsList[9]=reqAPI['player']['stats']['SkyWars']['survived_players']
        except: pass

        # Adds 10 - 12 on swStatsList
        try:
            swStatsList[10]=(format(reqAPI['player']['stats']['SkyWars']['win_streak'], ','))
            swStatsList[11]=(format(reqAPI['player']['stats']['SkyWars']['souls_gathered'], ','))
            swStatsList[12]=(format(reqAPI['player']['stats']['SkyWars']['heads'], ','))
        except: pass

        # Adds 13 on swStatsList
        jesushchrist = False
        try:
            if swkills <= 49: swStatsList[13]=('Eww!')
            if swkills > 49 and swkills < 200: swStatsList[13]=('Yucky!')
            if swkills > 199 and swkills < 500: swStatsList[13]=('Meh.')
            if swkills > 499 and swkills < 1000: swStatsList[13]=('Decent...')
            if swkills > 999 and swkills < 2000: swStatsList[13]=('Salty.')
            if swkills > 1999 and swkills < 5000: swStatsList[13]=('Tasty!')
            if swkills > 4999 and swkills < 10000: swStatsList[13]=('Succulent!')
            if swkills > 9999 and swkills < 25000: swStatsList[13]=('Divine!')
            if swkills > 25000: swStatsList[13]=('Heavenly..!')
            if swkills <= 10000 and rankParsed in sweetHeadsRanks: swStatsList[13]=('Sweet!')
        except: swStatsList[13]='Eww!'

        def minsec(seconds):
            return str(math.floor(seconds / 60)) + 'm ' + str(seconds % 60) + 's'

        # Adds 14 - 23 on swStatsList
        try:
            swStatsList[14]=(format(reqAPI['player']['stats']['SkyWars']['coins'], ','))
            swStatsList[15]=(format(reqAPI['player']['stats']['SkyWars']['blocks_broken'], ','))
            swStatsList[16]=(format(reqAPI['player']['stats']['SkyWars']['egg_thrown'], ','))
            swStatsList[17]=(format(reqAPI['player']['stats']['SkyWars']['arrows_shot'], ','))
            swStatsList[18]=(format(reqAPI['player']['stats']['SkyWars']['arrows_hit'], ','))
            swStatsList[19]=(minsec(reqAPI['player']['stats']['SkyWars']['fastest_win']))
            swStatsList[20]=(format(max(reqAPI['player']['stats']['SkyWars']['most_kills_game'], reqAPI['player']['stats']['SkyWars']['most_kills_game_team'], reqAPI['player']['stats']['SkyWars']['most_kills_game_solo']), ','))
            swStatsList[21]=(format(reqAPI['player']['stats']['SkyWars']['chests_opened'], ','))
            swStatsList[22]=(str(round((reqAPI['player']['stats']['SkyWars']['wins']/(reqAPI['player']['stats']['SkyWars']['wins']+reqAPI['player']['stats']['SkyWars']['losses'])) * 100, 4)))
            swStatsList[23]=(str(round(reqAPI['player']['stats']['SkyWars']['arrows_hit']/(reqAPI['player']['stats']['SkyWars']['arrows_hit']+reqAPI['player']['stats']['SkyWars']['arrows_shot'])*100, 4)))
        except: pass

        # Adds 24 - 25 on swStatsList
        twenty4plus = False
        try:
            swStatsList[24]=(round((swkills+reqAPI['player']['stats']['SkyWars']['assists'])/reqAPI['player']['stats']['SkyWars']['deaths'], 4))
            if 'Eww' in swStatsList[13]: swStatsList[25]=('darkgray')
            if 'Yucky' in swStatsList[13]: swStatsList[25]=('gray')
            if 'Meh' in swStatsList[13]: swStatsList[25]=('lightgray')
            if 'Decent' in swStatsList[13]: swStatsList[25]=('decentyellow')
            if 'Salty' in swStatsList[13]: swStatsList[25]=('green')
            if 'Tasty' in swStatsList[13]: swStatsList[25]=('cyan')
            if 'Succulent' in swStatsList[13]: swStatsList[25]=('pink')
            if 'Divine' in swStatsList[13]: swStatsList[25]=('gold')
            if 'Heavenly' in swStatsList[13]: swStatsList[25]=('chocolate')
        except: swStatsList[25]='darkgray'

        # Add 26 - 31 on swStatsList
        try:
            swStatsList[26]=(round(swkills/swwins, 4))
            swStatsList[27]=(round(swkills/swlosses, 4))
            swStatsList[28]=(round(swkills/swgames, 4))
            swStatsList[29]=(round(reqAPI['player']['stats']['SkyWars']['blocks_broken']/swgames, 4))
            swStatsList[30]=(round(reqAPI['player']['stats']['SkyWars']['egg_thrown']/swgames, 4))
            swStatsList[31]=(round(reqAPI['player']['stats']['SkyWars']['arrows_shot']/swgames, 4))
        except: pass
    

        # Function that takes in experience and spits out level as a floating point number
        def swexp2level(experience):
            try:
                expertest = 0
                level = 0
                if experience <= 15000:
                    if experience < 20: level = 1 + (experience - 0) / 20 
                    elif experience < 70: level = 2 + (experience - 20) / 50
                    elif experience < 150: level = 3 + (experience - 70) / 80
                    elif experience < 250: level = 4 + (experience - 150) / 100
                    elif experience < 500: level = 5 + (experience - 250) / 250
                    elif experience < 1000: level = 6 + (experience - 500) / 500
                    elif experience < 2000: level = 7 + (experience - 1000) / 1000
                    elif experience < 3500: level = 8 + (experience - 2000) / 2500
                    elif experience < 6000: level = 9 + (experience - 3500) / 4000
                    elif experience < 10000: level = 10 + (experience - 6000) / 5000
                    elif experience < 15000: level = 11 + (experience - 10000) / 10000
                    return level
                elif experience > 14999:
                    expertest = experience - 15000
                    return expertest / 10000 + 12
            except:
                return 0

        # Function that takes in level and spits out prestige and color as a tuple
        def getPrestige(level):
            try:
                if level < 5: return ('No', 'white')
                elif level < 10: return ('Iron', 'lightgray')
                elif level < 15: return ('Gold', 'gold')
                elif level < 20: return ('Diamond', 'turquoise')
                elif level < 25: return ('Emerald', 'chartreuse')
                elif level < 30: return ('Sapphire', 'blue')
                elif level < 35: return ('Ruby', 'firebrick')
                elif level < 40: return ('Crystal', 'hotpink')
                elif level < 45: return ('Opal', 'darkblue')
                elif level < 50: return ('Amethyst', 'indigo')
                elif level >= 50: return ('Rainbow', 'chocolate')
            except:
                return ('No', 'white')

        # Adds 0 - 4 on swExpList
        swExpList = [0,0,0,0,0]
        try:
            swexpee = reqAPI['player']['stats']['SkyWars']['skywars_experience']
        except:
            swexpee = 0
        try:
            swExpList[0]=(format(swexpee, ','))
            swExpList[1]=(swexp2level(swexpee))
            swExpList[2]=(getPrestige(swExpList[1]))
            swExpList[3]=(math.floor(swExpList[1]) + 1)
            swExpList[4]=(round((swExpList[1] - math.floor(swExpList[1])) * 100, 2))
        except: pass

    ########## SkyWars Mode Stats I
        def swModeStats(statsList, gamemoder):
            try:
                swVAR = reqAPI['player']['stats']['SkyWars']
                try:
                    solokd = round(swVAR.get('kills_' + gamemoder,0)/swVAR.get('deaths_'+gamemoder, 1),4)
                except:
                    solokd = 1
                try:
                    solowl = round(swVAR.get('wins_'+gamemoder,0)/swVAR.get('losses_'+gamemoder, 1),4)
                except:
                    solowl = 1
                solowlrelative = [0,0]
                try:
                    solowlrelative[0] = round(solowl-swStatsList[8],4)
                    solowlrelative[1] = round(100*(solowl/swStatsList[8]-1),2)
                except: pass
                solokdrelative = [0,0]
                try:
                    solokdrelative[0] = round(solokd-swStatsList[4],4)
                    solokdrelative[1] = round(100*(solokd/swStatsList[4]-1),2)
                except: pass
                try:
                    statsList["kills"]= [swVAR.get('kills_'+gamemoder,0), round(100*(swVAR.get('kills_'+gamemoder,0)/swkills),2)]
                except: statsList["kills"]=[0,0]
                try:
                    statsList["deaths"]= [swVAR.get('deaths_'+gamemoder, 0), round(100*(swVAR.get('deaths_'+gamemoder, 0)/swdeaths),2)]
                except: statsList["deaths"] = [0,0]
                try:
                    statsList["kd"]= solokd
                except: statsList["kd"] = [0,0]
                try:
                    statsList["assists"]= [swVAR.get('assists_'+gamemoder, 0), round(100*(swVAR.get('assists_'+gamemoder, 0)/swStatsList[5]),2)]
                except: statsList["assists"] = (0,0)
                try:
                    statsList["survived"]= [swVAR.get('survived_players_'+gamemoder,0), round(100*(swVAR.get('survived_players_'+gamemoder,0)/swStatsList[9]),2)]
                except: statsList["survived"] = (0,0)
                try:
                    statsList["games"]= [swVAR.get('wins_'+gamemoder,0) + swVAR.get('losses_'+gamemoder,0), round(100*(swVAR.get('wins_'+gamemoder,0) + swVAR.get('losses_'+gamemoder,0))/swgames,2)]
                except: statsList["games"] = (0,0)
                try:
                    statsList["wins"]= [swVAR.get('wins_'+gamemoder,0), round(100*(swVAR.get('wins_'+gamemoder,0)/swwins),2)]
                except: statsList["wins"] = (0,0)
                try:
                    statsList["losses"]= [swVAR.get('losses_'+gamemoder,0), round(100*(swVAR.get('losses_'+gamemoder,0)/swlosses),2)]
                except: statsList["losses"] = (0,0)
                statsList["wl"]= solowl
                statsList["kit"]= swVAR.get('activeKit_'+gamemoder.upper(),'Default').split('_')[-1].capitalize()
                statsList["fastestwin"]= minsec(swVAR.get('fastest_win_'+gamemoder,0))
                statsList['highkill']= swVAR.get('most_kills_game_'+gamemoder,0)
                statsList['kdrelative']= solokdrelative
                statsList['wlrelative']= solowlrelative
                statsList['winperc']= round(100*(solowl/(1+solowl)), 4)

                if gamemoder == 'team':
                    statsList['kit'] = swVAR.get('activeKit_TEAMS','Default').split('_')[-1].capitalize().replace('-',' ').title()
                
                if gamemoder == 'ranked':
                    if statsList['highkill'] > 3:
                        statsList['highkill'] = 3

            except:
                statsList = {
                "kills": (0,0),
                "deaths": (0,0),
                "kd": 0,
                "assists": (0,0),
                "survived":(0,0),
                "games": (0,0),
                "wins": (0,0),
                "losses": (0,0),
                "wl": 0,
                "kit": "Default",
                "fastestwin": "N/A",
                'highkill': 0,
                'kdrelative': [0,0],
                'wlrelative': [0,0],
                'winperc': 0,
                }
            return statsList
        
        swSoloStatsList = {}
        swTeamStatsList = {}
        swRankedStatsList = {}
        swMegaStatsList = {}
        swSoloStatsList = swModeStats(swSoloStatsList, 'solo')
        swTeamStatsList = swModeStats(swTeamStatsList, 'team')
        swRankedStatsList = swModeStats(swRankedStatsList, 'ranked')
        swMegaStatsList = swModeStats(swMegaStatsList, 'mega')

        # Printing!
        print(swStatsList)
        print(len(swStatsList))

############################################################################ GUILD ############################################################################
        
        # 0 - guild tag
        # 1 - guild name
        # 2 - guild role
        # 3 - guild color

        VVV = requests.get('https://api.hypixel.net/guild?key=' + HAPIKEY + '&player=' + uuid)
        reqGUILD = VVV.json()
        guildList = [0,0,0,0]
        try:
            if reqGUILD['guild'] != 'null':
                guildList[0] = reqGUILD['guild']['tag']
                guildList[1] = reqGUILD['guild']['name']
                for member in reqGUILD['guild']['members']:
                    if member['uuid'] == uuid:
                        guildList[2] = member['rank']
                        break
                try:
                    guildList[3] = reqGUILD['guild']['tagColor'].lower()
                except:
                    guildList[3] = 'darkgray'
        except: pass

############################################################################ RENDERS BASE.HTML ############################################################################
        displayname = username
        if uuid in ADMINS:
            displayname += ' 🍰'
        if uuid in FLOWERS:
            displayname += ' 🌸'
        print(rankParsed)
        print("--- %s seconds ---" % (time.time() - start_time))
        return render_template('base.html', uuid=uuid, username=username, displayname=displayname, hypixelUN=hypixelUN, namehis=namehis, profile='reqAPI', reqList=reqList['karma'], achpot=achpot, achievements=achievements, level=level, levelProgress=levelProgress, levelplusone=levelplusone, lastLogin=lastLogin, lastLoginUnix=lastLoginUnix, firstLogin=firstLogin, firstLoginUnix=firstLoginUnix, lastLogoutUnix=lastLogoutUnix, lastLogout=lastLogout, lastSession=lastSession, rank=rankParsed.replace('[','').replace(']',''), rankcolor=rankcolor, rankbracketcolor=rankbracketcolor, multiplier=multiplier , swGamesPlayed=swStatsList[0], swGamesQuit=swStatsList[1], swKills=swStatsList[2], swDeaths=swStatsList[3], swKD=swStatsList[4], swAssists=swStatsList[5], swWins=swStatsList[6], swLosses=swStatsList[7], swWL=swStatsList[8], swSurvived=swStatsList[9], swWinstreak=swStatsList[10], swSouls=swStatsList[11], swHeads=swStatsList[12], swHeadDesc=swStatsList[13], swCoins=swStatsList[14], swBlocks=swStatsList[15], swEggs=swStatsList[16], swArrowsShot=swStatsList[17], swArrowsHit=swStatsList[18], swFastestWin=swStatsList[19], swHighestKills=swStatsList[20], swChestsOpened=swStatsList[21], swWinRate=swStatsList[22], swArrowRate=swStatsList[23], swKDA=swStatsList[24], swHeadColor=swStatsList[25], swKW=swStatsList[26], swKL=swStatsList[27], swKG=swStatsList[28], swBPG=swStatsList[29], swEPG=swStatsList[30], swAPG=swStatsList[31], swExp=swExpList[0], swLevel=math.floor(swExpList[1]), swPrestige=swExpList[2][0], swPrestigeColor=swExpList[2][1], swNextLevel=swExpList[3], swToNL=swExpList[4], joinedAgoText=joinedAgoText, seniority=seniority, boughtPastRank=boughtPastRank, quests=quests, currentSession=currentSession, sessionType=sessionType, boughtPastTime=boughtPastTime, rankUnparsed=rankUnparsed2, rankunparsedcolor=rankunparsedcolor, twitter=twitter, instagram=instagram, twitch=twitch, discord=discord, hypixelForums=hypixelForums, youtube=youtube, pluscolor=pluscolor, guildList=guildList, gamemodes={'Solo':swSoloStatsList,'Teams':swTeamStatsList,'Ranked':swRankedStatsList,'Mega':swMegaStatsList})
    
############################################################################ INVALID USERNAME CHECK ############################################################################
    else:
        if len(q) < 3 or len(q) > 16:
            return "A Minecraft username has to be between 3 and 16 characters (with a few special exceptions), and can only contain alphanumeric characters and underscores."
        for letter in q:
            if letter not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_':
                return 'Username contains invalid characters. A Minecraft username can only contain alphanumeric characters and underscores.'
        for swear in swearList:
            if swear in q:
                return "Username might be blocked by Mojang- username contains one of the following: \nhttps://paste.ee/p/RYo2C. \nIf this is a derivative of the Scunthorpe problem, sorry about that."
        return render_template('user404.html')
        #except:
        #    return "Errored out. Lol"

############################################################################ FRIENDS LIST ###################################################################################

@app.route('/f/<q>', methods=['POST', 'GET'])
@cache.cached(timeout=50)
def friends(q):
    start_time = time.time()
    def uuid2un(uuid):
        session = FuturesSession()
        robbb = session.get('http://sessionserver.mojang.com/session/minecraft/profile/' + uuid)
        response_one = robbb.result()
        return response_one

        #return robbb.json()['name']

    friendUUID = ''
    friendListList = []
    if len(q) == 32 or len(q) == 36:
        q = q.replace('-','')
        try:
            if q == MojangAPI.get_uuid(MojangAPI.get_username(q)):
                username = MojangAPI.get_username(q)
                uuid = q
            else:
                return "That UUID doesn't exist. Try again with a different UUID."
        except:
            return "This UUID doesn't exist. Try again with a different UUID."

    else:
        uuid = MojangAPI.get_uuid(q)
        username = MojangAPI.get_username(MojangAPI.get_uuid(q))

    try:
        r = requests.get('https://api.hypixel.net/friends?key=' + HAPIKEY + '&uuid=' + uuid)
        freqAPI = r.json()
        
        if freqAPI['records'] == ['']:
            return "This person hasn't friended anyone on the Hypixel Network yet!"
        else:
            friendList = freqAPI['records']
            
            for friend in friendList:
                try:
                    if friend['uuidSender'] == uuid:
                        friendListList.append({'name':(friend['uuidReceiver']), 'date':friend['started'], 'initiated':friend['uuidSender'], 'duration':time.time()-friend['started']/1000})
                    elif friend['uuidReceiver'] == uuid:
                        friendListList.append({'name':(friend['uuidSender']), 'date':friend['started'], 'initiated':friend['uuidSender'], 'duration':time.time()-friend['started']/1000})
                except: pass

    except:
        if len(q) < 3 or len(q) > 16:
            return "A Minecraft username has to be between 3 and 16 characters (with a few special exceptions), and can only contain alphanumeric characters and underscores."
        for letter in q:
            if letter not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_':
                return 'Username contains invalid characters. A Minecraft username can only contain alphanumeric characters and underscores.'
        for swear in swearList:
            if swear in q:
                return "Username might be blocked by Mojang- username contains one of the following: \nhttps://paste.ee/p/RYo2C. \nIf this is a derivative of the Scunthorpe problem, sorry about that."
        return render_template('user404.html')
    print("--- %s seconds ---" % (time.time() - start_time))    
    return render_template('friends.html', username=username, uuid=uuid, friendListList=friendListList)

############################################################################ ACTUAL GUILD ###################################################################################

############################################################################ ERROR HANDLING ###################################################################################
@app.errorhandler(404)
def four04(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def four03(e):
    return "You got a 403 error. How, I don't know. Contact me @kofjeko on Twitter."

@app.errorhandler(502)
def five02(e):
    return "Something screwed up with the gateway. Contact me @kofjeko on Twitter."

############################################################################ FLASK INITIALIZATION ############################################################################
if __name__ == "__main__":
    app.run(debug=True)