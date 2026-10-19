"""
Reusable card showing a single destination preview.
"""

from duck.shortcuts import resolve
from duck.html.components.container import Container, FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.link import LinkButton
from duck.html.components.image import Image
from duck.html.components.paragraph import Paragraph

from quirl.components import SmartImage

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
            "box-shadow": Theme.card_shadow,
            "transition": "transform .2s ease, box-shadow .2s ease",
        })

        self.add_children([
            self.build_media(destination),
            self.build_body(destination),
        ])

    def build_media(self, destination: Destination) -> FlexContainer:
        """
        Builds the icon banner and save toggle for the card.
        """
        image = Image(
            source=destination.image_url,
            alt=destination.name,
            style={
                "position": "absolute",
                "inset": "0",
                "width": "100%",
                "height": "100%",
                "object-fit": "cover",
            },
        )
        
        save_button = SaveToggleButton(destination=destination)
        children = [image]
        detail_url = f"{resolve('destination_detail')}?id={destination.destination_id}"

        # Soft bottom gradient so overlaid labels stay legible
        children.append(Container(style={
            "position": "absolute", "inset": "0",
            "background": Theme.image_overlay, "pointer-events": "none",
        }))
        
        # Whole media area opens the detail page (save/credit sit above it)
        open_link = LinkButton(url=detail_url, children=[], style={
            "position": "absolute", "inset": "0", "z-index": "1",
        })
        
        open_link.props["aria-label"] = destination.name
        children.append(open_link)

        if destination.image_credit and destination.image_source_url:
            children.append(LinkButton(
                url=destination.image_source_url,
                text=destination.image_credit,
                style={
                    "position": "absolute",
                    "right": "10px",
                    "bottom": "10px",
                    "z-index": "2",
                    "max-width": "75%",
                    "overflow": "hidden",
                    "padding": "4px 8px",
                    "border-radius": "999px",
                    "background": Theme.image_credit_bg_color,
                    "color": Theme.image_credit_text_color,
                    "text-decoration": "none",
                    "font-size": "0.62rem",
                    "text-overflow": "ellipsis",
                    "white-space": "nowrap",
                },
            ))
        else:
            children.append(Icon(
                klass=f"bi {destination.icon}",
                style={
                    "position": "absolute",
                    "font-size": "2.75rem",
                    "color": "#fff",
                    "opacity": "0.9",
                },
            ))

        children.append(save_button)
        
        return FlexContainer(
            style={
                "display": "flex",
                "position": "relative",
                "height": Theme.card_image_height,
                "align-items": "center",
                "justify-content": "center",
                "background": destination.accent,
            },
            children=children,
        )

    def build_body(self, destination: Destination) -> FlexContainer:
        """
        Builds the category tag, name link, and location line.
        """
        category = Paragraph(
            text=destination.category,
            style={
                "align-self": "flex-start",
                "padding": "4px 11px",
                "border-radius": "999px",
                "background": Theme.accent_muted_color,
                "color": Theme.accent_color,
                "font-size": "0.68rem",
                "font-weight": "750",
                "letter-spacing": "0.04em",
                "text-transform": "uppercase",
                "margin": "0",
            },
        )
        name_link = LinkButton(
            url=f"{resolve('destination_detail')}?id={destination.destination_id}",
            text=destination.name,
            style={
                "margin": "2px 0 0",
                "font-size": "1.12rem",
                "font-weight": "750",
                "letter-spacing": "-0.02em",
                "color": Theme.text_primary_color,
                "text-decoration": "none",
            },
        )

        location = IconText(
            icon_class="bi-geo-alt-fill",
            text=destination.location,
            icon_style={"color": Theme.accent_color},
            text_style={"color": Theme.text_secondary_color, "font-size": "0.88rem"},
        )

        return FlexContainer(
            style={
                "display": "flex",
                "flex-direction": "column",
                "gap": "6px",
                "padding": "14px 16px 16px",
            },
            children=[category, name_link, location],
        )
