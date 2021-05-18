
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json

epsraw = np.loadtxt('eps.txt',delimiter=',')
gpsraw = np.loadtxt('gps.txt',delimiter=',')
prsraw = np.loadtxt('prs.txt',delimiter=',')

with open('tmp.txt', 'r') as playersfile :
    players = json.load(playersfile)

# find classes

druidids = []
hunterids = []
mageids = []
paladinids = []
priestids = []
rogueids = []
shamanids = []
warlockids = []
warriorids = []

for player in players :
    if player['class'] == 'druid' :
        druidids.append(player['id'])
    elif player['class'] == 'hunter' :
        hunterids.append(player['id'])
    elif player['class'] == 'mage' :
        mageids.append(player['id'])
    elif player['class'] == 'paladin' :
        paladinids.append(player['id'])
    elif player['class'] == 'priest' :
        priestids.append(player['id'])
    elif player['class'] == 'rogue' :
        rogueids.append(player['id'])
    elif player['class'] == 'shaman' :
        shamanids.append(player['id'])
    elif player['class'] == 'warlock' :
        warlockids.append(player['id'])
    elif player['class'] == 'warrior' :
        warriorids.append(player['id'])

druidprs = []
hunterprs = []
mageprs = []
paladinprs = []
priestprs = []
rogueprs = []
shamanprs = []
warlockprs = []
warriorprs = []

for druidid in druidids :
    subprs = []
    for run in prsraw :
        subprs.append(run[druidid])
    druidprs.append(subprs)

for hunterid in hunterids :
    subprs = []
    for run in prsraw :
        subprs.append(run[hunterid])
    hunterprs.append(subprs)

for mageid in mageids :
    subprs = []
    for run in prsraw :
        subprs.append(run[mageid])
    mageprs.append(subprs)

for paladinid in paladinids :
    subprs = []
    for run in prsraw :
        subprs.append(run[paladinid])
    paladinprs.append(subprs)

for priestid in priestids :
    subprs = []
    for run in prsraw :
        subprs.append(run[priestid])
    priestprs.append(subprs)

for rogueid in rogueids :
    subprs = []
    for run in prsraw :
        subprs.append(run[rogueid])
    rogueprs.append(subprs)

for shamanid in shamanids :
    subprs = []
    for run in prsraw :
        subprs.append(run[shamanid])
    shamanprs.append(subprs)

for warlockid in warlockids :
    subprs = []
    for run in prsraw :
        subprs.append(run[warlockid])
    warlockprs.append(subprs)

for warriorid in warriorids :
    subprs = []
    for run in prsraw :
        subprs.append(run[warriorid])
    warriorprs.append(subprs)

print (hunterprs)

figdruids, ax = plt.subplots()
for prdata in druidprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

fighunters, ax = plt.subplots()
for prdata in hunterprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figmages, ax = plt.subplots()
for prdata in mageprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figpaladins, ax = plt.subplots()
for prdata in paladinprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figpriests, ax = plt.subplots()
for prdata in priestprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figrogues, ax = plt.subplots()
for prdata in rogueprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figshamans, ax = plt.subplots()
for prdata in shamanprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figwarlocks, ax = plt.subplots()
for prdata in warlockprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])

figwarriors, ax = plt.subplots()
for prdata in warriorprs :
    ax.plot(prdata)
    ax.set_ylim([0,10])



figdruids.savefig('./graphics/druids.png')
fighunters.savefig('./graphics/mages.png')
fighunters.savefig('./graphics/hunters.png')
figpaladins.savefig('./graphics/paladins.png')
figpriests.savefig('./graphics/priests.png')
figrogues.savefig('./graphics/rogues.png')
figshamans.savefig('./graphics/shamans.png')
figwarlocks.savefig('./graphics/warlocks.png')
figwarriors.savefig('./graphics/warriors.png')
