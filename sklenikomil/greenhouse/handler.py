import logging

import asab
import asab.web
import asab.web.rest

from ..utils import to_greenhouse_time
from .service import TileAlreadyPlantedException

###

L = logging.getLogger(__name__)

###


class GreenhouseHandler(object):


	def __init__(self, app):
		self.GreenhouseService = app.GreenhouseService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/greenhouse', self.show_elisky_greenhouse)
		web_app.router.add_get('/greenhouse/{greenhouse_id}', self.show_greenhouse)
		web_app.router.add_put('/greenhouse/create', self.create_greenhouse)  # TODO: create all tiles
		web_app.router.add_post('/greenhouse/plant_new', self.plant_new)
		web_app.router.add_delete('/greenhouse/planted/{planted_id}', self.delete_planted)

	async def show_greenhouse(self, request):
		greenhouse_id = request.match_info['greenhouse_id']
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"}, status=400)
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhouseService.get_greenhouse(greenhouse_id, greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})

	async def show_elisky_greenhouse(self, request):
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"})
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		greenhouse = await self.GreenhouseService.get_greenhouse("eliska", greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": greenhouse})

	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"tile_id": {"type": "integer"},
			"plant_id": {"type": "string"},
			"week": {"type": "integer"},
			"year": {"type": "integer"},
		},
	})
	async def plant_new(self, request, json_data):
		# greenhouse_id = request.match_info['greenhouse_id']
		greenhouse_id = "eliska"
		greenhouse_time = to_greenhouse_time(json_data["week"], json_data["year"])
		try:
			planted = await self.GreenhouseService.plant_new(greenhouse_id, json_data["tile_id"], greenhouse_time, json_data)
		except TileAlreadyPlantedException:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "Tile already planted"}, status=400)
		return asab.web.rest.json_response(request, {"result": "OK", "planted": planted})

	async def create_greenhouse(self, request):
		greenhouse_id = await self.GreenhouseService.create_greenhouse()
		return asab.web.rest.json_response(request, {"result": "OK", "greenhouse_id": greenhouse_id})

	async def delete_planted(self, request):
		planted_id = request.match_info['planted_id']
		await self.GreenhouseService.delete_planted(planted_id)
		return asab.web.rest.json_response(request, {"result": "OK"})
