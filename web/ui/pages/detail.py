"""
Detail page for a single destination.
"""

from duck.shortcuts import resolve
from duck.html.components.container import Container, FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.icon import Icon
from duck.html.components.image import Image
from duck.html.components.link import Link
from duck.html.components.paragraph import Paragraph

from web.meta import APP_NAME, BACK_LABEL, NOT_FOUND_MESSAGE
from web.services import destinations as destination_service
from web.ui.components.contact_sheet import ContactSheet
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
            return [Paragraph(text=NOT_FOUND_MESSAGE, style={"padding": "40px 0", "text-align": "center"})]

        return [self.build_hero(), self.build_body(), ContactSheet(destination=self.destination)]

    def build_back_link(self) -> Link:
        """
        Builds the glass back button floating over the hero photo.
        """
        link = Link(
            url=resolve("home"),
            klass="tz-press",
            style={
                "position": "absolute", "top": "12px", "left": "12px", "z-index": "3",
                "display": "flex", "align-items": "center", "justify-content": "center",
                "width": "40px", "height": "40px", "border-radius": "50%",
                "background": Theme.card_badge_color,
                "backdrop-filter": Theme.glass_blur,
                "-webkit-backdrop-filter": Theme.glass_blur,
                "box-shadow": "0 4px 12px rgba(15, 23, 42, 0.18)",
                "text-decoration": "none",
            },
            children=[Icon(klass="bi bi-arrow-left", style={"font-size": "1.1rem", "color": Theme.text_primary_color})],
        )
        link.props["aria-label"] = BACK_LABEL
        return link

    def build_hero(self) -> FlexContainer:
        """
        Builds the destination photo, image credit, back and save buttons.
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
            },
        )
        save_button = SaveToggleButton(destination=self.destination)
        children = [image, Container(style={
            "position": "absolute", "inset": "0",
            "background": Theme.image_overlay, "pointer-events": "none",
        })]

        if self.destination.image_credit and self.destination.image_source_url:
            children.append(Link(
                url=self.destination.image_source_url,
                text=self.destination.image_credit,
                style={
                    "position": "absolute",
                    "right": "12px",
                    "bottom": "12px",
                    "z-index": "2",
                    "max-width": "70%",
                    "overflow": "hidden",
                    "text-overflow": "ellipsis",
                    "white-space": "nowrap",
                    "padding": "5px 10px",
                    "border-radius": "999px",
                    "background": Theme.image_credit_bg_color,
                    "color": Theme.image_credit_text_color,
                    "text-decoration": "none",
                    "font-size": "0.68rem",
                },
            ))
        else:
            children.append(Icon(
                klass=f"bi {self.destination.icon}",
                style={"position": "absolute", "font-size": "4.5rem", "color": "#fff", "opacity": "0.9"},
            ))

        children.extend([self.build_back_link(), save_button])

        return FlexContainer(
            style={
                "display": "flex",
                "position": "relative",
                "height": "280px",
                "border-radius": "28px",
                "overflow": "hidden",
                "align-items": "center",
                "justify-content": "center",
                "background": self.destination.accent,
                "margin": "4px 0 18px",
                "box-shadow": Theme.card_shadow,
            },
            children=children,
        )

    def build_body(self) -> FlexContainer:
        """
        Builds the category tag, name, location, and about block.
        """
        category = Paragraph(
            text=self.destination.category,
            style={
                "align-self": "flex-start",
                "padding": "5px 12px",
                "border-radius": "999px",
                "background": Theme.accent_muted_color,
                "color": Theme.accent_color,
                "font-size": "0.72rem",
                "font-weight": "750",
                "letter-spacing": "0.04em",
                "text-transform": "uppercase",
                "margin": "0",
            },
        )
        name = Heading(
            type="h1",
            text=self.destination.name,
            style={"margin": "4px 0 0", "font-size": "1.75rem", "font-weight": "800", "letter-spacing": "-0.03em"},
        )
        location = IconText(
            icon_class="bi-geo-alt-fill",
            text=self.destination.location,
            icon_style={"color": Theme.accent_color},
            text_style={"color": Theme.text_secondary_color, "font-size": "0.95rem"},
        )
        about = FlexContainer(
            style={
                "display": "flex", "flex-direction": "column", "gap": "6px",
                "margin-top": "6px", "padding": "16px 18px",
                "background": Theme.surface_color,
                "border": f"1px solid {Theme.surface_border_color}",
                "border-radius": Theme.card_radius,
                "box-shadow": Theme.card_shadow,
            },
            children=[
                Heading(type="h2", text="About", style={"margin": "0", "font-size": "0.95rem", "font-weight": "750"}),
                Paragraph(
                    text=self.destination.description,
                    style={"margin": "0", "line-height": "1.65", "font-size": "0.98rem", "color": Theme.text_secondary_color},
                ),
            ],
        )

        return FlexContainer(
            style={"display": "flex", "flex-direction": "column", "gap": "8px", "margin-bottom": "18px"},
            children=[category, name, location, about],
        )
