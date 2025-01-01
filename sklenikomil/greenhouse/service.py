import logging

import asab

L = logging.getLogger(__name__)


class GreenhouseService(asab.Service):

	def __init__(self, app, service_name='GreenhouseService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")

	async def get_greenhouse(self, greenhouse_id, greenhouse_time):
		greenhouse_tiles = await self.get_greenhouse_tiles(greenhouse_id, greenhouse_time)
		plant_ids = [i["plant_id"] for i in greenhouse_tiles]
		coll_herbarium = await self.StorageService.collection("herbarium")
		cursor_herbarium = coll_herbarium.find({"_id": {"$in": plant_ids}})
		res_herbarium = await cursor_herbarium.to_list()
		herbarium_dict = {herb["_id"]: herb for herb in res_herbarium}
		res = [
			{**plant, **{"plant": herbarium_dict[plant["plant_id"]]}}
			for plant in greenhouse_tiles
			if plant["plant_id"] in herbarium_dict
		]
		return res

	async def get_greenhouse_tiles(self, greenhouse_id, greenhouse_time):
		coll = await self.StorageService.collection("planted")
		cursor = coll.find({
			"greenhouse_id": greenhouse_id,
			"week_planted": {"$lte": greenhouse_time},
			"week_of_harvest": {"$gte": greenhouse_time}
		})
		return await cursor.to_list()


	async def plant_new(self, greenhouse_id: str, tile_id: str, greenhouse_time: int, data: str):
		plant_id = data["plant_id"]
		plant = await self.StorageService.get("herbarium", plant_id)
		if plant is None:
			raise RuntimeError("Plant not found")
		seed_to_harvest_days = plant.get("seed_to_harvest_days")
		if seed_to_harvest_days is None:
			raise RuntimeError("Plant has no seed_to_harvest_days")
		week_of_harvest = greenhouse_time + seed_to_harvest_days // 7
		upsertor = self.StorageService.upsertor("planted")
		upsertor.set("greenhouse_id", greenhouse_id)
		upsertor.set("tile_id", tile_id)
		upsertor.set("week_planted", greenhouse_time)
		upsertor.set("plant_id", plant_id)
		upsertor.set("week_of_harvest", week_of_harvest)
		return await upsertor.execute()
