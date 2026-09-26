"""
Sticky top app bar shown on every page.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.image import Image
from duck.shortcuts import static

from web.meta import APP_LOGO_PATH, APP_NAME
from web.ui.components.menu import TopBarMenu
from web.ui.components.theme import Theme


class TopBar(FlexContainer):
    """
    Sticky top bar with the app logo, title, and overflow menu.
    """

    def on_create(self):
        super().on_create()

        snackbar = self.get_kwarg_or_raise("snackbar")

        self.style.update({
            "display": "flex",
            "position": "sticky",
            "top": "0",
            "z-index": "10",
            "height": Theme.top_bar_height,
            "align-items": "center",
            "gap": Theme.top_bar_spacing,
            "padding": f"0 {Theme.screen_padding_x}",
            "background": Theme.top_bar_bg_color,
            "color": "#fff",
            "box-shadow": "0 2px 12px rgba(0, 0, 0, 0.12)",
        })

        logo = Image(
            source=static(APP_LOGO_PATH),
            alt=f"{APP_NAME} logo",
            style={
                "height": "32px",
                "width": "32px",
                "border-radius": "8px",
                "object-fit": "cover",
            },
        )
        title = Heading(
            type="h1",
            text=APP_NAME,
            style={"font-size": "1.05rem", "font-weight": "700", "margin": "0"},
        )

        self.add_children([logo, title, TopBarMenu(snackbar=snackbar)])
