"""
Search input that filters a target grid in place via Lively — no page
reload and no client JavaScript.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.input import Input

from web.meta import SEARCH_PLACEHOLDER
from web.ui.components.theme import Theme


class SearchField(FlexContainer):
    """
    Pill-shaped search box that live-filters the destinations grid.

    Clearing the text also resets the category chips to "All", so an
    empty query always shows the full default catalog.
    """

    def on_create(self):
        super().on_create()

        self.grid = self.get_kwarg_or_raise("grid")
        self.chips = self.get_kwarg_or_raise("chips")
        self.on_change = self.get_kwarg_or_raise("on_change")
        query = self.kwargs.get("query", "")

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
            placeholder=SEARCH_PLACEHOLDER,
            props={"value": query},
            style={
                "flex": "1",
                "width": "100%",
                "border": "none",
                "outline": "none",
                "background": "transparent",
                "font-size": "1rem",
            },
        )
        search_input.bind(
            "input",
            self.on_input,
            update_targets=[self.grid, self.chips],
        )

        self.add_children([icon, search_input])

    async def on_input(self, component, event, value, ws):
        """
        Reports the new query to the parent, which refreshes the grid.

        An empty value also resets the category chips, so clearing the
        box always restores the full default catalog.
        """
        self.on_change(value)

        if not value:
            self.chips.set_active_category("")
