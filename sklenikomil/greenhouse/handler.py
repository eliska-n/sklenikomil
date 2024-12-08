import logging

import asab
import asab.web
import asab.web.rest

from ..utils import to_greenhouse_time

###

L = logging.getLogger(__name__)

###


class GreenhouseHandler(object):


	def __init__(self, app):
		self.GreenhosueService = app.GreenhouseService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/greenhouse', self.show_elisky_greenhouse)
		web_app.router.add_put('/greenhouse/{greenhouse_id}', self.show_greenhouse)


	async def show_greenhouse(self, request):
		greenhouse_id = request.match_info['greenhouse_id']
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		selected_week = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhosueService.get_greenhouse(greenhouse_id, selected_week)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})

	async def show_elisky_greenhouse(self, request):
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		selected_week = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhosueService.get_greenhouse("eliska", selected_week)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})
