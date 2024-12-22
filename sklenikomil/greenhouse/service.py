import logging

import asab

L = logging.getLogger(__name__)


class GreenhouseService(asab.Service):

	def __init__(self, app, service_name='GreenhouseService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")

	async def get_greenhouse(self, greenhouse_id, greenhouse_time):
		greenhouse_size = 6 * 9  # 6 rows, 9 columns TODO: read this from the greenhouse collection
		coll = await self.StorageService.collection("planted")
		cursor = coll.find({
			"greenhouse_id": greenhouse_id,
			"week_planted": {"$lte": greenhouse_time},
			"week_of_harvest": {"$gte": greenhouse_time}
		})
		greenhouse = [{"tile_id": i, "planted": {}} for i in range(greenhouse_size)]
		while await cursor.fetch_next:
			obj = cursor.next_object()
			tile_id = int(obj.pop("tile_id"))
			assert len(greenhouse[tile_id]["planted"]) == 0
			assert "plant_id" in obj
			assert tile_id <= greenhouse_size
			greenhouse[tile_id]["planted"] = {k: v for k, v in obj.items() if not k.startswith("_")}
		return greenhouse


	async def plant_new(self, greenhouse_id: str, tile_id: str, greenhouse_time: int, data: str):
		plant_id = data["plant_id"]
		plant = await self.StorageService.get("plants", plant_id)
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
