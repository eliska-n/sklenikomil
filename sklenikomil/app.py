import asab.web
import asab.web.rest
import asab.metrics
import asab.storage

from .greenhouse import GreenhouseService, GreenhouseHandler
from .herbarium import HerbariumService, HerbariumHandler
from .tips import TipsService, TipsHandler
from .image import ImageService, ImageHandler
from .auth import AuthHandler


asab.Config.add_defaults({
	"web": {
		"listen": "7777",
	},
	"asab:storage": {
		"type": "mongodb",
		"mongodb_database": "sklenikomil",
	},
	"image": {
		"storage_path": "./images",
	}
})


class SklenikomilApp(asab.Application):

	def __init__(self):
		super().__init__()

		self.add_module(asab.web.Module)
		self.add_module(asab.metrics.Module)
		self.add_module(asab.storage.Module)

		# Locate the web service
		self.WebService = self.get_service("asab.WebService")
		self.WebContainer = asab.web.WebContainer(self.WebService, "web")
		self.WebContainer.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

		self.GreenhouseService = GreenhouseService(self)
		self.GreenhouseHandler = GreenhouseHandler(self)

		self.HerbariumService = HerbariumService(self)
		self.HerbariumHandler = HerbariumHandler(self)

		self.TipsService = TipsService(self)
		self.TipsHandler = TipsHandler(self)

		self.ImageService = ImageService(self)
		self.ImageHandler = ImageHandler(self)

		self.AuthHandler = AuthHandler(self)
