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

		web_app.router.add_get('/tips/greenhouse', self.list_elisky_tips)
		web_app.router.add_get('/tips/greenhouse/{greenhouse_id}', self.list_greenhouse_tips)

		web_app.router.add_get('/tips/plant/{plant_id}', self.list_plant_tips)
		web_app.router.add_post('/tips/plant/{plant_id}', self.create_plant_tip)
		web_app.router.add_post('/tips/plant/{plant_id}/{tip_id}', self.update_plant_tip)
		web_app.router.add_delete('/tips/plant/{plant_id}/{tip_id}', self.delete_plant_tip)

	async def list_greenhouse_tips(self, request):
		raise NotImplementedError(":-(")  # TODO

	async def list_elisky_tips(self, request):
		greenhouse_id = "eliska"
		week = request.query.get('week')
		year = request.query.get('year')
		if week is None or year is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "week and year must be provided"}, status=400)
		greenhouse_time = to_greenhouse_time(int(week), int(year))
		tips = await self.TipsService.list_greenhouse_tips(greenhouse_id, greenhouse_time)
		return asab.web.rest.json_response(request, {"result": "OK", "data": tips})

	async def list_plant_tips(self, request):
		plant_id = request.match_info['plant_id']
		tips = await self.TipsService.list_plant_tips(plant_id)
		return asab.web.rest.json_response(request, {"result": "OK", "data": tips})

	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"week_from_seed": {"type": ["integer", "string"]},
			"header": {"type": "string"},
			"text": {"type": "string"},
			"image": {"type": "string"},
			"category": {"type": "string"},
		},
		"required": ["week_from_seed", "header"],
	})
	async def create_plant_tip(self, request, json_data):
		plant_id = request.match_info['plant_id']
		# Convert week_from_seed to integer
		json_data["week_from_seed"] = int(json_data["week_from_seed"])
		await self.TipsService.create_plant_tip(plant_id, json_data)
		return asab.web.rest.json_response(request, {"result": "OK"})


	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"week_from_seed": {"type": ["integer", "string"]},
			"header": {"type": "string"},
			"text": {"type": "string"},
			"image": {"type": "string"},
			"category": {"type": "string"},
		},
		"required": ["week_from_seed", "header"],
	})
	async def update_plant_tip(self, request, json_data):
		plant_id = request.match_info['plant_id']
		tip_id = request.match_info['tip_id']
		# Convert week_from_seed to integer
		json_data["week_from_seed"] = int(json_data["week_from_seed"])
		await self.TipsService.update_plant_tip(plant_id, tip_id, json_data)
		return asab.web.rest.json_response(request, {"result": "OK"})

	async def delete_plant_tip(self, request):
		plant_id = request.match_info['plant_id']
		tip_id = request.match_info['tip_id']
		tip_id = await self.TipsService.delete_plant_tip(plant_id, tip_id)
		return asab.web.rest.json_response(request, {"result": "OK", "tip_id": tip_id})


