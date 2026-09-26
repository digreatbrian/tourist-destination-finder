"""
Saved destinations page.
"""

from duck.html.components.heading import Heading

from web.meta import SAVED_EMPTY_MESSAGE, SAVED_HEADING, SAVED_PAGE_TITLE
from web.services import destinations as destination_service
from web.ui.components.destination_grid import DestinationGrid
from web.ui.pages.base import BasePage


class SavedPage(BasePage):
    """
    Shows destinations the visitor has marked as saved.
    """

    page_title = SAVED_PAGE_TITLE

    def build_page_children(self) -> list:
        heading = Heading(
            type="h1",
            text=SAVED_HEADING,
            style={"margin": "14px 0", "font-size": "1.4rem", "font-weight": "800"},
        )
        grid = DestinationGrid(
            destinations=destination_service.list_saved_destinations(),
            empty_message=SAVED_EMPTY_MESSAGE,
        )

        return [heading, grid]
