"""
Base page shared by every page in the app.
"""
from duck.shortcuts import static
from duck.html.components.container import Container
from duck.html.components.style import Style

from duck.native.components.page import AppPage

from web.meta import APP_LOGO_PATH, APP_NAME
from web.ui.components.bottom_nav import BottomNav
from web.ui.components.snackbar import Snackbar
from web.ui.components.theme import Theme
from web.ui.components.topbar import TopBar


class BasePage(AppPage):
    """
    Shared shell: top bar, centered content column, floating bottom
    nav, and the snackbar host used by the top bar menu.
    """

    page_title = APP_NAME

    def on_create(self):
        super().on_create()

        # SEO and browser chrome defaults
        self.set_title(self.page_title)
        self.set_favicon(static(APP_LOGO_PATH))
        self.set_accessibility(lang="en")
        self.add_meta(name="theme-color", content=Theme.accent_color)

        # Add viewport meta
        self.add_meta(
            name="viewport",
            content=(
                "width=device-width, "
                "initial-scale=1, "
                "viewport-fit=cover"
            ),
        )

        # Add global styles
        self.add_global_styles()

        # Shared layout: top bar, page-specific body, floating nav,
        # and the snackbar host the top bar menu shows toasts through
        snackbar = Snackbar()
        self.add_to_body([
            TopBar(snackbar=snackbar),
            self.build_content_column(),
            BottomNav(active=self.request.path),
            snackbar,
        ])

    def add_global_styles(self):
      """
      Adds global style/stylesheets.
      """
      self.add_stylesheet(href=static("css/bootstrap.min.css"))
      self.add_stylesheet(href=static("css/bootstrap-icons.min.css"))
      self.add_to_head(self.build_global_style())

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
                "max-width": Theme.max_content_width,
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
        Builds the minimal global reset and snackbar keyframes injected
        into <head>.
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
            @keyframes duck-snackbar-a {{
                0% {{ opacity: 0; transform: translate(-50%, 10px); }}
                12% {{ opacity: 1; transform: translate(-50%, 0); }}
                85% {{ opacity: 1; }}
                100% {{ opacity: 0; }}
            }}
            @keyframes duck-snackbar-b {{
                0% {{ opacity: 0; transform: translate(-50%, 10px); }}
                12% {{ opacity: 1; transform: translate(-50%, 0); }}
                85% {{ opacity: 1; }}
                100% {{ opacity: 0; }}
            }}
        """)
