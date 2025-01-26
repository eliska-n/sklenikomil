import aiohttp.web


def verify_client(handler, *args, **kwargs):
	async def middleware_handler(self, request, *args, **kwargs):
		client_verified = request.headers.get('X-SSL-Client-Verified')
		if client_verified != 'SUCCESS':
			return aiohttp.web.json_response({"error": "Unauthorized"}, status=401)
		return await handler(self, request, *args, **kwargs)
	return middleware_handler
