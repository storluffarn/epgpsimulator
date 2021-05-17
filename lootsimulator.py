
####################################
### simulating EPGP for karazhan ###
####################################

# code by storluffarn

# get the latest version at 
# github/storluffarn/epgpsimulator


# TODO 
#
# consider making players and items into dicts of dicts


import numpy as np
import random as rn 
import csv
import json 

### common things

## objects

playerkeys = ['id','name','class','ep','gp','pr']

nplayers = 25
players = []

for n in range(nplayers) : 
    player = dict.fromkeys(playerkeys)
    
    player['id'] = n
    player['name'] = 'raider' + str(n)
    player['ep'] = 1
    player['gp'] = 1
    player['pr'] = 1

    players.append(player)

## load loot data

itemkeys = ['id','name','slot','level','droprate']

#attumenraw = np.loadtxt('./attumen.csv',delimiter=',',skiprows=1)

lootfiles = ['./attumen.csv',
'./moroes.csv',
'./maiden.csv',
'./terestian.csv',
'./shadeofaran.csv',
'./netherspite.csv',
'./nightbane.csv',
'./princemalchezaar.csv']

lootdata = []

for lootfile in lootfiles :
    bossloot = []
    with open(lootfile, 'r') as lootfile :
        content = csv.reader(lootfile, delimiter=',')    # use csv reder for multi data type support
        next(content)      # skip header line
        for line in content :
            item = dict.fromkeys(itemkeys)
            item['id'] = int(line[0])
            item['name'] = line[1]
            item['slot'] = line[2]
            item['level'] = int(line[3])
            item['droprate'] = 0.01 * int(line[4])
            
#            print(item)
            bossloot.append(item)

#    print (lootfile)
    lootdata.append(bossloot)
    lootfile.close()

#print (lootdata)

#lootdata = []
#
#for bossdata in lootraw :
#    bossloot = []
#    for data in bossdata :
#    
#        item['id'] = data[0]
#        item['name'] = data[1]
#        item['slot'] = data[2]
#        item['level'] = data[3]
#        item['droprate'] = data[4]
#    
#        bossloot.append(item)
#
#    lootdata.append(bossloot)

#print (lootdata)

#attumenraw = np.loadtxt('./lootattumen.csv',delimiter=',')
#
#attumenloot = [];
#
#for data in attumenraw :
#    item = dict.fromkeys(itemkeys)
#
#    item['id'] = data[0]
#    item['name'] = data[1]
#    item['slot'] = data[2]
#    item['level'] = data[3]
#    item['droprate'] = data[4]
#
#    attumenloot.append(item)
#
#moroesraw = np.loadtxt('./lootmoroes.csv',delimiter=',')
#
#moroesloot = [];
#
#for data in moroesraw :
#    item = dict.fromkeys(keys)
#
#    item['id'] = data[0]
#    item['name'] = data[1]
#    item['slot'] = data[2]
#    item['level'] = data[3]
#    item['droprate'] = data[4]
#
#    moroesloot.append(item)

#lootdata = [attumen]

## functions

def citemval(item) :           # calculate itemvalue
    itemlevel = item['level']
    ival = (itemlevel - 1.3) / 1.3
    return ival

def cslotval(item) :
    
    slot = item['slot']
    sval = 0

    if slot in ['head','chest','legs','2h'] :
        sval = 1
    elif slot in ['shoulder','hands','waist','feet'] :
        sval = 7/9
    elif slot in ['tinkret'] :
        sval = 0.7
    elif slot in ['wrist','neck','back','finger','offhand','shield'] :
        sval = 5/9
    elif slot in ['1h', 'ranged', 'wand'] :
        sval = 0.42

    if sval == 0 :
        print ('error, item value could not be assigned printing last item data and returning 0')
        print (item)

    return sval;

def cgp(item) :             # calculate gear points
    
    ival = citemval(item)
    sval = cslotval(item)

    gp = 0.04 * sval * ival ** 2

    return gp

def generatedrops(bossloot) :
    droprates = []
    for drop in bossloot :
        droprate = drop.get('droprate')
        droprates.append(droprate)

    droprates = np.array(droprates)
    dnorm = sum(droprates)
    droprates = droprates / dnorm
    
    out = np.random.choice(bossloot,2,1,droprates)

    return out

def generatelooters(players) : 
   
    #raiders = []
    prs = []

    for player in players : 
        #get1 = player.get('id')
        get2 = player.get('pr')
        #raiders.append(get1)
        prs.append(get2)
    
    prs = np.array(prs)
    prnorm = sum(prs)
    prs = prs / prnorm

    out = np.random.choice(players,2,0,prs)

    return out

## global constants

epkara = 150        # model parameter, set by user

## data containers

epvector = []
gpvector = []
prvectpr = []

for player in players : 
    epvector.append(player['ep'])
    epvector.append(player['ep'])
    epvector.append(player['ep'])

### automatic mode

runs = 5
cprog = 1.5                 # progress factor
kills = 1
maxkills = 2

for run in range(runs) :     
    
    # generate a progressive random amount of kills
    kills = round(0.5*runs + np.random.normal(0,1))
    if kills < 0 :
        kills = 0
    elif kills > maxkills :
        kills = maxkills
    
    for kill in range(kills) :
        
        # generate drops
        boss = lootdata[kill]
        drops = generatedrops(boss)

        # generate looters
        looters = generatelooters(players)
       
        # distribute loot
        for looter in looters :
            counter = 0
            lootgp = cgp(drops[counter])
            players[looter['id']]['gp'] += lootgp
            counter += 1

        # update ep
        for player in players :
            player['ep'] += epkara

        # update pr
        for player in players : 
            player['pr'] = player['ep'] / player['gp']


#    bossdowns = []
#    
#    for kill in range(kills) :
#        bossdowns.append(1)
#
#    
#    # boss kills
#    if (bossdowns[0] == 1) :        # attumen was killed
#        drop1id = rn.randint(1,len(attumenloot))
#        drop2id = rn.randint(1,len(attumenloot))
#        
#        drop1 = attumenloot[drop1id]
#        drop2 = attumenloot[drop2id]
#        drops = [drop1, drop2]
#
#        # who gets loot
#        looters = autoloot(players)
#
#        # distribute loot
#        for looter in looters :
#            lootgp = cgp(drops[looter])
#            players[looter]['gp'] =+ lootgp
#
#        # update ep
#        for player in players :
#            player['ep'] += epkara
#
#        # update pr
#        for player in players : 
#            player['pr'] = player['ep'] / player['gp']
            
            
    

### manual mode




### print data

# print players

fplayers = open('players.txt', 'w+')
fplayers.write(json.dumps(players))

# save ep, gp, pr data

np.savetxt('ep.txt',epvector,delimiter=',')
np.savetxt('gp.txt',gpvector,delimiter=',')
np.savetxt('pr.txt',prvector,delimiter=',')



