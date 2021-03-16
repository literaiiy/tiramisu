############################################################################ IMPORTING ############################################################################
from flask import Flask, render_template, request, url_for, redirect, session
import json
from mojang import MojangAPI
from flask_wtf import Form
from wtforms import TextField
from datetime import datetime
import requests
import math
import time
import re
#from itertools import cycle, islice
#from num2words import num2words
import requests_cache
#from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
#from livereload import Server

############################################################################ INITIALIZATION & CONSTANTS ############################################################################
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

app.secret_key = 'a34w7tfyner9ryhzrbfw7ynhhcdtg78as34'
HAPIKEY = '1e5f6a57-6327-4888-886a-590c39861a6a'
ADMINS = ['35a178c0c37043aea959983223c04de0']
FLOWERS = ['27bcc1547423484683fd811155d8c472']
SPARKLES = ['903100946468408aaf2462365389059c', '35bb69ce904a4380a03ffd55acbc2331', '35a178c0c37043aea959983223c04de0']
PENGUINS = ['cfc42e543d834b4f9f7a23c059783ba5']
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
    gameList = [
        ('Total Players', hs.json()['playerCount']),
        ('🏹 SkyWars', gameCount['SKYWARS']['players']),
        ('🌎 SkyBlock', gameCount['SKYBLOCK']['players']),
        ('️🛌 BedWars', gameCount['BEDWARS']['players']),
        ('⚔️ Duels', gameCount['DUELS']['players']),
        ('🦸 Super Smash Mobs', gameCount['SUPER_SMASH']['players']),
        ('💨 Speed UHC', gameCount['SPEED_UHC']['players']),
        ('🔫 Cops and Crims', gameCount['MCGO']['players']),
        ('🕳️ The Pit', gameCount['PIT']['players']),
        ('🍎 UHC Champions', gameCount['UHC']['players']),
        ('🛠️ Build Battle', gameCount['BUILD_BATTLE']['players']),
        ('🕵️‍♂️ Murder Mystery', gameCount['MURDER_MYSTERY']['players']),
        ('🏇 Warlords', gameCount['BATTLEGROUND']['players']),
        ('🏠 Housing', gameCount['HOUSING']['players']),
        ('🕹️ Arcade', gameCount['ARCADE']['players']),
        ('🗡️ Blitz Survival Games', gameCount['SURVIVAL_GAMES']['players']),
        ('🧱 Mega Walls', gameCount['WALLS3']['players']),
        ('🏗️ Prototype', gameCount['PROTOTYPE']['players']),
        ('💣 TNT Games', gameCount['TNTGAMES']['players']),
        ('Main Lobby', gameCount['MAIN_LOBBY']['players']),
        ('Watching a replay', gameCount['REPLAY']['players']),
        ('In limbo', gameCount['LIMBO']['players']),
        ('Idle', gameCount['IDLE']['players']),
        ('🎉 Party Games', gameCount['ARCADE']['modes']['PARTY']),
        ('🧟 Zombies', gameCount['ARCADE']['modes']['ZOMBIES_DEAD_END'] + gameCount['ARCADE']['modes']['ZOMBIES_ALIEN_ARCADIUM'] + gameCount['ARCADE']['modes']['ZOMBIES_BAD_BLOOD']),
        ('🙈 Hide and Seek', gameCount['ARCADE']['modes']['HIDE_AND_SEEK_PROP_HUNT'] + gameCount['ARCADE']['modes']['HIDE_AND_SEEK_PARTY_POOPER']),
        ('🛩️ Mini Walls', gameCount['ARCADE']['modes']['MINI_WALLS']),
        ('📢 Hypixel Says', gameCount['ARCADE']['modes']['SIMON_SAYS']),
        
    ]
    gameDict = []
    for item in gameList:
        try:
            gameDict.append({'game':item[0],'playerCount':item[1],})
        except:
            gameDict.append({'game':item[0],'playerCount':0,})

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
    print(uuid)
    if isinstance(uuid, str):
        #username = MojangAPI.get_username(uuid)

############################################################################ JSON PARSING ############################################################################

############################################################################ RETRIEVE FROM API & INITIALIZE ############################################################################
        r = requests.Session().get('https://api.hypixel.net/player?key=' + HAPIKEY + '&uuid=' + uuid)
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
        namehispure = MojangAPI.get_name_history(uuid)
        namehisLength = len(namehis)
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
        try:
            sec2format(namehisDiff)
        except:
            pass
        
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
        ###
            try:
                nhut3unix = namehispure[1]['changed_to_at']/1000 - firstLoginUnix
            except: nhut3unix = 0
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

        # Does this serve a purpose?
        # try:	
        #     nhutdate3 = [0,0,0,0]	
        #     nhutdate3[0] = math.floor(nhut2ndindex / 31536000)	
        #     nhutdate3[1] = math.floor(nhut2ndindex / 86400) - nhutdate3[0] * 365	
        #     nhutdate3[2] = math.floor(nhut2ndindex / 3600) - nhutdate3[1] * 24 - nhutdate3[0] * 365 * 24	
        #     nhutdate3[3] = math.floor(nhut2ndindex / 60) -nhutdate3[2] * 60 - nhutdate3[1] * 24 * 60 - nhutdate3[0] * 365 * 24 * 60	
        # except:	
        #     nhutdate3=[0,0,0,0]
        ###

        #else:
         #   namehis[-1]['time_between'] = ''
        if firstLoginUnix > 1357027200:
            namehis[0]['time_between'] = sec2format2ydhms(sec2format(int(time.time())-nhut2unix/1000))
        
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
            joinedAgoText = sec2format2ydhms(sec2format(joinedAgo))
                
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
                boughtPastRank = sec2format2ydhms(sec2format(time.time() - reqAPI['player']['levelUp_' + rankUnparsed]/1000))
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
        reqAPIsess = requests.Session().get('https://api.hypixel.net/status?key=' + HAPIKEY + '&uuid=' + uuid)
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
            swStatsList[14]=int(reqAPI['player']['stats']['SkyWars']['coins'])
            swStatsList[15]=reqAPI['player']['stats']['SkyWars']['blocks_broken']
            swStatsList[16]=reqAPI['player']['stats']['SkyWars']['egg_thrown']
            swStatsList[17]=reqAPI['player']['stats']['SkyWars']['arrows_shot']
            swStatsList[18]=reqAPI['player']['stats']['SkyWars']['arrows_hit']
            swStatsList[19]=(minsec(reqAPI['player']['stats']['SkyWars']['fastest_win']))
            swStatsList[20]=reqAPI['player']['stats']['SkyWars']['most_kills_game']
            swStatsList[21]=reqAPI['player']['stats']['SkyWars']['chests_opened']
            swStatsList[22]=round((reqAPI['player']['stats']['SkyWars']['wins']/(reqAPI['player']['stats']['SkyWars']['wins']+reqAPI['player']['stats']['SkyWars']['losses'])) * 100, 4)
            swStatsList[23]=round(reqAPI['player']['stats']['SkyWars']['arrows_hit']/reqAPI['player']['stats']['SkyWars']['arrows_shot']*100, 4)
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
            if 'Sweet' in swStatsList[13]: swStatsList[25]=('dark_purple')
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
                if level < 5: return ('No', 'gray')
                elif level < 10: return ('Iron', 'lightgray')
                elif level < 15: return ('Gold', 'gold')
                elif level < 20: return ('Diamond', 'turquoise')
                elif level < 25: return ('Emerald', 'dark_green')
                elif level < 30: return ('Sapphire', 'blue')
                elif level < 35: return ('Ruby', 'firebrick')
                elif level < 40: return ('Crystal', 'hotpink')
                elif level < 45: return ('Opal', 'darkblue')
                elif level < 50: return ('Amethyst', 'indigo')
                elif level >= 50: return ('Rainbow', 'chocolate')
            except:
                return ('No', 'gray')

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
        swBestGame = [0, False]
        def swModeStats(statsList, gamemoder):
            try:
                swVAR = reqAPI['player']['stats']['SkyWars']
                try:
                    solokd = round(swVAR.get('kills_' + gamemoder,0)/swVAR.get('deaths_'+gamemoder, 0.000001),4)
                except:
                    solokd = [0,0]
                try:
                    solowl = round(swVAR.get('wins_'+gamemoder,0)/swVAR.get('losses_'+gamemoder, 0.000001),4)
                except:
                    solowl = [0,0]
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
                    if statsList['games'][0] > swBestGame[0] and '_' in gamemoder:
                        swBestGame[0] = statsList['games'][0]
                        swBestGame[1] = gamemoder
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
        swLabStatsList = {}
        swSoloStatsList = swModeStats(swSoloStatsList, 'solo')
        swTeamStatsList = swModeStats(swTeamStatsList, 'team')
        swRankedStatsList = swModeStats(swRankedStatsList, 'ranked')
        swMegaStatsList = swModeStats(swMegaStatsList, 'mega')
        swLabStatsList = swModeStats(swMegaStatsList, 'lab')

        swSoloNormal = {}
        swSoloInsane = {}
        swTeamsNormal = {}
        swTeamsInsane = {}
        swMegaDoubles = {}
        swLabSolo = {}
        swLabTeams = {}
        swSoloNormal = swModeStats(swSoloNormal, 'solo_normal')
        swSoloInsane = swModeStats(swSoloInsane, 'solo_insane')
        swTeamsNormal = swModeStats(swTeamsNormal, 'team_normal')
        swTeamsInsane = swModeStats(swTeamsInsane, 'team_insane')
        swMegaDoubles = swModeStats(swMegaDoubles, 'mega_doubles')
        swLabSolo = swModeStats(swLabSolo, 'lab_solo')
        swLabTeams = swModeStats(swLabTeams, 'lab_team')

        ########## SkyWars Kill Types
        swKillTypeList = {}
        swKTLList = []
        for killType in ['melee', 'void', 'bow', 'mob', 'fall']:
            try:
                swKillTypeList[killType] = (reqAPI['player']['stats']['SkyWars'][killType + '_kills'], round(100*(reqAPI['player']['stats']['SkyWars'][killType + '_kills']/swStatsList[2]), 2))
                swKillTypeList['success'] = True
                swKTLList.append(swKillTypeList[killType][0])
            except:
                swKillTypeList[killType] = (0, 0)

        ########## Time Wasted
        try:
            TIMEOVERALL = reqAPI['player']['stats']['SkyWars']['time_played']-reqAPI['player']['stats']['SkyWars']['time_played_mega_doubles']+reqAPI['player']['stats']['SkyWars']['time_played_lab']
        except:
            TIMEOVERALL = 0
        try:
            swPercPlayedLife = round(100*TIMEOVERALL/(time.time()-firstLoginUnix),4)
        except: swPercPlayedLife = 0
        swTimeList = []
        swTimeListPerc = []
        swTimeModeList = ['Solo', 'Teams', 'Mega', 'Ranked', 'Laboratory']
        for mode in ['_solo', '_team','_mega','_ranked','_lab']:
            try:
                timePlayedForThisMode = reqAPI['player']['stats']['SkyWars']['time_played'+mode]
                swTimeList.append(sec2format2ydhms(sec2format(timePlayedForThisMode)))
                swTimeListPerc.append(round(100*(timePlayedForThisMode/TIMEOVERALL), 2))
            except:
                swTimeList.append(0)
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
                    swKperList.append((round(swStatsList[2]/TIMEOVERALL * kw[1],4), kw[0]))
                else:
                    swKperList.append((round(swStatsList[2]/TIMEOVERALL * kw[1],2), kw[0]))
            except: swKperList.append((0, kw[0]))

            try:
                if kw[0] == 'second' or kw[0] == 'minute':
                    swWperList.append((round(swStatsList[6]/TIMEOVERALL * kw[1],4), kw[0]))
                else:
                    swWperList.append((round(swStatsList[6]/TIMEOVERALL * kw[1],2), kw[0]))
            except: swWperList.append((0, kw[0]))

        # Souls
        swSoulList = []
        try:
            SWVARSOULS = reqAPI['player']['stats']['SkyWars']
        except: pass
        try:
            swSoulList.append((SWVARSOULS['souls'], ' total souls'))
        except: swSoulList.append((0, ' total souls'))
        try:
            swSoulList.append((SWVARSOULS['souls_gathered'], ' souls harvested'))
        except: swSoulList.append((0, ' souls harvested'))
        try:
            swSoulList.append((SWVARSOULS['paid_souls'], ' souls bought'))
        except: swSoulList.append((0, ' souls bought'))
        try:
            swSoulList.append((SWVARSOULS['souls_gathered_lab'], ' souls from lab modes'))
        except: swSoulList.append((0, ' souls from lab modes'))
        try:
            swSoulList.append((swSoulList[1][0]-swSoulList[3][0], ' souls from non-lab modes'))
        except: swSoulList.append((0, ' souls from non-lab modes'))
        try:
            swSoulList.append((SWVARSOULS['soul_well_legendaries'], ' legendaries', 'gold'))
        except: swSoulList.append((0, ' legendaries', 'gold'))
        try:
            swSoulList.append((SWVARSOULS['soul_well_rares'], ' rares', 'blue'))
        except: swSoulList.append((0, ' rares', 'blue'))
        try:
            swSoulList.append((SWVARSOULS['soul_well']-SWVARSOULS['soul_well_legendaries']-SWVARSOULS['soul_well_rares'], ' commons', 'green'))
        except: swSoulList.append((0, ' commons', 'green'))
        try:
            swSoulList.append((SWVARSOULS['soul_well'], ' soul well uses'))
        except: swSoulList.append((0, ' soul well uses',))

        swSoulsRaritiesList = [swSoulList[-2][0], swSoulList[-3][0], swSoulList[-4][0]]

        # Heads
        #headCollection = reqAPI['player']['stats']['SkyWars']['head_collection']['prestigious']
        try:
            swHEADVAR = reqAPI['player']['stats']['SkyWars']
        except: pass
        swHeads = []
        swHeadsSolo = []
        swHeadsTeam = []

        for x in [('eww','darkgray'),('yucky','gray'),('meh','lightgray'),('decent','decentyellow'),('salty','green'),('tasty','cyan'),('succulent','pink'), ('sweet','dark_purple'), ('divine','gold'),('heavenly','chocolate')]:
            try:
                swHeads.append([x[0].capitalize(), swHEADVAR['heads_'+x[0]], x[1], round(100*swHEADVAR['heads_'+x[0]]/int(swStatsList[12]),2)])
            except: swHeads.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsSolo.append([x[0].capitalize(), swHEADVAR['heads_'+x[0]+'_solo'], x[1], round(100*swHEADVAR['heads_'+x[0]+'_solo']/int(swStatsList[12]),2)])
            except: swHeadsSolo.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsTeam.append([x[0].capitalize(), swHEADVAR['heads_'+x[0]+'_team'], x[1], round(100*swHEADVAR['heads_'+x[0]+'_team']/int(swStatsList[12]),2)])
            except: swHeadsTeam.append([x[0].capitalize(), 0, x[1], 0])
        
        swHeads.reverse()
        swHeadsSolo.reverse()
        swHeadsTeam.reverse()

        # Angel's Descent
        try:
            swADVAR = reqAPI['player']['stats']['SkyWars']
        except: pass
        swOpals = {}
        try:
            swOpals['opals'] = swADVAR['opals']
        except: swOpals['opals'] = 0
        try:
            swOpals['shards'] = swADVAR['shard']
            swOpals['until next opal'] = swOpals['shards'] % 20000
            swOpals['shardsTilNextPerc'] = round(100*swOpals['until next opal']/20000,2)
            swOpals['shardsTilNextPrBa'] = int(32*(swOpals['shardsTilNextPerc']/100))
        except:
            swOpals['shards'] = 0
            swOpals['until next opal'] = 0
            swOpals['shardsTilNextPerc'] = 0
            swOpals['shardsTilNextPrBa'] = 0
        try:
            swOpals['opals from prestige'] = int(swExpList[1]/5)
        except: swOpals['opals from prestige'] = 0
        try:
            swOpals['shard_solo'] = swADVAR['shard_solo']
            swOpals['shard_solo_perc'] = round(100*swOpals['shard_solo']/swOpals['shards'],2)
        except:
            swOpals['shard_solo'] =0
            swOpals['shard_solo_perc'] = 0
        try:
            swOpals['shard_team'] = swADVAR['shard_team']
            swOpals['shard_team_perc'] = round(100*swOpals['shard_team']/swOpals['shards'],2)
        except: 
            swOpals['shard_team'] = 0
            swOpals['shard_team_perc'] = 0
        try:
            swOpals['shards per kill'] = round(swOpals['shards']/int(swStatsList[2]),2)
        except: swOpals['shards per kill'] = 0
        try:
            swOpals['shards per game'] = round(swOpals['shards']/int(swStatsList[0]),2)
        except: swOpals['shards per game'] = 0

        ########## Printing!
        #print(swStatsList)
        #print(len(swStatsList))

############################################################################ BEDWARS ############################################################################

        bwOverallStats = {}
        try:
            bwSTATVAR = reqAPI['player']['stats']['Bedwars']
        except: pass

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
            ]

        # Add through iteration
        for item in bwStatsChooseList:
            try:
                bwOverallStats[item] = bwSTATVAR[item]
            except:
                bwOverallStats[item] = 0

        # Add 4 criss cross final kill death crap, W/L, and B/L
        for x in [['K/D','kills_bedwars','deaths_bedwars'], ['finK/D','final_kills_bedwars','final_deaths_bedwars'], ['K/FD', 'kills_bedwars', 'final_deaths_bedwars'], ['FK/D', 'final_kills_bedwars', 'deaths_bedwars'], ['W/L', 'wins_bedwars', 'losses_bedwars'], ['B/L', 'beds_broken_bedwars', 'beds_lost_bedwars']]:
            try:
                bwOverallStats[x[0]] = round(bwOverallStats[x[1]]/bwOverallStats[x[2]],4)
            except ZeroDivisionError:
                if bwOverallStats[x[1]] == bwOverallStats[x[2]]:
                    bwOverallStats[x[0]] = 0
                else: bwOverallStats[x[0]] = float('inf')
            except:
                bwOverallStats[x[0]] = 0
        
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
        #bwOverallStats['level'].append(bwOverallStats['level'][0]+1)

        # Prestige
        def lvl2prestige(level):
            try:
                if level < 100: return ('No', 'gray', round(100*(level-math.floor(level)),2))
                elif level < 200: return ('Iron', 'lightgray', round(100*(level-math.floor(level)),2))
                elif level < 300: return ('Gold', 'gold', round(100*(level-math.floor(level)),2))
                elif level < 400: return ('Diamond', 'turquoise', round(100*(level-math.floor(level)),2))
                elif level < 500: return ('Emerald', 'dark_green', round(100*(level-math.floor(level)),2))
                elif level < 600: return ('Sapphire', 'cyan', round(100*(level-math.floor(level)),2))
                elif level < 700: return ('Ruby', 'firebrick', round(100*(level-math.floor(level)),2))
                elif level < 800: return ('Crystal', 'hotpink', round(100*(level-math.floor(level)),2))
                elif level < 900: return ('Opal', 'darkblue', round(100*(level-math.floor(level)),2))
                elif level < 1000: return ('Amethyst', 'indigo', round(100*(level-math.floor(level)),2))
                elif level >= 1000: return ('Rainbow', 'chocolate', round(100*(level-math.floor(level)),2))
            except:
                return ('No', 'gray')

        bwOverallStats['prestige'] = lvl2prestige(bwOverallStats['level'])
        #bwOverallStats['prestige'].append(lvl2prestige(bwOverallStats['level'][1]))
        bwOverallStats['level'] = math.floor(bwOverallStats['level'])
        print(bwOverallStats['prestige'])

############################################################################ GUILD ############################################################################
        
        # 0 - guild tag
        # 1 - guild name
        # 2 - guild role
        # 3 - guild color

        VVV = requests.Session().get('https://api.hypixel.net/guild?key=' + HAPIKEY + '&player=' + uuid)
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
        if uuid in SPARKLES:
            displayname += ' ✨'
        if uuid in PENGUINS:
            displayname += ' 🐧'
        #print(rankParsed)
        print("--- %s seconds ---" % (time.time() - start_time))
        return render_template('base.html', uuid=uuid, username=username, displayname=displayname, hypixelUN=hypixelUN, namehis=namehis, profile='reqAPI', reqList=reqList['karma'], achpot=achpot, achievements=achievements, level=level, levelProgress=levelProgress, levelplusone=levelplusone, lastLogin=lastLogin, lastLoginUnix=lastLoginUnix, firstLogin=firstLogin, firstLoginUnix=firstLoginUnix, lastLogoutUnix=lastLogoutUnix, lastLogout=lastLogout, lastSession=lastSession, rank=rankParsed.replace('[','').replace(']',''), rankcolor=rankcolor, rankbracketcolor=rankbracketcolor, multiplier=multiplier , swGamesPlayed=swStatsList[0], swGamesQuit=swStatsList[1], swKills=swStatsList[2], swDeaths=swStatsList[3], swKD=swStatsList[4], swAssists=swStatsList[5], swWins=swStatsList[6], swLosses=swStatsList[7], swWL=swStatsList[8], swSurvived=swStatsList[9], swWinstreak=swStatsList[10], swSouls=swStatsList[11], swHeads=swStatsList[12], swHeadDesc=swStatsList[13], swCoins=swStatsList[14], swBlocks=swStatsList[15], swEggs=swStatsList[16], swArrowsShot=swStatsList[17], swArrowsHit=swStatsList[18], swFastestWin=swStatsList[19], swHighestKills=swStatsList[20], swChestsOpened=swStatsList[21], swWinRate=swStatsList[22], swArrowRate=swStatsList[23], swKDA=swStatsList[24], swHeadColor=swStatsList[25], swKW=swStatsList[26], swKL=swStatsList[27], swKG=swStatsList[28], swBPG=swStatsList[29], swEPG=swStatsList[30], swAPG=swStatsList[31], swExp=swExpList[0], swLevel=math.floor(swExpList[1]), swPrestige=swExpList[2][0], swPrestigeColor=swExpList[2][1], swNextLevel=swExpList[3], swToNL=swExpList[4], joinedAgoText=joinedAgoText, seniority=seniority, boughtPastRank=boughtPastRank, quests=quests, currentSession=currentSession, sessionType=sessionType, boughtPastTime=boughtPastTime, rankUnparsed=rankUnparsed2, rankunparsedcolor=rankunparsedcolor, twitter=twitter, instagram=instagram, twitch=twitch, discord=discord, hypixelForums=hypixelForums, youtube=youtube, pluscolor=pluscolor, guildList=guildList, gamemodes={'Solo':swSoloStatsList,'Teams':swTeamStatsList,'Ranked':swRankedStatsList,'Mega':swMegaStatsList, 'Laboratory':swLabStatsList},gamemodes2={'Solo Normal':swSoloNormal, 'Solo Insane':swSoloInsane, 'Teams Normal':swTeamsNormal, 'Teams Insane':swTeamsInsane, 'Mega Doubles':swMegaDoubles, 'Laboratory Solo':swLabSolo, 'Laboratory Teams':swLabTeams}, swKillTypeList=swKillTypeList, swKTLList=json.dumps(swKTLList), swTimeLists=[swTimeList, swTimeListPerc], swTimeModeList=swTimeModeList, swTimeListPercMinusOverall=swTimeListPercMinusOverall, swUnitConvList=swUnitConvList, swUnitConvList2=swUnitConvList2, swSoulList=swSoulList, swSoulsRaritiesList=swSoulsRaritiesList, swHeadsListList=(swHeads,swHeadsSolo,swHeadsTeam), swHeadsRaw=[swHeads[0][1],swHeads[1][1],swHeads[2][1],swHeads[3][1],swHeads[4][1],swHeads[5][1],swHeads[6][1],swHeads[7][1],swHeads[8][1],swHeads[9][1]], swHeadsRawSolo=[swHeadsSolo[0][1],swHeadsSolo[1][1],swHeadsSolo[2][1],swHeadsSolo[3][1],swHeadsSolo[4][1],swHeadsSolo[5][1],swHeadsSolo[6][1],swHeadsSolo[7][1],swHeadsSolo[8][1],swHeadsSolo[9][1]], swHeadsRawTeam=[swHeadsTeam[0][1],swHeadsTeam[1][1],swHeadsTeam[2][1],swHeadsTeam[3][1],swHeadsTeam[4][1],swHeadsTeam[5][1],swHeadsTeam[6][1],swHeadsTeam[7][1],swHeadsTeam[8][1],swHeadsTeam[9][1]], swKWperLists=(swKperList, swWperList, swPercPlayedLife), swOpals=swOpals, swBestGame = swBestGame, bwOverallStats=bwOverallStats)
    
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
        r = requests.Session().get('https://api.hypixel.net/friends?key=' + HAPIKEY + '&uuid=' + uuid)
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
    return "You got a 403 error. How, I don't know. Contact me on Twitter."

@app.errorhandler(502)
def five02(e):
    return "Something screwed up with the gateway. Contact me on Twitter."

############################################################################ FLASK INITIALIZATION ############################################################################
if __name__ == "__main__":
    app.run(debug=True)
    # server = Server(app.wsgi_app)
    # server.serve()