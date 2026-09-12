"""
Main entry to the application.
"""
from kivymd.app import MDApp
from kivy.uix.button import Button

from core.container import AppContainer
from core.router import AppRouter


class TouristDestinationFinderApp(MDApp):
    """
    Main application class for Tourist Destination Finder.
    """
    
    def build(self):
        """
        Build and return the application's root widget.
        """
        self.title = "Tourist Destination Finder"
        
        # Initialize widgets
        container = AppContainer()
        router = AppRouter(container=container)
        
        # Return the router root
        return router.build_root()


if __name__ == "__main__":
    TouristDestinationFinderApp().run()
