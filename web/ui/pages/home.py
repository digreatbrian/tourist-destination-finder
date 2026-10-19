"""
Home page: hero header plus the shared search experience.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.paragraph import Paragraph

from web.meta import APP_TAGLINE, APP_TAGLINE_SUBTITLE, HOME_PAGE_TITLE
from web.ui.components.search_experience import SearchExperience
from web.ui.components.theme import Theme
from web.ui.pages.base import BasePage


class HomePage(BasePage):
    """
    Landing page: hero header, then the search field, chips, and catalog.
    """

    page_title = HOME_PAGE_TITLE

    def build_page_children(self) -> list:
        return [self.build_hero(), SearchExperience()]

    def build_hero(self) -> FlexContainer:
        """
        Builds the title and subtitle at the top of the page.
        """
        title = Heading(
            type="h1",
            text=APP_TAGLINE,
            style={
                "margin": "0",
                "font-size": "2.1rem",
                "font-weight": "850",
                "letter-spacing": "-0.035em",
                "line-height": "1.1",
                "background": Theme.accent_gradient,
                "-webkit-background-clip": "text",
                "background-clip": "text",
                "-webkit-text-fill-color": "transparent",
                "color": "transparent",
            },
        )
        subtitle = Paragraph(
            text=APP_TAGLINE_SUBTITLE,
            style={"margin": "8px 0 0", "color": Theme.text_secondary_color, "font-size": "1rem", "line-height": "1.5"},
        )

        return FlexContainer(
            style={"display": "flex", "flex-direction": "column", "padding": "18px 0 18px"},
            children=[title, subtitle],
        )
