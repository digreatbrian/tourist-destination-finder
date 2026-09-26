"""
Combined search field, category chips, and results grid — one component
shared by the home and search pages so both look and behave identically.
"""

from duck.html.components.container import FlexContainer

from web.meta import SEARCH_EMPTY_MESSAGE
from web.services import destinations as destination_service
from web.ui.components.category_chips import CategoryChips
from web.ui.components.destination_grid import DestinationGrid
from web.ui.components.search_field import SearchField
from web.ui.components.theme import Theme


class SearchExperience(FlexContainer):
    """
    Self-contained search box, category chips, and filtered results
    grid, wired together for live in-place filtering via Lively.

    Owns the query and category filters directly as instance
    attributes: Lively keeps this component alive across
    interactions, so no separate shared "state" object is needed.
    """

    def on_create(self):
        super().on_create()

        self.query = self.kwargs.get("query", "")
        self.category = self.kwargs.get("category", "")

        self.id = "search-experience"
        self.style.update({
            "display": "flex",
            "flex-direction": "column",
            "gap": Theme.section_spacing,
        })

        self.grid = DestinationGrid(
            destinations=self.filtered_destinations(),
            empty_message=SEARCH_EMPTY_MESSAGE,
        )
        self.chips = CategoryChips(
            categories=destination_service.list_categories(),
            active_category=self.category,
            grid=self.grid,
            on_select=self.on_category_select,
        )
        self.search_field = SearchField(
            query=self.query,
            grid=self.grid,
            chips=self.chips,
            on_change=self.on_query_change,
        )

        self.add_children([self.search_field, self.chips, self.grid])

    def filtered_destinations(self) -> list:
        """
        Returns destinations matching the current query and category.
        """
        return destination_service.search_destinations(self.query, self.category)

    def on_query_change(self, value: str):
        """
        Updates the query and, once cleared, the category too, then
        refreshes the results grid.
        """
        self.query = value

        if not value:
            self.category = ""

        self.grid.set_destinations(self.filtered_destinations())

    def on_category_select(self, category: str):
        """
        Updates the active category and refreshes the results grid.
        """
        self.category = category
        self.grid.set_destinations(self.filtered_destinations())
