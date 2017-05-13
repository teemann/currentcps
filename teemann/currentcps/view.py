import math

from pyplanet.views.generics.widget import WidgetView
from pyplanet.utils import times

class CPWidgetView(WidgetView):
    template_name = 'currentcps/cpwidget.xml'
    widget_x = -162
    widget_y = 55.5
    size_x = 38
    size_y = 55.5

    def __init__(self, app):
        super().__init__(self)
        self.app = app
        self.manager = app.context.ui
        self.id = 'pyplanet__widgets_currentcps'


    async def get_player_data(self):
        data = await super().get_player_data()

        max_n = math.floor((self.size_y - 5.5) / 3.3)

        cps = {}

        for player in self.app.instance.player_manager.online:
            list_times = []
            n = 0
            for pcp in self.app.player_cps:
                if n >= max_n:
                    break
                list_time = {}
                list_time['color'] = "$0f3" if player.login == pcp.player.login else "$bbb"
                if pcp.cp == -1 or (pcp.cp == 0 and pcp.time != 0):
                    list_time['cp'] = 'fin'
                else:
                    list_time['cp'] = str(pcp.cp)
                list_time['cptime'] = times.format_time(pcp.time)
                list_time['nickname'] = pcp.player.nickname
                list_times.append(list_time)
                n = n + 1
            cps[player.login] = {'cps': list_times}
        
        data.update(cps)

        return data

    async def get_context_data(self):
        context = await super().get_context_data()

        context.update({
            'content_pos_x' : 1,
            'content_pos_y': -4.5,
            'cps': None
        })
        return context