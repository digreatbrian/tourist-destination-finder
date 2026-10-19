"""
Responsive grid of destination cards, with an empty state fallback.
"""

from duck.html.components.container import FlexContainer, GridContainer
from duck.html.components.icon import Icon
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
            "grid-template-columns": "repeat(auto-fill, minmax(260px, 1fr))",
            "gap": Theme.section_spacing,
        })

        self.set_destinations(self.get_kwarg_or_raise("destinations"))

    def set_destinations(self, destinations: list):
        """
        Rebuilds the grid's cards for a new destination list.
        """
        self.clear_children()

        if not destinations:
            self.add_child(FlexContainer(
                style={
                    "grid-column": "1 / -1",
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                    "gap": "12px",
                    "padding": "48px 24px",
                    "text-align": "center",
                },
                children=[
                    FlexContainer(
                        style={
                            "display": "flex",
                            "align-items": "center",
                            "justify-content": "center",
                            "width": "64px",
                            "height": "64px",
                            "border-radius": "50%",
                            "background": Theme.accent_soft_gradient,
                        },
                        children=[Icon(
                            klass="bi bi-compass",
                            style={"font-size": "1.7rem", "color": Theme.accent_color},
                        )],
                    ),
                    Paragraph(
                        text=self.empty_message,
                        style={
                            "margin": "0",
                            "max-width": "280px",
                            "color": Theme.text_secondary_color,
                            "line-height": "1.5",
                            "font-size": "0.95rem",
                        },
                    ),
                ],
            ))
            return

        for destination in destinations:
            self.add_child(DestinationCard(destination=destination, klass="tz-card"))
