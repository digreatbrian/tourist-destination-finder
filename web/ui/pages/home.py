"""
Home page: hero header plus the shared search experience.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.paragraph import Paragraph

from web.ui.components.search_experience import SearchExperience
from web.ui.components.theme import Theme
from web.ui.pages.base import BasePage


class HomePage(BasePage):
    """
    Landing page: hero header, then the search field, chips, and catalog.
    """

    page_title = "Tour Zimbabwe — Home"

    def build_page_children(self) -> list:
        return [self.build_hero(), SearchExperience()]

    def build_hero(self) -> FlexContainer:
        """
        Builds the title and subtitle at the top of the page.
        """
        title = Heading(
            type="h1",
            text="Discover Zimbabwe",
            style={"margin": "0", "font-size": "1.85rem", "font-weight": "800"},
        )
        
        subtitle = Paragraph(
            text="Falls, wildlife, and ancient ruins — all in one place.",
            style={"margin": "6px 0 0", "color": Theme.text_secondary_color, "font-size": "1rem"},
        )

        return FlexContainer(
            style={"display": "flex", "flex-direction": "column", "padding": "22px 0 4px"},
            children=[title, subtitle],
        )
