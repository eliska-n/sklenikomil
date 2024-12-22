import logging

import asab
import asab.web
import asab.web.rest

###

L = logging.getLogger(__name__)

###


class HerbariumHandler(object):
	def __init__(self, app):
		self.HerbariumService = app.HerbariumService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/herbarium', self.list)
		web_app.router.add_post('/herbarium', self.create_plant)
		web_app.router.add_post('/herbarium/{plant_id}', self.update_plant)
		# web_app.router.add_get('/plant/{plant_id}', self.get_plant)
		# web_app.router.add_get('/plants/', self.list_plants)


	async def list(self, request):
		data = await self.HerbariumService.list()
		return asab.web.rest.json_response(request, {"result": "OK", "data": data})


	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"display_name": {"type": "string"},
			"seed_to_harvest_days": {"type": "integer"},
		},
	})
	async def create_plant(self, request, json_data):
		plant_id = await self.HerbariumService.create_plant(json_data)
		return asab.web.rest.json_response(request, {"result": "OK", "plant_id": plant_id})


	@asab.web.rest.json_schema_handler({
		"type": "object",
		"properties": {
			"display_name": {"type": "string"},
			"seed_to_harvest_days": {"type": "integer"},
		},
	})
	async def update_plant(self, request, json_data):
		plant_id = request.match_info['plant_id']
		plant_id = self.HerbariumService.update_plant(plant_id, json_data)
		return asab.web.rest.json_response(request, {"result": "OK", "plant_id": plant_id})
