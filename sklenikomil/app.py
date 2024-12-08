import asab.web
import asab.web.rest
import asab.metrics

from .greenhouse import GreenhouseService, GreenhouseHandler


asab.Config.add_defaults({
	"web": {
		"listen": "7777",
	},
})


class SklenikomilApp(asab.Application):

	def __init__(self):
		super().__init__()

		self.add_module(asab.web.Module)
		self.add_module(asab.metrics.Module)

		# Locate the web service
		self.WebService = self.get_service("asab.WebService")
		self.WebContainer = asab.web.WebContainer(self.WebService, "web")
		self.WebContainer.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

		self.GreenhouseService = GreenhouseService(self)
		self.GreenhouseHandler = GreenhouseHandler(self)
