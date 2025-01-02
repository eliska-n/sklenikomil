import logging
import uuid

import asab
import os

L = logging.getLogger(__name__)


class ImageService(asab.Service):

	def __init__(self, app, service_name='ImageService'):
		super().__init__(app, service_name)
		self.image_storage_path = app.Config['image']['storage_path']

	def get_image(self, image_name):
		image_path = os.path.join(self.image_storage_path, image_name)
		if not os.path.exists(image_path):
			L.error(f"Image {image_name} not found in storage.")
			return None

		with open(image_path, 'rb') as image_file:
			image_data = image_file.read()

		return image_data

	def save_image(self, image_data, image_name=None):
		if image_name is None:
			image_name = str(uuid.uuid4())
		else:
			image_name = str(uuid.uuid4()) + image_name
		image_path = os.path.join(self.image_storage_path, image_name)
		with open(image_path, 'wb') as image_file:
			image_file.write(image_data)
		return image_name

	def delete_image(self, image_name):
		image_path = os.path.join(self.image_storage_path, image_name)
		if os.path.exists(image_path):
			os.remove(image_path)
		else:
			L.error(f"Image {image_name} not found in storage.")
			return None
