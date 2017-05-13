import logging

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.utils import times
from pyplanet.apps.core.maniaplanet.models.player import Player
from pyplanet.apps.core.maniaplanet.models.player import PlayerFlow
from pyplanet.core.events.callback import Callback
from pyplanet.core.gbx import GbxClient
from pyplanet.utils import times

from .view import CPWidgetView


class CurrentCPs(AppConfig):
    name = 'teemann.current_cps'
    game_dependencies = ['trackmania']
    app_dependencies = ['core.maniaplanet', 'core.trackmania']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_cps = {}
        self.widget = None
        self.player_cps = []
        logging.info("Loaded app CurrentCPs")

    async def on_start(self):
        self.instance.signal_manager.listen(tm_signals.waypoint, self.player_cp)
        self.instance.signal_manager.listen(tm_signals.start_line, self.player_start)
        self.instance.signal_manager.listen(tm_signals.finish, self.player_finish)
        self.instance.signal_manager.listen(mp_signals.player.player_connect, self.player_connect)
        self.instance.signal_manager.listen(mp_signals.player.player_disconnect, self.player_disconnect)
        self.instance.signal_manager.listen(mp_signals.map.map_start__end, self.map_end)

        self.widget = CPWidgetView(self)
        await self.widget.display()

    async def player_cp(self, player, race_time, flow, raw):
        cp = int(raw['checkpointinrace'])
        if not player.login in self.current_cps:
            self.current_cps[player.login] = PlayerCP(player)
        self.current_cps[player.login].cp = cp + 1
        self.current_cps[player.login].time = race_time
        await self.update_view()

    async def player_start(self, time, player, flow):
        if not player.login in self.current_cps:
            self.current_cps[player.login] = PlayerCP(player)
        await self.update_view()

    async def player_finish(self, player, race_time, lap_time, cps, lap_cps, race_cps, flow, is_end_race, is_end_lap, signal, raw):
        if not player.login in self.current_cps:
            self.current_cps[player.login] = PlayerCP(player)
        if(is_end_race):
            self.current_cps[player.login].cp = -1
        else:
            self.current_cps[player.login].cp = race_cps
        self.current_cps[player.login].time = race_time
        await self.update_view()

    async def player_connect(self, signal, player, is_spectator, source):
        await self.update_view()
        await self.widget.display(player=player)
        logging.info("Player connected: " + player.login)

    async def player_disconnect(self, signal, player, reason, source):
        self.current_cps.pop(player.login, None)
        await self.update_view()

    async def map_end(self, time, count, restarted, map):
        self.current_cps.clear()
        await self.update_view()

    async def update_view(self):
        def keyfunc(key):
            pcp = self.current_cps[key]
            return (1 if pcp.cp == -1 else 2, -pcp.cp, pcp.time)

        self.player_cps.clear()
        for login in sorted(self.current_cps, key = lambda x: keyfunc(x)):
            pcp = self.current_cps[login]
            cp = pcp.cp
            cpstr = str(cp)
            if cp == -1:
                cpstr = "fin"
            #logging.info(str(login) + ": " + cpstr)
            self.player_cps.append(pcp)

        await self.widget.display()

class PlayerCP:
    def __init__(self, player):
        self.player = player
        self.cp = 0
        self.time = 0

#TODO: Remove the following code
    def cptime(self):
        return times.format_time(self.time)

    def compare(self, b):
        if self.cp < b.cp:
            return -1
        elif self.cp > b.cp:
            return 1
        else:
            return cmp(self.time, b.time)
