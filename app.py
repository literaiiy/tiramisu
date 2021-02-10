############################################################################ IMPORTING ############################################################################
from flask import Flask, render_template, request, url_for, redirect, flash, session
import json
from mojang import MojangAPI
from flask_wtf import Form
from wtforms import TextField
from datetime import datetime
import requests
import math
from flask_table import Table, Col
import time
import re
from itertools import cycle, islice
from num2words import num2words

############################################################################ INITIALIZATION & CONSTANTS ############################################################################
app = Flask(__name__)
app.secret_key = 'a34w7tfyner9ryhzrbfw7ynhhcdtg78as34'
HAPIKEY = '1e5f6a57-6327-4888-886a-590c39861a6a'
ADMINS = ['35a178c0c37043aea959983223c04de0']
FLOWERS = ['27bcc1547423484683fd811155d8c472']
VERSION = "0.0.1α TEST BUILD"
CODENAME ='Flour'
TIRAMISUDATE = datetime.fromtimestamp(1612589848).strftime('%b %d, %Y')
FLASKVER ='1.1.2'
FLASKVERDATE = datetime.fromtimestamp(1597665600).strftime('%b %d, %Y')
PYTHONVER ='3.7.9'
PYTHONVERDATE = datetime.fromtimestamp(1585915200).strftime('%b %d, %Y')
swearList = ['anal','anus','ass','bastard','bitch','blowjob','blow job','buttplug','clitoris','cock','cunt','dick','dildo','fag','fuck','hell','jizz','nigger','nigga','penis','piss','pussy','scrotum','sex','shit','slut','turd','vagina']

username = ''
uuid = ''

class searchBar():
    query = TextField("Search...")

############################################################################ ROUTING FOR HOMEPAGE ############################################################################
@app.route('/', methods=['POST', 'GET'], defaults={'path':''})
def queryt(path):
    form = searchBar()
    if request.method == 'POST':
        session['req'] = request.form
        if not session['req']['content'] == '':
            return redirect(url_for('compute', q=str(session['req']['content'])))
    return render_template('index.html')

@app.route('/<k>', methods=['POST', 'GET'])
def reddorect(k):
    return redirect(url_for('compute', q=k))

############################################################################ ROUTING FOR SEARCH PAGE ############################################################################
@app.route('/p/<q>', methods=['POST','GET'])
def compute(q):
    #try:
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
        #if q == MojangAPI.get_username(MojangAPI.get_uuid(q)):
        uuid = MojangAPI.get_uuid(q)
        username = MojangAPI.get_username(MojangAPI.get_uuid(q))
        print(uuid)
        #else:
        #    return "false uuid or username or smthing"

    if isinstance(uuid, str):
        print('this is the uuid: ' + uuid)
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
        reqList['karma']=(f'{reqListKarma:,}')
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
        rankcolor = 'gray'
        changerbc = False

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
        elif rank == 'MVP_PLUS': 
            rankParsed = '[MVP+]'
            rankcolor = 'aqua'
        elif rank == 'MVP': 
            rankParsed = '[MVP]'
            rankcolor = 'aqua'
        elif rank == 'VIP_PLUS': 
            rankParsed = '[VIP+]'
            rankcolor = 'lime'
        elif rank == 'VIP':
            rankParsed = '[VIP]'
            rankcolor = 'lime'
        else:
            rankParsed = ''
        try:
            ranke = reqAPI['player']['packageRank']
            if ranke == 'MVP_PLUS': 
                rankParsed = '[MVP+]'
                rankcolor = 'aqua'
            elif ranke == 'MVP': 
                rankParsed = '[MVP]'
                rankcolor = 'aqua'
            elif ranke == 'VIP_PLUS': 
                rankParsed = '[VIP+]'
                rankcolor = 'lime'
            elif ranke == 'VIP':
                rankParsed = '[VIP]'
                rankcolor = 'lime'
            else:
                rankParsed = ''
        except:
            True

        try:
            rankw = reqAPI['player']['newPackageRank']
            if rankw == 'MVP_PLUS': 
                rankParsed = '[MVP+]'
                rankcolor = 'aqua'
            elif rankw == 'MVP': 
                rankParsed = '[MVP]'
                rankcolor = 'aqua'
            elif rankw == 'VIP_PLUS': 
                rankParsed = '[VIP+]'
                rankcolor = 'lime'
            elif rankw == 'VIP':
                rankParsed = '[VIP]'
                rankcolor = 'lime'
            else:
                rankParsed = ''
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
                rankcolor = 'green'
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
            rankcolor = 'gray'
        else:
            rankbracketcolor = rankcolor

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

        # Last login
        try:
            lastLoginUnix = int(reqAPI['player']['lastLogin']/1000)
        except:
            lastLoginUnix = 1
        lastLogin = datetime.fromtimestamp(lastLoginUnix).strftime('%a, %b %d, %Y at %I:%M:%S %p %z')
        
        # First login
        try:
            firstLoginUnix = int(reqAPI['player']['firstLogin']/1000)
        except:
            firstLoginUnix = 1
            playedOnHypixel = False
        
        # If played on Hypixel before, changes the user's 2nd time_between to between the first name change and their first log-on to Hypixel
        if playedOnHypixel == True:
            firstLogin = datetime.fromtimestamp(firstLoginUnix).strftime('%a, %b %d, %Y at %I:%M:%S %p %z')
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
        
        # I don't know what this does, honestly
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
        except:
            achievements = 0
        try:
            achpot = reqAPI['player']['achievementPoints']
        except:
            achpot = 0
        ### END ###
        displayname = username
        if uuid in ADMINS:
            displayname += ' 🍰'
        if uuid in FLOWERS:
            displayname += ' 🌸'

        ### RETURN THE GODDAMN THING ###
        return render_template('base.html', uuid=uuid, username=username, displayname=displayname, hypixelUN=hypixelUN, \
        namehis=namehis, profile='reqAPI',reqList=reqList['karma'], \
        achpot=achpot, achievements=achievements, \
        level=level, levelProgress=levelProgress, levelplusone=levelplusone, \
        lastLogin=lastLogin, lastLoginUnix=lastLoginUnix, firstLogin=firstLogin, firstLoginUnix=firstLoginUnix, \
        version=VERSION, codename=CODENAME, flaskver=FLASKVER, flaskverdate=FLASKVERDATE, pythonver=PYTHONVER, pythonverdate=PYTHONVERDATE, tiramisudate=TIRAMISUDATE, \
        rank=rankParsed.replace('[','').replace(']',''), rankcolor=rankcolor, rankbracketcolor=rankbracketcolor, multiplier=multiplier)
    
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
            

        return "This person doesn't seem to exist. Try again?"
        #except:
        #    return "Errored out. Lol"

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