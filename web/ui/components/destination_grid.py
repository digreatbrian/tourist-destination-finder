"""
Responsive grid of destination cards, with an empty state fallback.
"""

from duck.html.components.container import GridContainer
from duck.html.components.paragraph import Paragraph

from web.ui.components.destination_card import DestinationCard
from web.ui.components.theme import Theme


class DestinationGrid(GridContainer):
    """
    Grid layout listing destination cards, or an empty-state message.

    Exposes `set_destinations()` so this component can be passed as a
    Lively `update_targets` entry and refreshed in place during live
    search filtering, without a page reload.
    """

    def on_create(self):
        super().on_create()

        self.empty_message = self.kwargs.get("empty_message", "No destinations found.")

        self.style.update({
            "display": "grid",
            "grid-template-columns": "repeat(auto-fill, minmax(240px, 1fr))",
            "gap": Theme.section_spacing,
        })

        self.set_destinations(self.get_kwarg_or_raise("destinations"))

    def set_destinations(self, destinations: list):
        """
        Rebuilds the grid's cards for a new destination list.
        """
        self.clear_children()

        if not destinations:
            self.add_child(Paragraph(
                text=self.empty_message,
                style={
                    "grid-column": "1 / -1",
                    "text-align": "center",
                    "color": Theme.text_tertiary_color,
                    "padding": "40px 0",
                    "font-size": "0.95rem",
                },
            ))
            return

        for destination in destinations:
            self.add_child(DestinationCard(destination=destination))
