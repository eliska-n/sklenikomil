import logging

import asab
import os

L = logging.getLogger(__name__)


class ImageService(asab.Service):

	def __init__(self, app, service_name='ImageService'):
		super().__init__(app, service_name)
		self.image_storage_path = asab.Config['image']['storage_path']

	# TODO: cleanup images every night that are not in used in any plant nor in any tip.

	def get_image(self, image_name):
		image_path = os.path.join(self.image_storage_path, image_name)
		if not os.path.exists(image_path):
			L.error(f"Image {image_name} not found in storage.")
			return None

		with open(image_path, 'rb') as image_file:
			image_data = image_file.read()

		return image_data

	async def get_image_iterator(self, image_name):
		image_path = os.path.join(self.image_storage_path, image_name)
		if not os.path.exists(image_path):
			L.error(f"Image {image_name} not found in storage.")
			raise FileNotFoundError

		with open(image_path, 'rb') as image_file:
			while True:
				chunk = image_file.read(1024)
				if not chunk:
					break
				yield chunk

	def get_image_path(self, file_id):
		return os.path.join(self.image_storage_path, file_id)

	def delete_image(self, image_name):
		image_path = os.path.join(self.image_storage_path, image_name)
		if os.path.exists(image_path):
			os.remove(image_path)
		else:
			L.error(f"Image {image_name} not found in storage.")
			return None
