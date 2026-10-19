"""
Floating bottom navigation bar.
"""
import json

from duck.utils.urlcrack import URL
from duck.shortcuts import resolve, static

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.paragraph import Paragraph
from duck.html.components.button import Button

from web.meta import NAV_ITEMS
from web.ui.components.theme import Theme


class BottomNav(FlexContainer):
    """
    Fixed, floating navigation bar with Home, Search, and Saved tabs.
    """

    def on_create(self):
        super().on_create()

        self.style.update({
            "display": "flex",
            "position": "fixed",
            "padding": Theme.nav_bar_padding,
            "gap": Theme.nav_bar_gap,
            "left": Theme.screen_padding_x,
            "right": Theme.screen_padding_x,
            "bottom": Theme.nav_bar_margin,
            "height": Theme.nav_bar_height,
            "max-width": Theme.max_content_width,
            "margin": "0 auto",
            "justify-content": "space-around",
            "align-items": "center",
            "z-index": "30",
            "background": Theme.glass_bg_color,
            "backdrop-filter": Theme.glass_blur,
            "-webkit-backdrop-filter": Theme.glass_blur,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": Theme.nav_bar_radius,
            "box-shadow": "0 12px 36px rgba(15, 23, 42, 0.14)",
        })

        active_path = URL(self.kwargs.get("active", resolve("home"))).path
        
        for url_name, active_icon, inactive_icon, label in NAV_ITEMS:
            url = resolve(url_name)
            is_active = URL(url).path == active_path
            icon_class = active_icon if is_active else inactive_icon
            self.add_child(self.build_nav_item(url, icon_class, label, is_active))

    def build_nav_item(self, url: str, icon_class: str, label: str, is_active: bool) -> FlexContainer:
        """
        Builds a single tappable nav item with a stacked icon and label.
        """
        color = Theme.accent_color if is_active else Theme.text_tertiary_color

        icon = Icon(klass=f"bi {icon_class}", style={"font-size": "1.25rem", "color": color})
        pill = FlexContainer(
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "width": "56px",
                "height": "30px",
                "border-radius": "999px",
                "background": Theme.accent_muted_color if is_active else "transparent",
            },
            children=[icon],
        )
        text = Paragraph(
            text=label,
            style={
                "margin": "0",
                "font-size": "0.72rem",
                "font-weight": "700" if is_active else "600",
                "color": color,
            },
        )

        item = Button(
            klass="tz-press",
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "gap": "2px",
                "cursor": "pointer",
                "flex": "1",
                "border": "none",
                "background": "transparent",
                "padding": "0",
            },
            children=[pill, text],
        )
        item.bind("click", self.build_navigate_handler(url))
        return item

    def build_navigate_handler(self, url: str):
        """
        Builds a click handler that navigates to the given URL.
        """
        async def on_click(component, event, value, ws):
            await ws.execute_js(f"window.open({json.dumps(url)})")
        return on_click
