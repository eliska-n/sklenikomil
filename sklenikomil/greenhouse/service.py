import logging

import asab

L = logging.getLogger(__name__)


class GreenhouseService(asab.Service):

	def __init__(self, app, service_name='GreenhouseService'):
		super().__init__(app, service_name)
		pass

	async def get_greenhouse(self, greenhouse_id, selected_week):
		greenhouse = []
		return greenhouse
