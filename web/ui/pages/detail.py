"""
Detail page for a single destination.
"""

from duck.shortcuts import resolve
from duck.html.components.container import FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.icon import Icon
from duck.html.components.image import Image
from duck.html.components.link import Link
from duck.html.components.paragraph import Paragraph

from web.meta import APP_NAME, BACK_LABEL, NOT_FOUND_MESSAGE
from web.services import destinations as destination_service
from web.ui.components.icon_text import IconText
from web.ui.components.save_toggle_button import SaveToggleButton
from web.ui.components.theme import Theme
from web.ui.pages.base import BasePage


class DestinationDetailPage(BasePage):
    """
    Shows full details for one destination, resolved from `?id=`.
    """

    page_title = APP_NAME

    def on_create(self):
        # Resolve the destination before the base page builds the layout
        destination_id = int(self.request.GET.get("id") or 0)
        self.destination = destination_service.get_destination(destination_id)

        if self.destination:
            self.page_title = f"{self.destination.name} — {APP_NAME}"

        super().on_create()

    def build_page_children(self) -> list:
        if self.destination is None:
            return [Paragraph(text=NOT_FOUND_MESSAGE)]

        return [self.build_back_link(), self.build_hero(), self.build_body()]

    def build_back_link(self) -> Link:
        """
        Builds the back-to-home link at the top of the page.
        """
        return Link(
            url=resolve("home"),
            text=BACK_LABEL,
            style={
                "display": "inline-flex",
                "align-items": "center",
                "gap": "6px",
                "margin": "18px 0 0",
                "padding": "8px 12px",
                "border-radius": "999px",
                "background": Theme.accent_muted_color,
                "color": Theme.text_secondary_color,
                "font-weight": "600",
                "text-decoration": "none",
            },
        )

    def build_hero(self) -> FlexContainer:
        """
        Builds the destination photo, image credit, and save toggle.
        """
        image = Image(
            source=self.destination.image_url,
            alt=self.destination.name,
            style={
                "position": "absolute",
                "inset": "0",
                "width": "100%",
                "height": "100%",
                "object-fit": "cover",
                "border-radius": Theme.card_radius,
            },
        )
        save_button = SaveToggleButton(destination=self.destination)
        save_button.style["z-index"] = "1"
        children = [image]

        if self.destination.image_credit and self.destination.image_source_url:
            children.append(Link(
                url=self.destination.image_source_url,
                text=self.destination.image_credit,
                style={
                    "position": "absolute",
                    "left": "12px",
                    "bottom": "12px",
                    "z-index": "1",
                    "padding": "5px 9px",
                    "border-radius": "4px",
                    "background": "rgba(0, 0, 0, 0.6)",
                    "color": "#fff",
                    "font-size": "0.75rem",
                },
            ))
        else:
            children.append(Icon(
                klass=f"bi {self.destination.icon}",
                style={
                    "position": "absolute",
                    "font-size": "4.5rem",
                    "color": "#fff",
                },
            ))

        children.append(save_button)

        return FlexContainer(
            style={
                "display": "flex",
                "position": "relative",
                "height": "230px",
                "border-radius": Theme.card_radius,
                "overflow": "hidden",
                "align-items": "center",
                "justify-content": "center",
                "background": self.destination.accent,
                "margin": "16px 0",
            },
            children=children,
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
