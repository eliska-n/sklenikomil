import logging

import asab
import asab.web
import asab.web.rest

from ..utils import to_greenhouse_time

###

L = logging.getLogger(__name__)

###


class TipsHandler(object):


	def __init__(self, app):
		self.TipsService = app.TipsService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/tips', self.show_elisky_tips)
		web_app.router.add_get('/tips/{greenhouse_id}', self.show_tips)

	async def show_tips(self, request):
		raise NotImplementedError(":-(")  # TODO

	async def show_elisky_tips(self, request):
		greenhouse_id = "eliska"
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"}, status=400)
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		tips = await self.TipsService.list_tips(greenhouse_id, greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": tips})
