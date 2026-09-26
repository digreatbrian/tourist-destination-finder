"""
Top bar overflow menu: a kebab button revealing secondary actions.
"""

from duck.html.components.container import Container, FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.button import Button

from web.meta import MENU_ITEMS, SNACKBAR_COMING_SOON
from web.ui.components.theme import Theme


class TopBarMenu(FlexContainer):
    """
    Kebab button that toggles a dropdown of menu items.

    Every item is wired up but not yet implemented — selecting one
    shows a "coming soon" snackbar instead.
    """

    def on_create(self):
        super().on_create()

        self.snackbar = self.get_kwarg_or_raise("snackbar")
        self.open = False

        self.style.update({"position": "relative", "margin-left": "auto"})

        self.dropdown = self.build_dropdown()
        
        # Add dropdown children
        self.dropdown.add_children([self.build_item(label) for label in MENU_ITEMS],)
        
        # Add all children.
        self.add_children([self.build_toggle_button(), self.dropdown])

    def build_toggle_button(self) -> Button:
        """
        Builds the kebab icon button that opens/closes the dropdown.
        """
        icon = Icon(klass="bi bi-three-dots-vertical", style={"font-size": "1.15rem", "color": "#fff"})
        button = Button(
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "width": "36px",
                "height": "36px",
                "border-radius": "50%",
                "background": "transparent",
                "cursor": "pointer",
            },
            children=[icon],
        )
        button.bind("click", self.on_toggle, update_targets=[self.dropdown])
        return button

    async def on_toggle(self, component, event, value, ws):
        """
        Flips the dropdown's open state.
        """
        self.open = not self.open
        self.dropdown.style.update(self.dropdown_style())

    def build_dropdown(self) -> Container:
        """
        Builds the dropdown panel listing every menu item.
        """
        return Container(
            style=self.dropdown_style(),
        )

    def dropdown_style(self) -> dict:
        """
        Returns the style dict for the dropdown, open or closed.

        The dropdown container itself is never rebuilt, only its
        `display`, so it stays a valid `update_targets` reference.
        """
        return {
            "display": "flex" if self.open else "none",
            "flex-direction": "column",
            "position": "absolute",
            "top": "calc(100% + 8px)",
            "right": "0",
            "min-width": "180px",
            "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": "14px",
            "box-shadow": "0 12px 30px rgba(18, 26, 51, 0.18)",
            "overflow": "hidden",
            "z-index": "20",
        }

    def build_item(self, label: str) -> Button:
        """
        Builds a single dropdown menu item.
        """
        item = Button(
            text=label,
            style={
                "display": "block",
                "width": "100%",
                "padding": "12px 16px",
                "margin": "0",
                "border": "none",
                "background": "transparent",
                "text-align": "left",
                "color": Theme.text_primary_color,
                "font-size": "0.9rem",
                "font-weight": "600",
                "cursor": "pointer",
            },
        )
        item.bind(
            "click",
            self.build_select_handler(),
            update_targets=[self.dropdown, self.snackbar],
        )
        return item

    def build_select_handler(self):
        """
        Builds a click handler that closes the menu and shows the
        "coming soon" snackbar.
        """
        async def on_click(component, event, value, ws):
            self.open = False
            self.dropdown.style.update(self.dropdown_style())
            self.snackbar.show(SNACKBAR_COMING_SOON)

        return on_click
