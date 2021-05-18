
# script for running a raid loot simulation, calculate EPGP and generating data pased on this

from os import system

print ('starting simulation')

system('python3 lootsimulator.py')

print ('executing data visualization procedures')

system ('python3 datavisuals.py')

print('all done, have a good day dear user!')

