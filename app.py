############################################################################ IMPORTING ############################################################################
from flask import Flask, render_template, request, url_for, redirect, session
import json
from mojang import MojangAPI
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

requests_cache.install_cache('test_cache', backend='sqlite', expire_after=30)

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

# requests_cache.install_cache('demo_cache', expire_after=3)
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
    # applesauce = MojangAPI.get_uuid(q)
    # print(applesauce)
    # return applesauce + ' <- UUID'
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
        username = MojangAPI.get_username(uuid)

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

############################################################################ RANK ############################################################################
       
        # Get from slothpixel.me API
        rankson = requests.Session().get('https://api.slothpixel.me/api/players/' + uuid)
        rankjson = rankson.json()

        # Set defaults
        rankNoPlus = ''
        rankPlusses = ''
        rankColorParsed = 'white'
        plusColorParsed = 'white'
        originalRank = rankjson['rank'] if 'rank' in rankjson else ''
        # If they have a rank, extract the non-plus section, the plusses, and the colors of each
        if 'rank_formatted' in rankjson:
            rankformattable = rankjson['rank_formatted']
            
            # Translate list for rank colors
            rankColorList = {
                '0':'black',
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
            
            # Strips all the crap off of rank_formatted (API) ex. &d[MVP&6+&d] into MVP
            rankParsed = re.sub('[a-z&0-9\[\]]','',rankformattable) if 'rank_formatted' in rankjson else ''

            # Gets no-plus and plus-only versions of rankParsed
            rankNoPlus = rankParsed.replace('+','')
            rankPlusses = re.sub('[A-Z]','',rankParsed)

            # Gets color code for player's rank
            rankColor = re.sub('[A-Z&+\[\]]','',rankformattable)

            # Sets rankColorParsed and plusColorParsed to the translated rank color
            rankColorParsed = rankColorList[rankColor[0]]
            if len(rankColor) > 1: plusColorParsed = rankColorList[rankColor[1]]
            print(rankNoPlus)
            print(rankColorParsed)
            print(plusColorParsed)

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
        
        # Last session
        try:
            if lastLoginUnix < lastLogoutUnix: lastSession = sec2format2ydhms(sec2format(lastLogoutUnix-lastLoginUnix))
        except: pass
        
        # If played on Hypixel before, changes the user's 2nd time_between to between the first name change and their first log-on to Hypixel
        if playedOnHypixel:
            firstLogin = datetime.fromtimestamp(firstLoginUnix).strftime('%a, %b %d, %Y at %I:%M %p %z')
        ###
            try:
                nhut3unix = namehispure[1]['changed_to_at']/1000 - firstLoginUnix
            except: nhut3unix = 0
            jon = sec2format(nhut3unix)
            if jon[0] > 0:	
                namehis[-1]['time_between'] = '>' + str(jon[0]) + 'y ' + str(jon[1]) + 'd ' + str(jon[2]) + 'h ' + str(jon[3]) + 'm'	
            elif nhutdate[0] == 0:	
                namehis[-1]['time_between'] = '>' + str(jon[1]) + 'd ' + str(jon[2]) + 'h ' + str(jon[3]) + 'm'	
            if jon[0] > 10:	
                namehis[-1]['time_between'] = ''	
        else:	
            namehis[-1]['time_between'] = ''
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
        currentSession = False
        sessionType = ''
        if playedOnHypixel:
            reqAPIsess = requests.Session().get('https://api.hypixel.net/status?key=' + HAPIKEY + '&uuid=' + uuid)
            reqAPIsession = reqAPIsess.json()
            if reqAPIsession['success']:
                if reqAPIsession['session']['online']:
                    if reqAPIsession['session']['gameType'] == 'SKYWARS': currentSession = 'SkyWars'
                    elif reqAPIsession['session']['gameType'] == 'SKYBLOCK': currentSession = 'SkyBlock'
                    elif reqAPIsession['session']['gameType'] == 'BEDWARS': currentSession = 'BedWars'
                    elif reqAPIsession['session']['gameType'] == 'SUPER_SMASH': currentSession = 'Smash Heroes'
                    elif reqAPIsession['session']['gameType'] == 'SPEED_UHC': currentSession = 'Speed UHC'
                    elif reqAPIsession['session']['gameType'] == 'MCGO': currentSession = 'Cops and Crims'
                    elif reqAPIsession['session']['gameType'] == 'PIT': currentSession = 'The Pit'
                    elif reqAPIsession['session']['gameType'] == 'UHC': currentSession = 'UHC Champions'
                    elif reqAPIsession['session']['gameType'] == 'BATTLEGROUND': currentSession = 'Warlords'
                    elif reqAPIsession['session']['gameType'] == 'SURVIVAL_GAMES': currentSession = 'Blitz Survival Games'
                    elif reqAPIsession['session']['gameType'] == 'WALLS3': currentSession = 'Mega Walls'
                    elif reqAPIsession['session']['gameType'] == 'TNTGAMES': currentSession = 'TNT Games'
                    else: currentSession = reqAPIsession['session']['gameType'].replace('_',' ').title()
                    try:
                        sessionType = reqAPIsession['session']['mode'].replace('_',' ').title()
                    except:
                        sessionType = 'somewhere...'

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
            'chests_opened':0,
            'refill_chest_destroy':0,
            'cosmetic_tokens':0,
            'skywars_experience':0,
        }

        swUnscannedDict = {
            'head_tastiness':('Eww!', 'darkgray'),
            'level':1,
            'prestige':('No','gray'),
            'xpRemainder':20,
            'winsRemainder':2,
            'presIcon':'☆',
        }

        if 'games' in swSTATSVAR:
            swExpList = []
            # 0 - experience
            # 1 - level
            # 2 - prestige
            # 3 - next level
            # 4 - XP until next level

            # Get the automatable ones
            for x in swStatsDict.keys():
                if x in swSTATSVAR: swStatsDict[x] = swSTATSVAR[x] 
            
            # Fastest win formatting
            if isinstance(swStatsDict['fastest_win'], int): swStatsDict['fastest_win'] = sec2format2ydhms(sec2format(swStatsDict['fastest_win']))

            # Games played, K/D, W/L
            swStatsDict['games_played'] = swStatsDict['wins'] + swStatsDict['losses']
            swStatsDict['K/D'] = round(swStatsDict['kills']/swStatsDict['deaths'],4) if swStatsDict['deaths'] != 0 else float('inf')
            swStatsDict['W/L'] = round(swStatsDict['wins']/swStatsDict['losses'],4) if swStatsDict['deaths'] != 0 else float('inf')

            # Head tastiness
            if rankNoPlus in sweetHeadsRanks and swStatsDict['kills'] < 10000: swStatsDict['head_tastiness'] = ('Sweet!', 'aqua')
            elif swStatsDict['kills'] < 49: swStatsDict['head_tastiness'] = ('Eww!', 'darkgray')
            elif swStatsDict['kills'] < 200: swStatsDict['head_tastiness'] = ('Yucky!', 'gray')
            elif swStatsDict['kills'] < 500: swStatsDict['head_tastiness'] = ('Meh.','lightgray')
            elif swStatsDict['kills'] < 1000: swStatsDict['head_tastiness'] = ('Decent...','yellow')
            elif swStatsDict['kills'] < 2000: swStatsDict['head_tastiness'] = ('Salty.','lime')
            elif swStatsDict['kills'] < 5000: swStatsDict['head_tastiness'] = ('Tasty!','cyan')
            elif swStatsDict['kills'] < 10000: swStatsDict['head_tastiness'] = ('Succulent!','light_purple')
            elif swStatsDict['kills'] < 25000: swStatsDict['head_tastiness'] = ('Divine!','gold')
            else: swStatsDict['head_tastiness'] = ('Heavenly..!', 'dark_purple')

            # Winrate, arrow hitrate, KDA, K/W, K/L, K/G, blocks/game, eggs/game, arrows/game, pearls/game
            swStatsDict['winrate'] = round(100*swStatsDict['wins']/swStatsDict['games_played'], 2)
            swStatsDict['arrow_hitrate'] = round(100*swStatsDict['arrows_hit']/swStatsDict['arrows_shot'],2)
            swStatsDict['KDA'] = round((swStatsDict['kills']+swStatsDict['assists'])/swStatsDict['deaths'],4)
            swStatsDict['K/W'] = round(swStatsDict['kills']/swStatsDict['wins'],4) if swStatsDict['wins'] != 0 else float('inf')
            swStatsDict['K/L'] = round(swStatsDict['kills']/swStatsDict['losses'],4) if swStatsDict['losses'] != 0 else float('inf')
            swStatsDict['K/G'] = round(swStatsDict['kills']/swStatsDict['games_played'],4) if swStatsDict['games_played'] != 0 else float('inf')
            swStatsDict['blocks_placed_per_game'] = round(swStatsDict['blocks_placed']/swStatsDict['games_played'],4) if swStatsDict['games_played'] != 0 else float('inf')
            swStatsDict['eggs_per_game'] = round(swStatsDict['egg_thrown']/swStatsDict['games_played'],4) if swStatsDict['games_played'] != 0 else float('inf')
            swStatsDict['arrows_per_game'] = round(swStatsDict['arrows_shot']/swStatsDict['games_played'],4) if swStatsDict['games_played'] != 0 else float('inf')
            swStatsDict['pearls_per_game'] = round(swStatsDict['enderpearls_thrown']/swStatsDict['games_played'],4) if swStatsDict['games_played'] != 0 else float('inf')

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
                    elif level < 10: return ('Iron', 'lightgray')
                    elif level < 15: return ('Gold', 'gold')
                    elif level < 20: return ('Diamond', 'aqua')
                    elif level < 25: return ('Emerald', 'dark_green')
                    elif level < 30: return ('Sapphire', 'blue')
                    elif level < 35: return ('Ruby', 'dark_red')
                    elif level < 40: return ('Crystal', 'light_purple')
                    elif level < 45: return ('Opal', 'dark_blue')
                    elif level < 50: return ('Amethyst', 'dark_purple')
                    elif level >= 50: return ('Rainbow', 'chocolate')
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

            # # Adds 0 - 4 on swExpList
            # swExpList = [0,0,0,0,0,'☆']
            # try:
            #     swexpee = swSTATSVAR['skywars_experience']
            # except:
            #     swexpee = 0
            # try:
            #     swExpList[0]=(format(swexpee, ','))
            #     swExpList[1]=(swexp2level(swexpee))
            #     swExpList[2]=(getPrestige(swExpList[1]))
            #     swExpList[3]=(math.floor(swExpList[1]) + 1)
            #     swExpList[4]=(round((swExpList[1] - math.floor(swExpList[1])) * 100, 2))
            #     swExpList[5]=re.sub('[0-9a-zA-Z§]', '', swSTATSVAR['levelFormatted'])
            # except: pass

        else: swStatsDict['success']:False
        #return swStatsDict

        # # Adds 0 - 9 on swStatsList
        # try:
        #     swgames = swSTATSVAR['losses'] + swSTATSVAR['wins']
        #     swStatsList[0]=swgames
        #     swStatsList[1]=swSTATSVAR['quits']

        #     swkills = swSTATSVAR['kills']
        #     swStatsList[2]=swkills
        #     swdeaths = swSTATSVAR['deaths']
        #     swStatsList[3]=swdeaths
        #     swStatsList[4]=(round(swkills/swdeaths, 4))
        #     swassists = swSTATSVAR['assists']
        #     swStatsList[5]=swassists

        #     swwins = swSTATSVAR['wins']
        #     swStatsList[6]=swwins
        #     swlosses = swSTATSVAR['losses']
        #     swStatsList[7]=swlosses
        #     swStatsList[8]=round(swSTATSVAR['wins']/swSTATSVAR['losses'],4)
        #     swStatsList[9]=swSTATSVAR['survived_players']
        # except: pass

        # # Adds 10 - 12 on swStatsList
        # try:
        #     swStatsList[10]=(format(swSTATSVAR['win_streak'], ','))
        #     swStatsList[11]=(format(swSTATSVAR['souls_gathered'], ','))
        #     swStatsList[12]=(format(swSTATSVAR['heads'], ','))
        # except: pass

        # # Adds 13 on swStatsList
        # jesushchrist = False
        # try:
        #     if swkills <= 49: swStatsList[13]=('Eww!')
        #     if swkills > 49 and swkills < 200: swStatsList[13]=('Yucky!')
        #     if swkills > 199 and swkills < 500: swStatsList[13]=('Meh.')
        #     if swkills > 499 and swkills < 1000: swStatsList[13]=('Decent...')
        #     if swkills > 999 and swkills < 2000: swStatsList[13]=('Salty.')
        #     if swkills > 1999 and swkills < 5000: swStatsList[13]=('Tasty!')
        #     if swkills > 4999 and swkills < 10000: swStatsList[13]=('Succulent!')
        #     if swkills > 9999 and swkills < 25000: swStatsList[13]=('Divine!')
        #     if swkills > 25000: swStatsList[13]=('Heavenly..!')
        #     if swkills <= 10000 and rankNoPlus in sweetHeadsRanks: swStatsList[13]=('Sweet!')
        # except: swStatsList[13]='Eww!'

        # # Adds 14 - 23 on swStatsList
        # swStatsList[14]=int(swSTATSVAR['coins'])
        # swStatsList[15]=swSTATSVAR['blocks_broken']
        # swStatsList[16]=swSTATSVAR['egg_thrown']
        # swStatsList[17]=swSTATSVAR['arrows_shot']
        # swStatsList[18]=swSTATSVAR['arrows_hit']
        # swStatsList[19]=sec2format2ydhms(sec2format(swSTATSVAR['fastest_win']))
        # swStatsList[20]=swSTATSVAR['most_kills_game']
        # swStatsList[21]=swSTATSVAR['chests_opened']
        # swStatsList[22]=round((swSTATSVAR['wins']/(swSTATSVAR['wins']+swSTATSVAR['losses'])) * 100, 4)
        # swStatsList[23]=round(swSTATSVAR['arrows_hit']/swSTATSVAR['arrows_shot']*100, 4)

        # # Adds 24 - 25 on swStatsList
        # twenty4plus = False
        # try:
        #     swStatsList[24]=(round((swkills+swSTATSVAR['assists'])/swSTATSVAR['deaths'], 4))
        #     if 'Eww' in swStatsList[13]: swStatsList[25]=('darkgray')
        #     if 'Yucky' in swStatsList[13]: swStatsList[25]=('gray')
        #     if 'Meh' in swStatsList[13]: swStatsList[25]=('lightgray')
        #     if 'Decent' in swStatsList[13]: swStatsList[25]=('decentyellow')
        #     if 'Salty' in swStatsList[13]: swStatsList[25]=('green')
        #     if 'Tasty' in swStatsList[13]: swStatsList[25]=('cyan')
        #     if 'Succulent' in swStatsList[13]: swStatsList[25]=('pink')
        #     if 'Sweet' in swStatsList[13]: swStatsList[25]=('dark_purple')
        #     if 'Divine' in swStatsList[13]: swStatsList[25]=('gold')
        #     if 'Heavenly' in swStatsList[13]: swStatsList[25]=('chocolate')
        # except: swStatsList[25]='darkgray'

        # # Add 26 - 31 on swStatsList
        # try:
        #     swStatsList[26]=(round(swkills/swwins, 4))
        #     swStatsList[27]=(round(swkills/swlosses, 4))
        #     swStatsList[28]=(round(swkills/swgames, 4))
        #     swStatsList[29]=(round(swSTATSVAR['blocks_broken']/swgames, 4))
        #     swStatsList[30]=(round(swSTATSVAR['egg_thrown']/swgames, 4))
        #     swStatsList[31]=(round(swSTATSVAR['arrows_shot']/swgames, 4))
        # except: pass

        ########## SkyWars Mode Stats I
        swBestGame = [0, False]
        def swModeStats(statsList, gamemoder):
            try:
                solokd = round(swSTATSVAR.get('kills_' + gamemoder,0)/swSTATSVAR.get('deaths_'+gamemoder, 0.000001),4)
            except:
                solokd = [0,0]
            try:
                solowl = round(swSTATSVAR.get('wins_'+gamemoder,0)/swSTATSVAR.get('losses_'+gamemoder, 0.000001),4)
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
                statsList["kills"]= [swSTATSVAR.get('kills_'+gamemoder,0), round(100*(swSTATSVAR.get('kills_'+gamemoder,0)/swkills),2)]
            except: statsList["kills"]=[0,0]
            try:
                statsList["deaths"]= [swSTATSVAR.get('deaths_'+gamemoder, 0), round(100*(swSTATSVAR.get('deaths_'+gamemoder, 0)/swdeaths),2)]
            except: statsList["deaths"] = [0,0]
            try:
                statsList["kd"]= solokd
            except: statsList["kd"] = [0,0]
            try:
                statsList["assists"]= [swSTATSVAR.get('assists_'+gamemoder, 0), round(100*(swSTATSVAR.get('assists_'+gamemoder, 0)/swStatsList[5]),2)]
            except: statsList["assists"] = (0,0)
            try:
                statsList["survived"]= [swSTATSVAR.get('survived_players_'+gamemoder,0), round(100*(swSTATSVAR.get('survived_players_'+gamemoder,0)/swStatsList[9]),2)]
            except: statsList["survived"] = (0,0)
            try:
                statsList["games"]= [swSTATSVAR.get('wins_'+gamemoder,0) + swSTATSVAR.get('losses_'+gamemoder,0), round(100*(swSTATSVAR.get('wins_'+gamemoder,0) + swSTATSVAR.get('losses_'+gamemoder,0))/swgames,2)]
                if swStatsDict['games_played'][0] > swBestGame[0] and '_' in gamemoder:
                    swBestGame[0] = statsList['games'][0]
                    swBestGame[1] = gamemoder
            except: statsList["games"] = (0,0)
            try:
                statsList["wins"]= [swSTATSVAR.get('wins_'+gamemoder,0), round(100*(swSTATSVAR.get('wins_'+gamemoder,0)/swwins),2)]
            except: statsList["wins"] = (0,0)
            try:
                statsList["losses"]= [swSTATSVAR.get('losses_'+gamemoder,0), round(100*(swSTATSVAR.get('losses_'+gamemoder,0)/swlosses),2)]
            except: statsList["losses"] = (0,0)
            statsList["wl"]= solowl
            statsList["kit"]= swSTATSVAR.get('activeKit_'+gamemoder.upper(),'Default').split('_')[-1].capitalize()
            statsList["fastestwin"]= sec2format2ydhms(sec2format(swSTATSVAR.get('fastest_win_'+gamemoder,0)))
            statsList['highkill']= swSTATSVAR.get('most_kills_game_'+gamemoder,0)
            statsList['kdrelative']= solokdrelative
            statsList['wlrelative']= solowlrelative
            statsList['winperc']= round(100*(solowl/(1+solowl)), 4)

            if gamemoder == 'team':
                statsList['kit'] = swSTATSVAR.get('activeKit_TEAMS','Default').split('_')[-1].capitalize().replace('-',' ').title()
            
            if gamemoder == 'ranked':
                if statsList['highkill'] > 3:
                    statsList['highkill'] = 3
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
                swKillTypeList[killType] = (swSTATSVAR[killType + '_kills'], round(100*(swSTATSVAR[killType + '_kills']/swStatsList[2]), 2))
                swKillTypeList['success'] = True
                swKTLList.append(swKillTypeList[killType][0])
            except:
                swKillTypeList[killType] = (0, 0)

        ########## Time Wasted
        try:
            TIMEOVERALL = swSTATSVAR['time_played']-swSTATSVAR['time_played_mega_doubles']+swSTATSVAR['time_played_lab']
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
                timePlayedForThisMode = swSTATSVAR['time_played'+mode]
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
            swSoulList.append((swSTATSVAR['souls'], ' total souls'))
        except: swSoulList.append((0, ' total souls'))
        try:
            swSoulList.append((swSTATSVAR['souls_gathered'], ' souls harvested'))
        except: swSoulList.append((0, ' souls harvested'))
        try:
            swSoulList.append((swSTATSVAR['paid_souls'], ' souls bought'))
        except: swSoulList.append((0, ' souls bought'))
        try:
            swSoulList.append((swSTATSVAR['souls_gathered_lab'], ' souls from lab modes'))
        except: swSoulList.append((0, ' souls from lab modes'))
        try:
            swSoulList.append((swSoulList[1][0]-swSoulList[3][0], ' souls from non-lab modes'))
        except: swSoulList.append((0, ' souls from non-lab modes'))
        try:
            swSoulList.append((swSTATSVAR['soul_well_legendaries'], ' legendaries', 'gold'))
        except: swSoulList.append((0, ' legendaries', 'gold'))
        try:
            swSoulList.append((swSTATSVAR['soul_well_rares'], ' rares', 'blue'))
        except: swSoulList.append((0, ' rares', 'blue'))
        try:
            swSoulList.append((swSTATSVAR['soul_well']-swSTATSVAR['soul_well_legendaries']-swSTATSVAR['soul_well_rares'], ' commons', 'green'))
        except: swSoulList.append((0, ' commons', 'green'))
        try:
            swSoulList.append((swSTATSVAR['soul_well'], ' soul well uses'))
        except: swSoulList.append((0, ' soul well uses',))

        swSoulsRaritiesList = [swSoulList[-2][0], swSoulList[-3][0], swSoulList[-4][0]]

        # Heads
        #headCollection = reqAPI['player']['stats']['SkyWars']['head_collection']['prestigious']
        swHeads = []
        swHeadsSolo = []
        swHeadsTeam = []

        for x in [('eww','darkgray'),('yucky','gray'),('meh','lightgray'),('decent','decentyellow'),('salty','green'),('tasty','cyan'),('succulent','pink'), ('sweet','dark_purple'), ('divine','gold'),('heavenly','chocolate')]:
            try:
                swHeads.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]], x[1], round(100*swSTATSVAR['heads_'+x[0]]/int(swStatsList[12]),2)])
            except: swHeads.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsSolo.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]+'_solo'], x[1], round(100*swSTATSVAR['heads_'+x[0]+'_solo']/int(swStatsList[12]),2)])
            except: swHeadsSolo.append([x[0].capitalize(), 0, x[1], 0])
            try:
                swHeadsTeam.append([x[0].capitalize(), swSTATSVAR['heads_'+x[0]+'_team'], x[1], round(100*swSTATSVAR['heads_'+x[0]+'_team']/int(swStatsList[12]),2)])
            except: swHeadsTeam.append([x[0].capitalize(), 0, x[1], 0])
        
        swHeads.reverse()
        swHeadsSolo.reverse()
        swHeadsTeam.reverse()

        # Angel's Descent
        swOpals = {}
        try:
            swOpals['opals'] = swSTATSVAR['opals']
        except: swOpals['opals'] = 0
        try:
            swOpals['shards'] = swSTATSVAR['shard']
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
            swOpals['shard_solo'] = swSTATSVAR['shard_solo']
            swOpals['shard_solo_perc'] = round(100*swOpals['shard_solo']/swOpals['shards'],2)
        except:
            swOpals['shard_solo'] =0
            swOpals['shard_solo_perc'] = 0
        try:
            swOpals['shard_team'] = swSTATSVAR['shard_team']
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
                elif level < 1100: return ('Rainbow', 'chocolate', round(100*(level-math.floor(level)),2))

                elif level < 1200: return ('Iron Prime', 'lightgray', round(100*(level-math.floor(level)),2))
                elif level < 1300: return ('Gold Prime', 'gold', round(100*(level-math.floor(level)),2))
                elif level < 1400: return ('Diamond Prime', 'turquoise', round(100*(level-math.floor(level)),2))
                elif level < 1500: return ('Emerald Prime', 'dark_green', round(100*(level-math.floor(level)),2))
                elif level < 1600: return ('Sapphire Prime', 'cyan', round(100*(level-math.floor(level)),2))
                elif level < 1700: return ('Ruby Prime', 'firebrick', round(100*(level-math.floor(level)),2))
                elif level < 1800: return ('Crystal Prime', 'hotpink', round(100*(level-math.floor(level)),2))
                elif level < 1900: return ('Opal Prime', 'darkblue', round(100*(level-math.floor(level)),2))
                elif level < 2000: return ('Amethyst Prime', 'indigo', round(100*(level-math.floor(level)),2))

                elif level < 2100: return ('Mirror', 'mirror', round(100*(level-math.floor(level)),2))
                elif level < 2200: return ('Light', 'light', round(100*(level-math.floor(level)),2))
                elif level < 2300: return ('Dawn', 'dawn', round(100*(level-math.floor(level)),2))
                elif level < 2400: return ('Dusk', 'dusk', round(100*(level-math.floor(level)),2))
                elif level < 2500: return ('Air', 'air', round(100*(level-math.floor(level)),2))
                elif level < 2600: return ('Wind', 'wind', round(100*(level-math.floor(level)),2))
                elif level < 2700: return ('Nebula', 'nebula', round(100*(level-math.floor(level)),2))
                elif level < 2800: return ('Thunder', 'thunder', round(100*(level-math.floor(level)),2))
                elif level < 2900: return ('Earth', 'earth', round(100*(level-math.floor(level)),2))
                elif level < 3000: return ('Water', 'water', round(100*(level-math.floor(level)),2))
                elif level >= 3000: return ('Fire', 'fire', round(100*(level-math.floor(level)),2))
                #elif level >= 1000: return ('Rainbow', 'chocolate', round(100*(level-math.floor(level)),2))
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
            'four_three':'3s',
            'four_four':'4s',
            'two_four':'4v4',
            'eight_two_armed':'Duos Armed',
            'four_four_armed':'4s Armed',
            'castle':'Castle',
            'eight_one_rush':'Solo Rush',
            'eight_two_rush': 'Duos Rush',
            'four_four_rush': '4s Rush',
            'eight_one_ultimate':'Solo Ultimate',
            'eight_two_ultimate':'Duos Ultimate',
            'four_four_ultimate':'4s Ultimate',
            'eight_two_lucky':'Duos Lucky Block',
            'four_four_lucky': '4s Lucky Block',
            'eight_two_voidless':'Duos Voidless',
            'four_four_voidless':'4s Voidless',
            'tourney_bedwars4s_1':'Tournament (4s)',
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
            try:
                bwModeStats[mode]['K/D'] = round(bwModeStats[mode]['kills_bedwars'][0]/bwModeStats[mode]['deaths_bedwars'][0],4)
            except: bwModeStats[mode]['K/D'] = 0
            try:
                bwModeStats[mode]['finK/D'] = round(bwModeStats[mode]['final_kills_bedwars'][0]/bwModeStats[mode]['final_deaths_bedwars'][0],4)
            except: bwModeStats[mode]['finK/D'] = 0
            try:
                bwModeStats[mode]['K/FD'] = round(bwModeStats[mode]['kills_bedwars'][0]/bwModeStats[mode]['final_deaths_bedwars'][0],4)
            except: bwModeStats[mode]['K/FD'] = 0
            try:
                bwModeStats[mode]['FK/D'] = round(bwModeStats[mode]['final_kills_bedwars'][0]/bwModeStats[mode]['deaths_bedwars'][0],4)
            except: bwModeStats[mode]['FK/D'] = 0

        # Win/loss ratio & winrate
            try:
                bwModeStats[mode]['W/L'] = round(bwModeStats[mode]['wins_bedwars'][0]/bwModeStats[mode]['losses_bedwars'][0],4)
            except: bwModeStats[mode]['W/L'] = 0
            try:
                bwModeStats[mode]['winrate'] = round(100*bwModeStats[mode]['wins_bedwars'][0]/bwModeStats[mode]['games_played_bedwars'][0],2)
            except: bwModeStats[mode]['winrate'] = 0

            # Bed break/lose
            try:
                bwModeStats[mode]['B/L'] = round(bwModeStats[mode]['beds_broken_bedwars'][0]/bwModeStats[mode]['beds_lost_bedwars'][0],4)
            except: bwModeStats[mode]['B/L'] = 0

            # Items and resources per game
            try:
                bwModeStats[mode]['purc/game'] = round(bwModeStats[mode]['_items_purchased_bedwars'][0]/bwModeStats[mode]['games_played_bedwars'][0],4)
            except: bwModeStats[mode]['purc/game'] = 0
            try:
                bwModeStats[mode]['resc/game'] = round(bwModeStats[mode]['resources_collected_bedwars'][0]/bwModeStats[mode]['games_played_bedwars'][0],4)
            except: bwModeStats[mode]['resc/game'] = 0

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
            '🏹 Projectile':'projectile',
            '🌌 Void':'void',
            '🪄 Magic':'magic',
            '🐕 Entity':'entity',
            '🤯 Entity explosion':'entity_explosion',
            '🔥 Fire':'final_tick',
            '👞 Fall damage':'fall',
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
            bwKillsVia['🗡 Melee'] = (bwOverallStats['kills_bedwars'] - bwTakeKillsCount, round(100*(bwOverallStats['kills_bedwars'] - bwTakeKillsCount)/bwOverallStats['kills_bedwars'],2))
            bwPureKillsVia.append(bwKillsVia['🗡 Melee'][0])
        except: 
            bwKillsVia['🗡 Melee'] = (0,0)
            bwPureKillsVia.append(0)

    # Final kills via
        bwFinKillsVia = {
            '🏹 Projectile':'projectile',
            '🌌 Void':'void',
            '🪄 Magic':'magic',
            '🐕 Entity':'entity',
            '🤯 Entity explosion':'entity_explosion',
            '🔥 Fire':'final_tick',
            '👞 Fall damage':'fall',
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
            bwFinKillsVia['🗡 Melee'] = (bwOverallStats['final_kills_bedwars'] - bwTakeFinKillsCount, round(100*(bwOverallStats['final_kills_bedwars'] - bwTakeFinKillsCount)/bwOverallStats['final_kills_bedwars'],2))
            bwPureFinKillsVia.append(bwFinKillsVia['🗡 Melee'][0])
        except: 
            bwFinKillsVia['🗡 Melee'] = (0,0)
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
                bwResColPerc.append(round(100*bwSTATVAR[x+'_resources_collected_bedwars']/bwTotalResources,2))
            else:
                bwResCol.append(0)
        print(bwResCol)
    
    # Cosmetics
        bwCosTranslate = {

        }
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
        print(bwCosmetics)
        # return 'fu'

############################################################################ GUILD ############################################################################

        # 0 - guild tag
        # 1 - guild name
        # 2 - guild role
        # 3 - guild color
        guildList = [0,0,0,0]
        if playedOnHypixel:
            VVV = requests.Session().get('https://api.hypixel.net/guild?key=' + HAPIKEY + '&player=' + uuid)
            reqGUILD = VVV.json()
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

        # Designated Crapification

        return render_template('base.html', uuid=uuid, username=username, displayname=displayname, hypixelUN=hypixelUN, namehis=namehis, profile='reqAPI', reqList=reqList['karma'], achpot=achpot, achievements=achievements, level=level, levelProgress=levelProgress, levelplusone=levelplusone, lastLogin=lastLogin, lastLoginUnix=lastLoginUnix, firstLogin=firstLogin, firstLoginUnix=firstLoginUnix, lastLogoutUnix=lastLogoutUnix, lastLogout=lastLogout, lastSession=lastSession, rank=rankNoPlus, rankPlusses=rankPlusses, originalRank=originalRank, rankColorParsed=rankColorParsed, plusColorParsed=plusColorParsed, multiplier=multiplier, swStatsDict=swStatsDict, swUnscannedDict=swUnscannedDict, joinedAgoText=joinedAgoText, seniority=seniority, boughtPastRank=boughtPastRank, quests=quests, currentSession=currentSession, sessionType=sessionType, boughtPastTime=boughtPastTime, rankUnparsed=rankUnparsed2, rankunparsedcolor=rankunparsedcolor, twitter=twitter, instagram=instagram, twitch=twitch, discord=discord, hypixelForums=hypixelForums, youtube=youtube, pluscolor=plusColorParsed, guildList=guildList, gamemodes={'Solo':swSoloStatsList,'Teams':swTeamStatsList,'Ranked':swRankedStatsList,'Mega':swMegaStatsList, 'Laboratory':swLabStatsList},gamemodes2={'Solo Normal':swSoloNormal, 'Solo Insane':swSoloInsane, 'Teams Normal':swTeamsNormal, 'Teams Insane':swTeamsInsane, 'Mega Doubles':swMegaDoubles, 'Laboratory Solo':swLabSolo, 'Laboratory Teams':swLabTeams}, swKillTypeList=swKillTypeList, swKTLList=json.dumps(swKTLList), swTimeLists=[swTimeList, swTimeListPerc], swTimeModeList=swTimeModeList, swTimeListPercMinusOverall=swTimeListPercMinusOverall, swUnitConvList=swUnitConvList, swUnitConvList2=swUnitConvList2, swSoulList=swSoulList, swSoulsRaritiesList=swSoulsRaritiesList, swHeadsListList=(swHeads,swHeadsSolo,swHeadsTeam), swHeadsRaw=[swHeads[0][1],swHeads[1][1],swHeads[2][1],swHeads[3][1],swHeads[4][1],swHeads[5][1],swHeads[6][1],swHeads[7][1],swHeads[8][1],swHeads[9][1]], swHeadsRawSolo=[swHeadsSolo[0][1],swHeadsSolo[1][1],swHeadsSolo[2][1],swHeadsSolo[3][1],swHeadsSolo[4][1],swHeadsSolo[5][1],swHeadsSolo[6][1],swHeadsSolo[7][1],swHeadsSolo[8][1],swHeadsSolo[9][1]], swHeadsRawTeam=[swHeadsTeam[0][1],swHeadsTeam[1][1],swHeadsTeam[2][1],swHeadsTeam[3][1],swHeadsTeam[4][1],swHeadsTeam[5][1],swHeadsTeam[6][1],swHeadsTeam[7][1],swHeadsTeam[8][1],swHeadsTeam[9][1]], swKWperLists=(swKperList, swWperList, swPercPlayedLife), swOpals=swOpals, swBestGame = swBestGame, bwOverallStats=bwOverallStats, bwModeStats=bwModeStats, bwTranslateList=bwTranslateList, bwCompList=bwCompList, bwMKWList=bwMKWList, bwKillsList=(bwKillsVia, bwKillsPerMode, bwFinKillsVia, bwFinKillsPerMode), bwPureKillsLists=[bwPureKillsVia, bwPureFinKillsVia], bwLootBoxes=bwLootBoxes, bwLootPure=bwLootPure, bwResCol=bwResCol, bwResColPerc=bwResColPerc, bwItemsPurchased=bwItemsPurchased, bwTotalResources=bwTotalResources, bwCosmetics=bwCosmetics)
    
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
    app.run(debug=False)
    # server = Server(app.wsgi_app)
    # server.serve()