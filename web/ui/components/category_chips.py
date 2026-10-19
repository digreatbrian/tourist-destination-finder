"""
Horizontal row of category filter chips, updated live via Lively.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.button import Button
from duck.contrib.sync import ensure_async

from web.ui.components.theme import Theme


class CategoryChips(FlexContainer):
    """
    Scrollable row of category chips that filter a target grid in place.

    Chips are rebuilt from scratch on every selection, so click
    bindings target this container (which stays mounted) rather than
    the individual chip button (which does not survive the rebuild).
    """

    ALL_LABEL = "All"

    def on_create(self):
        super().on_create()

        self.categories = self.get_kwarg_or_raise("categories")
        self.grid = self.get_kwarg_or_raise("grid")
        self.on_select = self.get_kwarg_or_raise("on_select")
        self.active_category = self.kwargs.get("active_category", "")

        self.style.update({
            "display": "flex",
            "flex-wrap": "nowrap",
            "gap": "8px",
            "overflow-x": "auto",
            "margin": f"0 -{Theme.screen_padding_x}",
            "box-sizing": "border-box",
            "padding": f"2px {Theme.screen_padding_x}",
        })

        self.build_chips()

    def set_active_category(self, category: str):
        """
        Updates the active category and refreshes the chip strip.

        Called by sibling components (e.g. the search field) when a
        change elsewhere should also reset the chip highlighting.
        """
        self.active_category = category
        
    def build_chips(self):
        """
        Builds all chip labels to reflect the current active category.
        """
        self.clear_children()
        self.add_child(self.build_chip(self.ALL_LABEL, ""))

        for category in self.categories:
            self.add_child(self.build_chip(category, category))

    def build_chip(self, label: str, category: str) -> Button:
        """
        Builds a single pill-shaped, clickable chip.
        """
        is_active = category == self.active_category

        chip = Button(text=label, klass="tz-press", style=self.chip_style(is_active))
        chip.bind(
            "click",
            self.build_select_handler(category),
            update_targets=[self, self.grid],
        )
        chip.category = category
        return chip

    def build_select_handler(self, category: str):
        """
        Builds a click handler that activates the given category.
        """
        async def on_click(component, event, value, ws):
            self.active_category = category
            active_style = self.chip_style(is_active=True)
            non_active_style = self.chip_style(is_active=False)
            
            for chip in self.children:
                if chip.category == category:
                    chip_style = active_style
                else:
                    chip_style = non_active_style
                chip.style.update(chip_style)
            
            await ensure_async(self.on_select)(category)

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
            "padding": "0 18px",
            "margin": "0",
            "border-radius": Theme.chip_radius,
            "background": Theme.accent_gradient if is_active else Theme.surface_color,
            "border": "1px solid transparent" if is_active else f"1px solid {Theme.surface_border_color}",
            "color": "#fff" if is_active else Theme.text_secondary_color,
            "font-size": "0.88rem",
            "font-weight": "650",
            "white-space": "nowrap",
            "cursor": "pointer",
            "box-shadow": "0 6px 16px rgba(59, 108, 246, 0.28)" if is_active else "none",
        }
