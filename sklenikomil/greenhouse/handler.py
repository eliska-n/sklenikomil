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
		web_app.router.add_get('/greenhouse/{greenhouse_id}', self.show_greenhouse)
		web_app.router.add_put('/greenhouse/create', self.create_greenhouse)  # TODO: create all tiles
		web_app.router.add_post('/greenhouse/plant_new', self.plant_new)

		web_app.router.add_post('/plant/create', self.create_plant)
		# web_app.router.add_post('/plant/{plant_id}', self.update_plant)
		# web_app.router.add_get('/plant/{plant_id}', self.get_plant)
		# web_app.router.add_get('/plants/', self.list_plants)


	async def show_greenhouse(self, request):
		greenhouse_id = request.match_info['greenhouse_id']
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhosueService.get_greenhouse(greenhouse_id, greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})

	async def show_elisky_greenhouse(self, request):
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhosueService.get_greenhouse("eliska", greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})

	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			# "tile_id": {"type": "integer"},
			"plant_id": {"type": "string"},
		},
	})
	async def plant_new(self, request, json_data):
		# greenhouse_id = request.match_info['greenhouse_id']
		greenhouse_id = "eliska"
		week = request.query.get('week')
		year = request.query.get('year')
		tile_id = request.query.get('tile_id')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		selected_week = to_greenhouse_time(int(week), int(year))
		planted = await self.GreenhosueService.plant_new(greenhouse_id, tile_id, selected_week, json_data)
		return asab.web.rest.json_response(request, {"result": "OK", "planted": planted})

	async def create_greenhouse(self, request):
		greenhouse_id = await self.GreenhosueService.create_greenhouse()
		return asab.web.rest.json_response(request, {"result": "OK", "greenhouse_id": greenhouse_id})


	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"display_name": {"type": "string"},
			"seed_to_harvest_days": {"type": "integer"},
		},
	})
	async def create_plant(self, request, json_data):
		plant_id = await self.GreenhosueService.create_plant(json_data)
		return asab.web.rest.json_response(request, {"result": "OK", "plant_id": plant_id})

