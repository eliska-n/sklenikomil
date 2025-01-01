import logging

import asab

L = logging.getLogger(__name__)


class TipsService(asab.Service):

	def __init__(self, app, service_name='TipsService'):
		super().__init__(app, service_name)
		self.GreenhouseService = app.GreenhouseService
		self.StorageService = app.get_service("asab.StorageService")

	async def list_tips(self, greenhouse_id, greenhouse_time):
		greenhouse_tiles = await self.GreenhouseService.get_greenhouse_tiles(greenhouse_id, greenhouse_time)
		tips_by_plants = {}
		for tile in greenhouse_tiles:
			plant_id = tile["plant_id"]
			coll = await self.StorageService.collection("tips")
			cursor = coll.find({
				"plant_id": plant_id,
				"week_from_seed": greenhouse_time - tile["week_planted"]
			})
			if plant_id not in tips_by_plants:
				tips_by_plants[plant_id] = []
			tips_by_plants[plant_id].extend(await cursor.to_list())
		res = [
			{
				"plant_id": plant_id,
				"tips": tips
			}
			for plant_id, tips in tips_by_plants.items()
			if len(tips) > 0
		]
		return res
