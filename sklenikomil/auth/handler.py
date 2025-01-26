import logging

import asab
import asab.web
import asab.web.rest


###

L = logging.getLogger(__name__)

###


class AuthHandler(object):
	def __init__(self, app):
		web_app = app.WebContainer.WebApp

		web_app.router.add_get('/auth', self.is_authorized)

	async def is_authorized(self, request):
		return asab.web.rest.json_response(
			request,
			{
				"result": "OK",
				"data": {
					"X-SSL-Client-Verified": request.headers.get("X-SSL-Client-Verified"),  # SUCCESS if verified, NONE if certificate is not provided
					"X-SSL-Client-Subject": request.headers.get("X-SSL-Client-Subject")
				}
			}
		)
