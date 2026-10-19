"""
Base page shared by every page in the app.
"""
from duck.shortcuts import static
from duck.html.components.container import Container
from duck.html.components.style import Style

from duck_native.components.page import AppPage

from web.meta import APP_LOGO_PATH, APP_NAME
from web.ui.components.ai_assistant import AIAssistant
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
            AIAssistant(),
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
            html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
            body {{
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
                -webkit-font-smoothing: antialiased;
                background:
                    radial-gradient(60% 40% at 90% -5%, rgba(124,92,250,0.16), transparent 70%),
                    radial-gradient(55% 35% at -10% 8%, rgba(34,211,238,0.14), transparent 70%),
                    {Theme.screen_bg_color};
                background-attachment: fixed;
                color: {Theme.text_primary_color};
                -webkit-tap-highlight-color: transparent;
                overscroll-behavior-y: none;
            }}
            button {{ font-family: inherit; }}
            a {{ -webkit-touch-callout: none; }}
            ::selection {{ background: rgba(59,108,246,0.2); }}
            .tz-card:hover {{ transform: translateY(-3px); box-shadow: 0 2px 4px rgba(15,23,42,0.05), 0 18px 40px rgba(15,23,42,0.12) !important; }}
            .tz-press {{ transition: transform .15s ease, opacity .15s ease; }}
            .tz-press:active {{ transform: scale(0.95); opacity: .9; }}
            .tz-search {{ transition: box-shadow .2s ease, border-color .2s ease; }}
            .tz-search:focus-within {{ border-color: {Theme.accent_color} !important; box-shadow: 0 0 0 4px rgba(59,108,246,0.15) !important; }}
            .tz-scroll::-webkit-scrollbar, .tz-hide-scroll::-webkit-scrollbar {{ display: none; }}
            .tz-scroll, .tz-hide-scroll {{ scrollbar-width: none; }}
            input::placeholder {{ color: {Theme.text_tertiary_color}; }}

            /* AI status pill: state is driven by data-state */
            #ai-status {{ display: none; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 999px;
                font-size: .8rem; font-weight: 650; background: {Theme.accent_muted_color}; color: {Theme.accent_color}; }}
            #ai-status[data-state="thinking"], #ai-status[data-state="working"],
            #ai-status[data-state="done"], #ai-status[data-state="error"] {{ display: inline-flex; }}
            #ai-status[data-state="done"] {{ background: #E7F8F1; color: #0B8F63; }}
            #ai-status[data-state="error"] {{ background: {Theme.danger_muted_color}; color: #C62828; }}
            #ai-status .tz-dot {{ width: 8px; height: 8px; border-radius: 50%; background: currentColor; flex: 0 0 auto; }}
            #ai-status[data-state="thinking"] .tz-dot, #ai-status[data-state="working"] .tz-dot {{
                animation: tz-pulse 1s ease-in-out infinite; }}
            #ai-fab[data-busy="1"] {{ animation: tz-glow 1.6s ease-in-out infinite; }}

            @keyframes tz-pulse {{ 0%,100% {{ transform: scale(.7); opacity: .5; }} 50% {{ transform: scale(1.2); opacity: 1; }} }}
            @keyframes tz-glow {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(124,92,250,0.5); }} 50% {{ box-shadow: 0 0 0 12px rgba(124,92,250,0); }} }}
            @keyframes tz-sheet-up {{ from {{ transform: translateY(40px); opacity: 0; }} to {{ transform: none; opacity: 1; }} }}
            @keyframes tz-pop {{ from {{ transform: translateY(16px) scale(.96); opacity: 0; }} to {{ transform: none; opacity: 1; }} }}
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
