from kivymd.app import MDApp

from tourist_destination_finder.core.container import AppContainer
from tourist_destination_finder.core.router import AppRouter


class TouristDestinationFinderApp(MDApp):
    def build(self):
        self.title = "Tourist Destination Finder"
        container = AppContainer()
        router = AppRouter(container=container)
        return router.build_root()
