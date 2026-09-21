"""
Icon badge that toggles a destination's saved state entirely server-side
via Lively — no client JavaScript involved.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon

from web.services.destinations import Destination, toggle_saved
from web.ui.components.theme import Theme


class SaveToggleButton(FlexContainer):
    """
    Circular badge that toggles whether a destination is saved.
    """

    def on_create(self):
        super().on_create()

        destination: Destination = self.get_kwarg_or_raise("destination")
        self.destination_id = destination.destination_id

        self.style.update(self.badge_style())
        self.add_child(self.build_icon(destination.is_saved))

        self.bind("click", self.on_toggle, update_self=True)

    def badge_style(self) -> dict:
        """
        Returns the style dict for the circular badge shell.
        """
        return {
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "position": "absolute",
            "top": "12px",
            "right": "12px",
            "width": "40px",
            "height": "40px",
            "border-radius": "50%",
            "background": Theme.card_badge_color,
            "cursor": "pointer",
            "box-shadow": "0 4px 10px rgba(18, 26, 51, 0.15)",
        }

    def build_icon(self, is_saved: bool) -> Icon:
        """
        Builds the heart icon reflecting the current saved state.
        """
        klass = "bi bi-heart-fill" if is_saved else "bi bi-heart"
        color = Theme.success_color if is_saved else Theme.text_tertiary_color
        return Icon(klass=klass, style={"font-size": "1.2rem", "color": color})

    async def on_toggle(self, component, event, value, ws):
        """
        Flips the saved state and rebuilds this badge's icon in place.
        """
        destination = toggle_saved(self.destination_id)
        self.clear_children()
        self.add_child(self.build_icon(destination.is_saved))
