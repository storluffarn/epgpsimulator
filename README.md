
Overall goal:

Simulate the time evolution of an EPGP system in karazhan. 

Dependencies: 

Python 3.x with packages: numpy, (matplotlib)

Known issues and caveats:

This software is provided as is, and may or may not be updated at www.github.com/storluffarn/epgpsimulator. 

See TODO list in 'lootsimulator.py'.

What the script does:

From a pool of players, a number or raid groups is constructed. Then a number of Karazhan bosses (Huntsman, Steward, Maiden, Terestain, Aran, Netherspite, Nightbane, Malchezaar) are "killed". They drop loot with the same probability that they wold in game (loot data taked from the internet). The loot is then distributed. This process is repeated until a chosen amount of bosses was killed. At which point the program either starts a new raid or terminates. Raid data (ep,gp,pr,drops) is stored in a local file, which may then be visualized using a supplied or by some other means.

Running proces:

At start-up the program will prompt for 'manual' of 'auto' mode. In practice, only 'manual' mode is maintained at this point, 'auto' is mostly used for debugging purposes.

The program will read players from 'tanks.txt', 'healers.txt', 'meleedps.txt', 'rangeddps.txt' and make this the pool of available players. The user can inspect and modify these pre-loaded defaults, but any significant changes should probably be made to the txt-files themselves since it is faster and permament.

The script is now configured to laod 25 players from the files mentioned, and then populate two raids based on the resulting list of players. Each raid will have: 2 tanks, 2 melee dps, 3 ranged dps, and 3 healers.

A raid now starts for the first raid group, and the user is propted to supply how many bosses was killed. After each boss, the loot is manually distributed, and the ep. gp, and pr values are automatically updated. The lot data can be edited through their respective 'bossname.txt' files. After the raid concludes, the process is repeated for the second raid, after which the used is asked whether a new raid (and new seeding) should commence.

