"""
Sticky translucent top app bar shown on every page.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.image import Image
from duck.html.components.link import Link
from duck.shortcuts import resolve, static

from web.meta import APP_LOGO_PATH, APP_NAME
from web.ui.components.menu import TopBarMenu
from web.ui.components.theme import Theme


class TopBar(FlexContainer):
    """
    Glass top bar with the app logo, title, and overflow menu.
    """

    def on_create(self):
        super().on_create()

        snackbar = self.get_kwarg_or_raise("snackbar")

        self.style.update({
            "display": "flex",
            "position": "sticky",
            "top": "0",
            "z-index": "30",
            "height": Theme.top_bar_height,
            "align-items": "center",
            "gap": Theme.top_bar_spacing,
            "padding": f"0 {Theme.screen_padding_x}",
            "background": Theme.top_bar_bg_color,
            "backdrop-filter": Theme.glass_blur,
            "-webkit-backdrop-filter": Theme.glass_blur,
            "border-bottom": f"1px solid {Theme.surface_border_color}",
            "color": Theme.text_primary_color,
        })

        logo = Image(
            source=static(APP_LOGO_PATH),
            alt=f"{APP_NAME} logo",
            style={
                "height": "34px",
                "width": "34px",
                "border-radius": "10px",
                "object-fit": "cover",
                "box-shadow": "0 2px 8px rgba(59, 108, 246, 0.25)",
            },
        )
        title = Heading(
            type="h1",
            text=APP_NAME,
            style={
                "font-size": "1.08rem",
                "font-weight": "750",
                "margin": "0",
                "letter-spacing": "-0.02em",
            },
        )
        logo_link = Link(
            url=resolve("home"),
            children=[logo],
            style={"display": "flex", "align-items": "center"},
        )
        logo_link.props["aria-label"] = f"{APP_NAME} home"
        self.add_children([logo_link, title, TopBarMenu(snackbar=snackbar)])
