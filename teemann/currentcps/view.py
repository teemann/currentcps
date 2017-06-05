import math

from pyplanet.views.generics.widget import TimesWidgetView
from pyplanet.utils import times


class CPWidgetView(TimesWidgetView):
	widget_x = -160
	widget_y = 70.5
	size_x = 38
	size_y = 55.5
	title = 'Current CPs'

	template_name = 'currentcps/cpwidget.xml'

	def __init__(self, app):
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui
		self.id = 'pyplanet__widgets_currentcps'

		self.record_amount = 15

	async def get_player_data(self):
		data = await super().get_player_data()

		# Calculated the maximum number of rows that can be displayed
		max_n = math.floor((self.size_y - 5.5) / 3.3)

		# Maps a logon to the data that should be displayed
		cps = {}

		for player in self.app.instance.player_manager.online:
			list_times = []
			n = 1
			for pcp in self.app.player_cps:
				# Make sure to only display a certain number of entries
				if float(n) >= max_n:
					break

				list_time = {}
				list_time['index'] = n

				# Set time color to green for your own CP time
				list_time['color'] = "$0f3" if player.login == pcp.player.login else "$bbb"

				# Display 'fin' when the player crossed the finish line else display the CP number
				if pcp.cp == -1 or (pcp.cp == 0 and pcp.time != 0):
					list_time['cp'] = 'fin'
				else:
					list_time['cp'] = str(pcp.cp)

				list_time['cptime'] = times.format_time(pcp.time)
				list_time['nickname'] = pcp.player.nickname
				list_times.append(list_time)
				n += 1
			cps[player.login] = {'cps': list_times}

		data.update(cps)

		return data
