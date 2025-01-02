import aiohttp
import logging

import asab
import asab.web
import asab.web.rest

###

L = logging.getLogger(__name__)

###


class ImageHandler(object):


	def __init__(self, app):
		self.ImageService = app.ImageService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/image/{image_name}', self.get_image)

	async def get_image(self, request):
		binary = self.ImageService.get_image(request.match_info['image_name'])
		if binary is None:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "Image not found"}, status=404)
		return aiohttp.web.Response(body=binary, content_type='image/jpeg')
	
