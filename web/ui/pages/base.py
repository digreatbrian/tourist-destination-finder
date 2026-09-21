"""
Base page shared by every page in the app.
"""

from duck.html.components.container import Container
from duck.html.components.page import Page
from duck.html.components.style import Style

from web.ui.components.bottom_nav import BottomNav
from web.ui.components.theme import Theme
from web.ui.components.topbar import TopBar

SITE_NAME = "Tour Zimbabwe"


class BasePage(Page):
    """
    Shared shell: top bar, centered content column, and floating bottom nav.
    """

    page_title = SITE_NAME

    def on_create(self):
        super().on_create()

        # SEO and browser chrome defaults
        self.set_title(self.page_title)
        self.set_favicon("/static/images/duck-logo.png")
        self.set_accessibility(lang="en")
        self.add_meta(name="theme-color", content=Theme.accent_color)
        self.add_meta(
            name="viewport",
            content="width=device-width, initial-scale=1, viewport-fit=cover",
        )
        self.add_to_head(self.build_global_style())

        # Shared layout: top bar, page-specific body, floating nav
        self.add_to_body(TopBar())
        self.add_to_body(self.build_content_column())
        self.add_to_body(BottomNav(active=self.request.path))

    def build_page_children(self) -> list:
        """
        Override in subclasses to return the page-specific body components.
        """
        raise NotImplementedError

    def build_content_column(self) -> Container:
        """
        Wraps subclass content in the centered, padded page column.
        """
        return Container(
            style={
                "max-width": "720px",
                "margin": "0 auto",
                "padding": (
                    f"{Theme.screen_padding_y} {Theme.screen_padding_x} "
                    f"calc({Theme.nav_bar_height} + {Theme.nav_bar_margin} * 3)"
                ),
            },
            children=self.build_page_children(),
        )

    def build_global_style(self) -> Style:
        """
        Builds the minimal global reset injected into <head>.
        """
        return Style(inner_html=f"""
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: {Theme.screen_bg_color};
                color: {Theme.text_primary_color};
                -webkit-tap-highlight-color: transparent;
            }}
        """)
