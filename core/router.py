from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.saved_screen import SavedScreen
from screens.search_screen import SearchScreen


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.add_widget(
            MDLabel(
                text="Tourist Destination Finder",
                halign="center",
            )
        )


class AppRouter:
    """
    Owns screen registration and route setup.
    """

    def __init__(self, container):
        self.container = container

    def build_root(self):
        manager = MDScreenManager()
        
        # Add screens
        manager.add_widget(HomeScreen())
        manager.add_widget(SearchScreen(destination_service=self.container.destination_service))
        manager.add_widget(SavedScreen())
        
        # Return the manager
        return manager
