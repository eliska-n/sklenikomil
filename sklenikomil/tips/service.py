import logging
import uuid

import asab

L = logging.getLogger(__name__)


class TipsService(asab.Service):

	def __init__(self, app, service_name='TipsService'):
		super().__init__(app, service_name)
		self.StorageService = app.get_service("asab.StorageService")
		self.HerbariumService = app.HerbariumService
		self.GreenhouseService = app.GreenhouseService

	async def list_greenhouse_tips(self, greenhouse_id, greenhouse_time):
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


	async def list_plant_tips(self, plant_id):
		coll = await self.StorageService.collection("tips")
		cursor = coll.find({"plant_id": plant_id})
		return await cursor.to_list()

	async def create_plant_tip(self, plant_id: str, tip: dict):
		# Generate a unique plant_id based on the display name and a UUID, omit letters with diacritics
		tip_id = uuid.uuid4().hex
		tip["plant_id"] = plant_id
		return await self.upsert_tip(tip_id, tip)

	async def update_tip(self, plant_id, tip_id: str, tip: dict):
		version = tip.pop("_v")
		tip.pop("_id", None)
		tip["plant_id"] = plant_id
		return await self.upsert_tip(tip_id, tip, version)

	async def upsert_tip(self, tip_id: str, tip: dict, version=0):
		upsertor = self.StorageService.upsertor("tips", tip_id, version)
		for key, value in tip.items():
			upsertor.set(key, value)
		await upsertor.execute()
		return tip_id

	async def delete_tip(self, plant_id: str, tip_id: str):
		coll = await self.StorageService.collection("tips")
		await coll.delete_one({"_id": tip_id, "plant_id": plant_id})
		return tip_id

	async def delete_plant_tips(self, plant_id: str):
		coll = await self.StorageService.collection("tips")
		await coll.delete_many({"plant_id": plant_id})
		return plant_id
