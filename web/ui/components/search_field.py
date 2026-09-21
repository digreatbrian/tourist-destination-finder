"""
Search input that filters a target grid in place via Lively — no page
reload and no client JavaScript.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.input import Input

from web.services import destinations as destination_service
from web.ui.components.theme import Theme


class SearchField(FlexContainer):
    """
    Pill-shaped search box that live-filters a target grid as the
    visitor types, using the search state shared with `CategoryChips`.
    """

    def on_create(self):
        super().on_create()

        self.state = self.get_kwarg_or_raise("state")
        self.grid = self.get_kwarg_or_raise("grid")

        self.style.update({
            "display": "flex",
            "align-items": "center",
            "gap": "12px",
            "width": "100%",
            "height": Theme.search_field_height,
            "padding": f"0 {Theme.search_field_padding}",
            "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": Theme.search_field_radius,
            "box-sizing": "border-box",
        })

        icon = Icon(
            klass="bi bi-search",
            style={"font-size": "1.05rem", "color": Theme.text_tertiary_color},
        )
        search_input = Input(
            type="search",
            name="q",
            placeholder="Search destinations or cities",
            props={"value": self.state["query"]},
            style={
                "flex": "1",
                "width": "100%",
                "border": "none",
                "outline": "none",
                "background": "transparent",
                "font-size": "1rem",
            },
        )
        search_input.bind("input", self.on_query_input, update_targets=[self.grid])

        self.add_children([icon, search_input])

    async def on_query_input(self, component, event, value, ws):
        """
        Updates the shared query state and refreshes the results grid.
        """
        self.state["query"] = value
        self.grid.set_destinations(
            destination_service.search_destinations(
                self.state["query"], self.state["category"]
            )
        )
