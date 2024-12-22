import logging
import uuid

import asab

L = logging.getLogger(__name__)


class HerbariumService(asab.Service):

	def __init__(self, app, service_name='HerbariumService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")

	async def list(self):
		coll = await self.StorageService.collection("plants")
		cursor = coll.find().limit(50)  # Adjust the limit as needed TODO: pagination
		res = await cursor.to_list()
		return res

	async def create_plant(self, description: dict):
		# Generate a unique plant_id based on the display name and a UUID, omit letters with diacritics
		plant_id = description.get("display_name", "").lower().replace(" ", "_").encode('ascii', 'ignore').decode('ascii') + uuid.uuid4().hex
		return await self.upsert_plant(plant_id, description)

	async def update_plant(self, plant_id: str, description: dict):
		return await self.upsert_plant(plant_id, description)

	async def upsert_plant(self, plant_id: str, description: dict):
		upsertor = self.StorageService.upsertor("plants", plant_id)
		for key, value in description.items():
			upsertor.set(key, value)
		await upsertor.execute()
		return plant_id

	async def delete_plant(self, plant_id: str):
		coll = await self.StorageService.collection("plants")
		await coll.delete_one({"_id": plant_id})

	async def create_advice(self, plant_id: str, week_from_seed: int, advice: dict):
		pass
