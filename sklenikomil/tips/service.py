import logging

import asab

L = logging.getLogger(__name__)


class TipsService(asab.Service):

	def __init__(self, app, service_name='TipsService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")
		self.HerbariumService = app.HerbariumService
		self.GreenhouseService = app.GreenhouseService

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
				tips_by_plants[plant_id] = {}
			tips = await cursor.to_list()
			for tip in tips:
				if tip["_id"] not in tips_by_plants[plant_id]:  # Deduplicate tips
					tips_by_plants[plant_id][tip["_id"]] = tip
		res = [
			{
				"plant_id": plant_id,
				"tips": list(tips.values()),
				"plant": await self.HerbariumService.get_plant(plant_id)
			}
			for plant_id, tips in tips_by_plants.items()
			if len(tips) > 0
		]
		return res
