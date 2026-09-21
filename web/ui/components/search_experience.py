"""
Combined search field, category chips, and results grid — one component
shared by the home and search pages so both look and behave identically.
"""

from duck.html.components.container import FlexContainer

from web.services import destinations as destination_service
from web.ui.components.category_chips import CategoryChips
from web.ui.components.destination_grid import DestinationGrid
from web.ui.components.search_field import SearchField
from web.ui.components.theme import Theme


class SearchExperience(FlexContainer):
    """
    Self-contained search box, category chips, and filtered results grid,
    all wired together for live in-place filtering via Lively.
    """

    def on_create(self):
        super().on_create()

        query = self.kwargs.get("query", "")
        category = self.kwargs.get("category", "")
        state = {"query": query, "category": category}

        self.style.update({
            "display": "flex",
            "flex-direction": "column",
            "gap": Theme.section_spacing,
        })

        grid = DestinationGrid(
            destinations=destination_service.search_destinations(query, category),
            empty_message="No destinations match your search.",
        )
        
        chips = CategoryChips(
            categories=destination_service.list_categories(),
            state=state,
            grid=grid,
        )
        
        search_field = SearchField(state=state, grid=grid)

        self.add_children([search_field, chips, grid])
