
####################################
### simulating EPGP for karazhan ###
####################################

# code by storluffarn

# get the latest version at 
# github/storluffarn/epgpsimulator


# TODO 
#
# * consider making players and items into dicts of dicts
# * add a read raid data from file feature
# * fix the error handling during the manual mode menu navigation:
#     * inconsistant messages
#     * no error handling
#     * ugly error handling
# * make automatic mode more realistic
# * make it such that size of player vector is set by raid composition
#


import numpy as np
import random as rn 
import csv
import json 

### common things

## objects

playerkeys = ['id','name','class','note','ep','gp','pr','loot']

nplayers = 25
players = []

for n in range(nplayers) : 
    player = dict.fromkeys(playerkeys)
    
    player['id'] = n
    player['name'] = 'raider' + str(n)
    player['ep'] = 1
    player['gp'] = 1
    player['pr'] = 1
    player['loot'] = []

    players.append(player)

## load loot data

itemkeys = ['id','name','slot','type','level','droprate']

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
            item['type'] = line[3]
            item['level'] = int(line[4])
            item['droprate'] = 0.01 * int(line[5])
            
            bossloot.append(item)

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
    elif slot in ['1h', 'ranged', 'wand', 'relic'] :
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

def numtoboss(key) :
    if key ==  0:
        return 'Attumen the Huntsman'
    elif key ==  1:
        return 'Moroes, Tower Steward'
    elif key ==  2:
        return 'Maiden of Virtue'
    elif key ==  3:
        return 'Terestian Illhoof'
    elif key ==  4:
        return 'Shade of Aran'
    elif key ==  5:
        return 'Netherspite'
    elif key ==  6:
        return 'Nightbane'
    elif key ==  7:
        return 'Prince Malchezaar'

def getgpfactor(key) :
    if key == 1 :
        return 1.0 
    elif key == 2 :
        return 0.8
    elif key == 3 :
        return 0.5
    elif key == 4 :
        return 0.1

def assignclasses(numbers) :

    it = 0
    playerid = 0
    while it < len (numbers) : 
        number = numbers[it]
        currentclass = numtoclass(it)
        while number > 0 : 
            
            players[playerid]['class'] = currentclass
            
            playerid += 1
            number -= 1

        it += 1

def checkint (test) :
    try :
        test = int(test)
        return True
    except ValueError :
        print ('bad data format, expected an integer')
        return False

def checkrange (lower,upper,test) :
   if (test >= lower and test <= upper) :
       return True
   else :
       print ('error: expected {} to be in range {} to {}'.format(test,lower,upper))
       return False

def listplayers () :
    for player in players :
        print (player)

## global constantsi

epkara = 150        # model parameter, set by user
epdecayrate = 0.9
gpdecayrate = epdecayrate

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
    
    runs = 10
    cprog = 2.5                 # progress factor
    kills = 1
    maxkills = 8
    
    bosscounter = 0
    for run in range(runs) :     
        
        # generate a progressive random amount of kills
        kills = round(0.5*runs + np.random.normal(0,1))
        if kills < 0 :
            kills = 0
        elif kills >= maxkills :
            kills = maxkills
        
        for kill in range(kills) :
            
            bosscounter += 1
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
            player['gp'] *= 0.9
    
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

        print (bosscounter)

### manual mode
elif modeselect == 'manual' :
    print ('initializing raid setup... \n\nplease provide the number of')
    print ('druids: ')
    ndruid = int(input())
    print ('hunters: ')
    nhunter = int(input())
    print ('mages: ')
    nmage = int(input())
    print ('paladins: ')
    npaladin = int(input())
    print ('priests: ')
    npriest = int(input())
    print ('rogues: ')
    nrogue = int(input())
    print ('shamans: ')
    nshaman = int(input())
    print ('warlocks: ')
    nwarlock = int(input())
    print ('warriors: ')
    nwarrior = int(input())

    classdistribution = [ndruid, nhunter, nmage, npaladin, npriest, nrogue, nshaman, nwarlock, nwarrior]
    nraiders = sum(classdistribution)

    if (nraiders > 25) :
         print ('too many raiders provided, exiting')
         exit()
    
    assignclasses (classdistribution)

    modswitch = True 
    while modswitch :
        print ("inspect and modify roster (enter 'help' for guidance), enter 'finished' to continue")
        choise = input()
        if choise == 'help' : 
            print ('list of supported functionalities:')
            print ("* enter 'listraid' to print raid composition")
            print ("* enter 'modraid' to modify raid composition")
            print ("\tenter raider-id (0-24) to modify raider, available options are:")
            print ("\t'name'")
            print ("\t'class'")
            print ("\t'ep'")
            print ("\t'gp'")
            print ("\t'pr'")
            print ("\t'note'")
            print ("\texample of suggested usage: set tank status with 'note', or set witty names with 'name' for a more wholesome experience")
            print ("* enter 'finished' to continue")
            print ("please be nice to the script, you will be able to break it if you try to...")
        elif choise == 'listraid' : 
            for player in players : 
                print (player)
        elif choise == 'modraid' :
            choise2 = True
            while choise2 :
                print ("provide raider-id (0-24), please enter 'continue' when finished: ")
                raiderid = input()
                if raiderid == 'continue' :
                    choise2 = False
                    continue 
                
                raiderid = int(raiderid)
                if raiderid >= 0 and raiderid <= 24 :
                
                    print ("what would you like to change ('name','class','ep','gp','pr','note')?")
                    changethis = str(input())
                    print ("current value is: {}, what would you like to change it to?".format(players[raiderid][changethis]))
                    changeto = input()
                    players[raiderid][changethis] = changeto
                    print ("okay, the new value is: {}".format(players[raiderid][changethis]))
                else : 
                    print ('bad raider-id input, exiting')
                    continue

        elif choise == 'finished' :
            modswitch = False
        else : 
            print ("unsupported input, enter 'help' for available commands")
    

    print ('raid composition successful! \ninitiating raid interface...\n')

    raiding = True
    raidcounter = 0
    bosscounter = 0
    while raiding :

        wait = True 
        while wait :
            
            print('new raid started, how many bosses goes down (0 - 8)?')
            bosskills = input()
            if (checkint(bosskills)) :
                bosskills = int(bosskills)
                if (checkrange(0,8,bosskills)) :
                    wait = False
                else : continue
            else : continue
        
        for kill in range(bosskills) :
            
            bosscounter += 1
            bossloot = lootdata[kill]
            drops = generatedrops(bossloot)
            
            bossname = numtoboss(kill)
            print ('\n{} was killed, the loot was:'.format(bossname))
            print ('{} ({} {}) \nand \n{} ({} {})'.format(drops[0]['name'],drops[0]['slot'],drops[0]['type'],drops[1]['name'],drops[1]['slot'],drops[1]['type']))
            
            lootgp1 = cgp(drops[0])
            lootgp2 = cgp(drops[1])
            
            wait = True
            while wait :
                print ("who got {} (enter 'listraid' to see raider info)?".format(drops[0]['name']))
                looterid = input()
                if (looterid == 'listraid') :
                    listplayers()
                if (checkint(looterid)) :
                    looterid = int(looterid)
                    if (checkrange(0,len(players) - 1,looterid)) :
                        print ("what was the EP spending factor ('1': 100%, '2': 80%, '3': 50%, '4': 10%)?")
                        gpchoise = input()
                        if (checkint(gpchoise)) :
                            gpchoise = int(gpchoise)
                            if (checkrange(0,4,gpchoise)) :
                                gpfactor = getgpfactor(gpchoise)
                                players[looterid]['gp'] += gpfactor*lootgp1
                                players[looterid]['loot'].append(drops[0]['name'])
                                wait = False
                            else :
                                continue
                        else :
                            continue
                    else : 
                        continue
                else :
                    continue

            wait = True
            while wait :
                print ("who got {} (enter 'listraid' to see raider info)?".format(drops[1]['name']))
                looterid = input()
                if (looterid == 'listraid') :
                    listplayers()
                if (checkint(looterid)) :
                    looterid = int(looterid)
                    if (checkrange(0,len(players) - 1,looterid)) :
                        print ("what was the EP spending factor ('1': 100%, '2': 80%, '3': 50%, '4': 10%)?")
                        gpchoise = input()
                        if (checkint(gpchoise)) :
                            gpchoise = int(gpchoise)
                            if (checkrange(0,4,gpchoise)) :
                                gpfactor = getgpfactor(gpchoise)
                                players[looterid]['gp'] += gpfactor*lootgp2
                                players[looterid]['loot'].append(drops[1]['name'])
                                wait = False
                            else :
                                continue
                        else :
                            continue
                    else : 
                        continue
                else :
                    continue
           
            # update ep
            for player in players :
                player['ep'] += epkara
    
            # update pr
            for player in players : 
                player['pr'] = player['ep'] / player['gp']

        raidcounter += 1
        print ('raid finished! in total {} raids have been simulated, totaling {} boss kills'.format(raidcounter,bosscounter))
        print ('applying ep and gp decays and updating post-raid pr values...')
    
        # decay ep and gp
        for player in players :
            player['ep'] *= epdecayrate
        
        for player in players :
            player['ep'] *= gpdecayrate
    
        # update pr
        for player in players : 
            player['pr'] = player['ep'] / player['gp']
    
        # save raid progress
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

        print ('do you want to start another raid? (yes/no)')
        restart = input()
        if (restart == 'yes') :
            continue 
        else :
            raiding = False

else : 
    print ('unknown operation mode specified, exiting')
    exit()




### print data

# print players

fplayers = open('players.txt', 'w+')
fplayers.write(json.dumps(players))

# save ep, gp, pr data

epvector = np.array(epvector)
gpvector = np.array(gpvector)
prvector = np.array(prvector)

np.savetxt('eps.txt',epvector,delimiter=',')
np.savetxt('gps.txt',gpvector,delimiter=',')
np.savetxt('prs.txt',prvector,delimiter=',')



