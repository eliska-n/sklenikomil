import aiohttp
import aiohttp.web
import logging

import asab
import asab.web
import asab.web.rest

from ..auth import verify_client

###

L = logging.getLogger(__name__)

###


class ImageHandler(object):


	def __init__(self, app):
		self.ImageService = app.ImageService
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/image/{image_name}', self.get_image)
		web_app.router.add_post("/image/upload", self.handle_upload),
		# web_app.router.add_put("/image/{id}", self.handle_update),
		# web_app.router.add_delete("/image/{id}", self.handle_delete),

	async def get_image(self, request):
		image_name = request.match_info['image_name']
		response = aiohttp.web.StreamResponse()
		response.content_type = "application/octet-stream"
		response.headers["Content-Disposition"] = f"attachment; filename={image_name}"
		await response.prepare(request)
		try:
			async for chunk in self.ImageService.get_image_iterator(image_name):
				await response.write(chunk)
		except FileNotFoundError:
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "Image not found"}, status=404)
		await response.write_eof()
		return response

	@verify_client
	async def handle_upload(self, request):
		"""
		Handle image upload using streaming
		"""
		# Parse multipart request
		reader = await request.multipart()
		# Expect the first field to be 'image'
		file_field = await reader.next()
		if file_field.name != "image":
			return asab.web.rest.json_response(request, {"result": "ERROR", "error": "Invalid field name, expected 'image'"}, status=400)

		# Extract filename and content type
		filename = file_field.filename  # Original filename

		# Save the file
		file_path = self.ImageService.get_image_path(filename)
		with open(file_path, 'wb') as f:
			while chunk := await file_field.read_chunk():  # Read chunks of data
				f.write(chunk)
		return asab.web.rest.json_response(request, data={"result": "OK", "image": filename}, status=201)



# async def handle_update(request):
#     """
#     Update an existing image using streaming
#     """
#     file_id = request.match_info["id"]
#     file_path = UPLOAD_DIR / file_id

#     if not file_path.exists():
#         return web.json_response({"error": "File not found"}, status=404)

#     with file_path.open("wb") as f:
#         while True:
#             chunk = await request.content.read(1024 * 1024)  # Read in 1 MB chunks
#             if not chunk:
#                 break
#             f.write(chunk)

#     return web.json_response({"message": "File updated successfully"}, status=200)

# async def handle_delete(request):
#     """
#     Delete an image by ID
#     """
#     file_id = request.match_info["id"]
#     file_path = UPLOAD_DIR / file_id

#     if not file_path.exists():
#         return web.json_response({"error": "File not found"}, status=404)

#     file_path.unlink()  # Delete the file
#     return web.json_response({"message": "File deleted successfully"}, status=200)
