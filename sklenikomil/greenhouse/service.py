import logging
import uuid

import asab

L = logging.getLogger(__name__)


class GreenhouseService(asab.Service):

	def __init__(self, app, service_name='GreenhouseService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")

	async def get_greenhouse(self, greenhouse_id, selected_week):
		coll = await self.StorageService.collection("planted")
		cursor = coll.find({
			"greenhouse_id": greenhouse_id,
			"week_planted": {"$lte": selected_week},
			"week_of_harvest": {"$gte": selected_week}
		})
		greenhouse = []
		while await cursor.fetch_next:
			obj = cursor.next_object()
			greenhouse.append({k: v for k, v in obj.items() if not k.startswith("_")})
		return greenhouse


	async def upsert_planted(self, greenhouse_id: str, tile_id: str, selected_week: int, data: str):
		plant_id = data["plant_id"]
		plant = await self.StorageService.get("plants", plant_id)
		if plant is None:
			raise RuntimeError("Plant not found")
		seed_to_harvest_days = plant.get("seed_to_harvest_days")
		if seed_to_harvest_days is None:
			raise RuntimeError("Plant has no seed_to_harvest_days")
		week_of_harvest = selected_week + seed_to_harvest_days // 7
		upsertor = self.StorageService.upsertor("planted")
		upsertor.set("greenhouse_id", greenhouse_id)
		upsertor.set("tile_id", tile_id)
		upsertor.set("week_planted", selected_week)
		upsertor.set("plant_id", plant_id)
		upsertor.set("week_of_harvest", week_of_harvest)
		return await upsertor.execute()

	async def create_plant(self, description: dict):
		# Generate a unique plant_id based on the display name and a UUID, omit letters with diacritics
		plant_id = description.get("display_name", "").lower().replace(" ", "_").encode('ascii', 'ignore').decode('ascii') + uuid.uuid4().hex
		return await self.upsert_plant(plant_id, description)


	async def upsert_plant(self, plant_id: str, description: dict):
		upsertor = self.StorageService.upsertor("plants", plant_id)
		for key, value in description.items():
			upsertor.set(key, value)
		await upsertor.execute()

		return plant_id

	async def create_advice(self, plant_id: str, week_from_seed: int, advice: dict):
		pass
