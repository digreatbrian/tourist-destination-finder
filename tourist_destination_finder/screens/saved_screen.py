from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class SavedScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "saved"
        self.add_widget(
            MDLabel(
                text="Saved destinations module scaffold (KivyMD)",
                halign="center",
            )
        )
