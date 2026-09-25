"""
Detail page for a single destination.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.icon import Icon
from duck.html.components.link import LinkButton
from duck.html.components.paragraph import Paragraph

from web.services import destinations as destination_service
from web.ui.components.icon_text import IconText
from web.ui.components.save_toggle_button import SaveToggleButton
from web.ui.components.theme import Theme
from web.ui.pages.base import BasePage


class DestinationDetailPage(BasePage):
    """
    Shows full details for one destination, resolved from `?id=`.
    """

    page_title = "Tour Zimbabwe"

    def on_create(self):
        # Resolve the destination before the base page builds the layout
        destination_id = int(self.request.GET.get("id") or 0)
        self.destination = destination_service.get_destination(destination_id)

        if self.destination:
            self.page_title = f"{self.destination.name} — Tour Zimbabwe"

        super().on_create()

    def build_page_children(self) -> list:
        if self.destination is None:
            return [Paragraph(text="Destination not found.")]

        return [self.build_back_link(), self.build_hero(), self.build_body()]

    def build_back_link(self) -> LinkButton:
        """
        Builds the back-to-home link at the top of the page.
        """
        return LinkButton(
            url="/",
            text="Back",
            bg_color=Theme.accent_muted_color,
            style={
                "display": "inline-flex",
                "align-items": "center",
                "gap": "6px",
                "margin": "18px 0 0",
                "color": Theme.text_secondary_color,
                "font-weight": "600",
                "text-decoration": "none",
            },
        )

    def build_hero(self) -> FlexContainer:
        """
        Builds the icon banner and save toggle for the destination.
        """
        icon = Icon(
            klass=f"bi {self.destination.icon}",
            style={"font-size": "4.5rem", "color": "#fff"},
        )
        save_button = SaveToggleButton(destination=self.destination)

        return FlexContainer(
            style={
                "display": "flex",
                "position": "relative",
                "height": "230px",
                "border-radius": Theme.card_radius,
                "align-items": "center",
                "justify-content": "center",
                "background": f"linear-gradient(135deg, {self.destination.accent}, {Theme.surface_elevated_color})",
                "margin": "16px 0",
            },
            children=[icon, save_button],
        )

    def build_body(self) -> FlexContainer:
        """
        Builds the category tag, name, location, and description block.
        """
        category = Paragraph(
            text=self.destination.category,
            style={
                "align-self": "flex-start",
                "padding": "4px 12px",
                "border-radius": "999px",
                "background": Theme.accent_muted_color,
                "color": Theme.accent_color,
                "font-size": "0.75rem",
                "font-weight": "700",
                "text-transform": "uppercase",
                "margin": "0",
            },
        )
        name = Heading(
            type="h1",
            text=self.destination.name,
            style={"margin": "6px 0 0", "font-size": "1.55rem", "font-weight": "800"},
        )
        location = IconText(
            icon_class="bi-geo-alt-fill",
            text=self.destination.location,
            icon_style={"color": Theme.accent_color},
            text_style={"color": Theme.text_secondary_color, "font-size": "0.95rem"},
        )
        description = Paragraph(
            text=self.destination.description,
            style={"margin": "10px 0 0", "line-height": "1.6", "font-size": "1rem"},
        )

        return FlexContainer(
            style={"display": "flex", "flex-direction": "column", "gap": "8px"},
            children=[category, name, location, description],
        )
