from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class SearchScreen(MDScreen):
    def __init__(self, destination_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "search"
        self.destination_service = destination_service
        self.add_widget(
            MDLabel(
                text="Search module scaffold (KivyMD)",
                halign="center",
            )
        )
