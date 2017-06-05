import logging

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.utils import times

from .view import CPWidgetView


class CurrentCPs(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.current_cps = {}                                           # Maps a player login to a PlayerCP object
		self.widget = None
		self.player_cps = []                                            # Holds the sorted PlayerCP objects (these get displayed by the widget)
		logging.info("Loaded app CurrentCPs")                           # TODO: remove this line

	async def on_start(self):
		# Listen to some signals
		self.instance.signal_manager.listen(tm_signals.waypoint, self.player_cp)
		self.instance.signal_manager.listen(tm_signals.start_line, self.player_start)
		self.instance.signal_manager.listen(tm_signals.finish, self.player_finish)
		self.instance.signal_manager.listen(mp_signals.player.player_connect, self.player_connect)
		self.instance.signal_manager.listen(mp_signals.player.player_disconnect, self.player_disconnect)
		self.instance.signal_manager.listen(mp_signals.map.map_start__end, self.map_end)

		self.widget = CPWidgetView(self)
		await self.widget.display()

	# When a player passes a CP
	async def player_cp(self, player, race_time, flow, raw):
		cp = int(raw['checkpointinrace'])                               # Have to use raw to get the current CP
		if not player.login in self.current_cps:                        # Create new PlayerCP object if there is no PlayerCP object for that player yet
			self.current_cps[player.login] = PlayerCP(player)
		self.current_cps[player.login].cp = cp + 1                      # +1 because checkpointinrace starts at 0
		self.current_cps[player.login].time = race_time
		await self.update_view()

	# When a player starts the race
	async def player_start(self, time, player, flow):
		if not player.login in self.current_cps:
			self.current_cps[player.login] = PlayerCP(player)
		await self.update_view()

	# When a player passes the finish line
	async def player_finish(self, player, race_time, lap_time, cps, lap_cps, race_cps, flow, is_end_race, is_end_lap, signal, raw):
		if not player.login in self.current_cps:                        # Create new PlayerCP object if there is no PlayerCP object for that player yet
			self.current_cps[player.login] = PlayerCP(player)
		if(is_end_race):                                                # Set the current CP to -1 (signals finished) when a player finishes the race
			self.current_cps[player.login].cp = -1
		else:
			self.current_cps[player.login].cp = race_cps                # Otherwise just update the current cp
		self.current_cps[player.login].time = race_time
		await self.update_view()

	# When a player connects
	async def player_connect(self, signal, player, is_spectator, source):
		await self.update_view()
		await self.widget.display(player=player)                        # TODO: Check if this line can be removed
		logging.info("Player connected: " + player.login)

	# When a player disconnects
	async def player_disconnect(self, signal, player, reason, source):
		self.current_cps.pop(player.login, None)                        # Remove the current CP from the widget when a player leaves the server
		await self.update_view()

	# When the map ends
	async def map_end(self, time, count, restarted, map):
		self.current_cps.clear()                                        # Clear the current CPs when the map ends
		await self.update_view()

	# Update the view for all players
	async def update_view(self):
		# Used for sorting the PlayerCP objects by the 1. CP and 2. the time (Finished players are always on top; TODO: might limit these)
		def keyfunc(key):
			pcp = self.current_cps[key]
			return (1 if pcp.cp == -1 else 2, -(pcp.cp), pcp.time)

		self.player_cps.clear()

		# Sort the PlayerCP objects by using the key function above and copy them into the player_cps-list
		for login in sorted(self.current_cps, key = lambda x: keyfunc(x)):
			pcp = self.current_cps[login]
			cp = pcp.cp
			cpstr = str(cp)
			if cp == -1:
				cpstr = "fin"
			#logging.info(str(login) + ": " + cpstr)
			self.player_cps.append(pcp)

		await self.widget.display()                                     # Update the widget for all players


class PlayerCP:
	def __init__(self, player):
		self.player = player
		self.cp = 0
		self.time = 0

	# TODO: Check if the following code can be removed:
	def cptime(self):
		return times.format_time(self.time)

	def compare(self, b):
		if self.cp < b.cp:
			return -1
		elif self.cp > b.cp:
			return 1
		elif self.time < b.time:
			return -1
		elif self.time > b.time:
			return 1
		else:
			return 0
