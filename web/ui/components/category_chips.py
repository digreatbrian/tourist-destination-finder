"""
Horizontal row of category filter chips, updated live via Lively.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.paragraph import Paragraph

from web.services import destinations as destination_service
from web.ui.components.theme import Theme


class CategoryChips(FlexContainer):
    """
    Scrollable row of category chips that filter a target grid in place.
    """

    def on_create(self):
        super().on_create()

        self.categories = self.get_kwarg_or_raise("categories")
        self.state = self.get_kwarg_or_raise("state")
        self.grid = self.get_kwarg_or_raise("grid")
        
        self.style.update({
            "display": "flex",
            "gap": "10px",
            "overflow-x": "auto",
            "max-width": Theme.max_content_width,
            "padding": f"{Theme.section_spacing} 0",
        })

        self.rebuild_chips()

    def rebuild_chips(self):
        """
        Rebuilds all chip labels to reflect the current active category.
        """
        self.clear_children()
        self.add_child(self.build_chip("All", ""))
        
        for category in self.categories:
            self.add_child(self.build_chip(category, category))

    def build_chip(self, label: str, category: str) -> Paragraph:
        """
        Builds a single pill-shaped, clickable chip.
        """
        is_active = category == self.state["category"]

        chip = Paragraph(text=label, style=self.chip_style(is_active))
        chip.bind(
            "click",
            self.build_select_handler(category),
            update_self=True,
            update_targets=[self.grid],
        )
        return chip

    def build_select_handler(self, category: str):
        """
        Builds a click handler that activates the given category.
        """
        async def on_click(component, event, value, ws):
            self.state["category"] = category
            self.rebuild_chips()
            self.grid.set_destinations(
                destination_service.search_destinations(
                    self.state["query"], self.state["category"]
                )
            )

        return on_click

    def chip_style(self, is_active: bool) -> dict:
        """
        Returns the style dict for a chip in its active or inactive state.
        """
        return {
            "flex": "0 0 auto",
            "display": "flex",
            "align-items": "center",
            "height": Theme.chip_height,
            "padding": "0 20px",
            "margin": "0",
            "border-radius": Theme.chip_radius,
            "background": Theme.accent_color if is_active else Theme.surface_color,
            "border": f"1px solid {Theme.accent_color if is_active else Theme.surface_border_color}",
            "color": "#fff" if is_active else Theme.text_secondary_color,
            "font-size": "0.9rem",
            "font-weight": "600",
            "white-space": "nowrap",
            "cursor": "pointer",
        }
