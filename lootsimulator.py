
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

playerkeys = ['id','name','class','ep','gp','pr','note']

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
    elif slot in ['1h', 'ranged', 'wand', 'idol', 'totem'] :
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

def numtoclass(key) :
    if key == 0 :
        return 'druid'
    elif key == 1:
        return 'hunter'
    elif key == 2:
        return 'mage'
    elif key == 3:
        return 'paladin'
    elif key == 4:
        return 'priest'
    elif key == 5:
        return 'rogue'
    elif key == 6:
        return 'shaman'
    elif key == 7:
        return 'warlock'
    elif key == 8:
        return 'warrior'

def assignclasses(numbers) :

    it = 0
    player = 0
    while it < len (numbers) : 
        number = numbers[it]
        currentclass = numtoclass(it)
        while number > 0 : 
            
            players[player]['class'] = currentclass

## global constants

epkara = 150        # model parameter, set by user

## data containers

epstart = []
gpstart = []
prstart = []

for player in players : 
    epstart.append(player['ep'])
    gpstart.append(player['gp'])
    prstart.append(player['pr'])

epvector = [epstart]
gpvector = [gpstart]
prvector = [prstart]

print("specify mode: 'auto' or 'manual'")

modeselect = input()

### automatic mode
if modeselect == 'auto' :
    
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
    
        # decay ep and gp
        for player in players :
            player['ep'] *= 0.9
        
        for player in players :
            player['ep'] *= 0.9
    
        # update pr
        for player in players : 
            player['pr'] = player['ep'] / player['gp']
    
        currenteps = []
        currentgps = []
        currentprs = []
    
        for player in players : 
            currenteps.append(player['ep'])
            currentgps.append(player['gp'])
            currentprs.append(player['pr'])
    
        epvector.append(currenteps)
        gpvector.append(currentgps)
        prvector.append(currentprs)

### manual mode
elif modeselect == 'manual' :
    print ('initializing raid setup... \n\nplease provide the number of')
    print ('druids: ')
    ndruid = input()
    print ('hunters: ')
    nhunter = input()
    print ('names')
    nmage = input()
    print ('paladins')
    npaladin = input()
    print ('priests')
    npriest = input()
    print ('rogues')
    nrogue = input()
    print ('shamans')
    nshaman = input()
    print ('warlocks')
    nwarlock = input()
    print ('warriors')
    nwarrior = input()

    classdistribution = [ndruid, nhunter, nmage, npaladin, npriest, nrogue, nshaman, nwarlock, nwarrior]
    nraiders = sum(classdistribution)

    if (nraiders > 25)
         print ('too many raiders provided, exiting')
         break
    
    assignclasses (classdistribution)


    
    print ('you provided')


else : 
    print ('unknown operation mode specified, exiting')





### print data

# print players

fplayers = open('players.txt', 'w+')
fplayers.write(json.dumps(players))

# save ep, gp, pr data

epvector = np.array(epvector)
gpvector = np.array(epvector)
prvector = np.array(epvector)

np.savetxt('eps.txt',epvector,delimiter=',')
np.savetxt('gps.txt',gpvector,delimiter=',')
np.savetxt('prs.txt',prvector,delimiter=',')



