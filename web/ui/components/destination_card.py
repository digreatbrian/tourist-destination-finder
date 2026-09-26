"""
Reusable card showing a single destination preview.
"""

from duck.shortcuts import resolve
from duck.html.components.container import Container, FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.link import LinkButton
from duck.html.components.paragraph import Paragraph

from web.services.destinations import Destination
from web.ui.components.icon_text import IconText
from web.ui.components.save_toggle_button import SaveToggleButton
from web.ui.components.theme import Theme


class DestinationCard(Container):
    """
    Preview card linking to a destination's detail page.
    """

    def on_create(self):
        super().on_create()

        destination: Destination = self.get_kwarg_or_raise("destination")

        # Style the card shell
        self.style.update({
            "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": Theme.card_radius,
            "overflow": "hidden",
            "box-shadow": "0 8px 24px rgba(18, 26, 51, 0.06)",
        })

        self.add_children([
            self.build_media(destination),
            self.build_body(destination),
        ])

    def build_media(self, destination: Destination) -> FlexContainer:
        """
        Builds the icon banner and save toggle for the card.
        """
        icon = Icon(
            klass=f"bi {destination.icon}",
            style={"font-size": "2.75rem", "color": "#fff"},
        )
        
        save_button = SaveToggleButton(destination=destination)
        
        return FlexContainer(
            style={
                "display": "flex",
                "position": "relative",
                "height": Theme.card_image_height,
                "align-items": "center",
                "justify-content": "center",
                "background": f"linear-gradient(135deg, {destination.accent}, {Theme.surface_elevated_color})",
            },
            children=[icon, save_button],
        )

    def build_body(self, destination: Destination) -> FlexContainer:
        """
        Builds the category tag, name link, and location line.
        """
        category = Paragraph(
            text=destination.category,
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
        name_link = LinkButton(
            url=f"{resolve('destination_detail')}?id={destination.destination_id}",
            text=destination.name,
            style={
                "margin": "8px 0 0",
                "font-size": "1.15rem",
                "font-weight": "700",
                "color": Theme.text_primary_color,
                "text-decoration": "none",
                "background": Theme.accent_muted_color,
            },
        )
        
        location = IconText(
            icon_class="bi-geo-alt-fill",
            text=destination.location,
            icon_style={"color": Theme.accent_color},
            text_style={"color": Theme.text_secondary_color, "font-size": "0.9rem"},
        )

        return FlexContainer(
            style={
                "display": "flex",
                "flex-direction": "column",
                "gap": "6px",
                "padding": Theme.card_padding,
            },
            children=[category, name_link, location],
        )
