"""
Floating bottom navigation bar.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.paragraph import Paragraph
from duck.html.components.button import Button

from web.ui.components.theme import Theme


class BottomNav(FlexContainer):
    """
    Fixed, floating navigation bar with Home, Search, and Saved tabs.
    """

    # (url, icon when active, icon when inactive, label)
    NAV_ITEMS = [
        ("/", "bi-house-fill", "bi-house", "Home"),
        ("/search", "bi-search", "bi-search", "Search"),
        ("/saved", "bi-heart-fill", "bi-heart", "Saved"),
    ]

    def on_create(self):
        super().on_create()

        self.style.update({
            "display": "flex",
            "position": "fixed",
            "left": Theme.screen_padding_x,
            "right": Theme.screen_padding_x,
            "bottom": Theme.nav_bar_margin,
            "height": Theme.nav_bar_height,
            "max-width": "720px",
            "margin": "0 auto",
            "justify-content": "space-around",
            "align-items": "center",
            "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": Theme.nav_bar_radius,
            "box-shadow": "0 12px 30px rgba(18, 26, 51, 0.12)",
        })

        active_path = self.kwargs.get("active", "/")

        for url, active_icon, inactive_icon, label in self.NAV_ITEMS:
            is_active = url == active_path
            icon_class = active_icon if is_active else inactive_icon
            self.add_child(self.build_nav_item(url, icon_class, label, is_active))

    def build_nav_item(self, url: str, icon_class: str, label: str, is_active: bool) -> FlexContainer:
        """
        Builds a single tappable nav item with a stacked icon and label.
        """
        color = Theme.accent_color if is_active else Theme.text_tertiary_color

        icon = Icon(klass=f"bi {icon_class}", style={"font-size": "1.4rem", "color": color})
        text = Paragraph(
            text=label,
            style={"margin": "0", "font-size": "0.78rem", "font-weight": "600", "color": color},
        )

        item = Button(
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "gap": "4px",
                "cursor": "pointer",
                "flex": "1",
            },
            children=[icon, text],
        )
        item.bind("click", self.build_navigate_handler(url))
        return item

    def build_navigate_handler(self, url: str):
        """
        Builds a click handler that navigates to the given URL.
        """
        async def on_click(component, event, value, ws):
            await ws.execute_js(f"window.open('{url}')")

        return on_click
