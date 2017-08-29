# Currentcps
PyPlanet cp tracker app

## Description
Currentcps is an app for [PyPlanet][pyplanet]. It shows the progress of multiple players
on the current track. The players are ordered by their current CP and their time at that
CP.

### Finished players
Players that already finished the track are shown first, but only the fastest 5
finished players are shown. However, each finished player can always see themselves.

### Restart
When a player starts to drive and they haven't reached any CP before, they are shown
with CP 0 and a time of 0:00.000. A player that has already reached a CP before and
decides to restart is shown with the old CP and time until they pass a CP. The same
happens with players that have already finished.

### Spectating
A player is automatically set to spectator mode when they click on a name in the
widget. Of course, the player will be spectating the player they clicked on.
Also, players that enter spectator mode via this or any other method, will be
removed from the current-CP-list. They will be re-added when they start to drive
again.

## Installation
Installation of this app is handled by PyPi. To install it, simply activate your
virtual environment and type
```commandline
pip install -U pyplanet_currentcps
```
The same command can also be used to update the plugin and any dependencies.  
If you have already installed a version from github, you'll have to remove or
rename it.

[pyplanet]: https://github.com/PyPlanet/PyPlanet