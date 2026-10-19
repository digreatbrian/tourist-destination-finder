"""
Contact button that opens a bottom sheet of ways to reach a destination.
"""

from duck.html.components.button import Button
from duck.html.components.container import Container, FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.icon import Icon
from duck.html.components.link import Link
from duck.html.components.paragraph import Paragraph

from web.services import contacts
from web.ui.components.theme import Theme


class ContactSheet(Container):
    """
    Gradient "Contact" button plus a toggled bottom sheet (call, WhatsApp,
    email, website, directions). Toggled server-side via Lively.
    """

    def on_create(self):
        super().on_create()

        self.destination = self.get_kwarg_or_raise("destination")
        self.open = False

        self.overlay = Container(style=self.overlay_style())
        self.overlay.add_children([self.build_scrim(), self.build_sheet()])

        self.add_children([self.build_trigger(), self.overlay])

    def overlay_style(self) -> dict:
        return {
            "display": "block" if self.open else "none",
            "position": "fixed",
            "inset": "0",
            "z-index": "60",
        }

    def build_trigger(self) -> Button:
        button = Button(
            klass="tz-press",
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "gap": "10px",
                "width": "100%",
                "height": "56px",
                "border": "none",
                "border-radius": "999px",
                "background": Theme.accent_gradient,
                "color": "#fff",
                "font-size": "1rem",
                "font-weight": "700",
                "cursor": "pointer",
                "box-shadow": Theme.float_shadow,
            },
            children=[
                Icon(klass="bi bi-chat-dots-fill", style={"font-size": "1.1rem", "color": "#fff"}),
                Paragraph(text="Contact this destination", style={"margin": "0", "color": "#fff"}),
            ],
        )
        button.bind("click", self.on_toggle, update_targets=[self.overlay])
        return button

    def build_scrim(self) -> Container:
        scrim = Container(style={
            "position": "absolute", "inset": "0",
            "background": Theme.scrim_color,
            "backdrop-filter": "blur(3px)",
        })
        scrim.bind("click", self.on_toggle, update_targets=[self.overlay])
        return scrim

    def build_sheet(self) -> FlexContainer:
        close = Button(
            klass="tz-press",
            style={
                "display": "flex", "align-items": "center", "justify-content": "center",
                "width": "36px", "height": "36px", "border": "none", "border-radius": "50%",
                "background": Theme.surface_elevated_color, "cursor": "pointer",
            },
            children=[Icon(klass="bi bi-x-lg", style={"font-size": "0.95rem", "color": Theme.text_secondary_color})],
        )
        close.bind("click", self.on_toggle, update_targets=[self.overlay])

        header = FlexContainer(
            style={"display": "flex", "align-items": "center", "justify-content": "space-between"},
            children=[
                FlexContainer(
                    style={"display": "flex", "flex-direction": "column", "gap": "2px"},
                    children=[
                        Heading(type="h2", text="Get in touch", style={
                            "margin": "0", "font-size": "1.2rem", "font-weight": "800",
                            "letter-spacing": "-0.02em"}),
                        Paragraph(text=self.destination.name, style={
                            "margin": "0", "font-size": "0.85rem", "color": Theme.text_secondary_color}),
                    ],
                ),
                close,
            ],
        )

        handle = Container(style={
            "width": "40px", "height": "4px", "border-radius": "999px",
            "background": Theme.surface_border_color, "margin": "0 auto 4px",
        })
        rows = [
            self.build_row(channel)
            for channel in contacts.get_channels(self.destination.name, self.destination.location)
        ]

        return FlexContainer(
            style={
                "display": "flex",
                "flex-direction": "column",
                "gap": "14px",
                "position": "absolute",
                "left": "0", "right": "0", "bottom": "0",
                "max-width": Theme.max_content_width,
                "margin": "0 auto",
                "padding": "12px 18px calc(22px + env(safe-area-inset-bottom, 0px))",
                "background": Theme.surface_color,
                "border-radius": "28px 28px 0 0",
                "box-shadow": Theme.sheet_shadow,
                "animation": "tz-sheet-up .28s cubic-bezier(.2,.8,.2,1)",
            },
            children=[handle, header, *rows],
        )

    def build_row(self, channel: "contacts.ContactChannel") -> Link:
        icon_bubble = FlexContainer(
            style={
                "display": "flex", "align-items": "center", "justify-content": "center",
                "flex": "0 0 auto", "width": "44px", "height": "44px", "border-radius": "14px",
                "background": Theme.accent_soft_gradient,
            },
            children=[Icon(klass=f"bi {channel.icon}", style={"font-size": "1.1rem", "color": Theme.accent_color})],
        )
        texts = FlexContainer(
            style={"display": "flex", "flex-direction": "column", "flex": "1", "min-width": "0"},
            children=[
                Paragraph(text=channel.label, style={
                    "margin": "0", "font-size": "0.95rem", "font-weight": "700",
                    "color": Theme.text_primary_color}),
                Paragraph(text=channel.detail, style={
                    "margin": "0", "font-size": "0.82rem", "color": Theme.text_secondary_color,
                    "overflow": "hidden", "text-overflow": "ellipsis", "white-space": "nowrap"}),
            ],
        )
        chevron = Icon(klass="bi bi-chevron-right", style={"font-size": "0.9rem", "color": Theme.text_tertiary_color})

        row = Link(
            url=channel.url,
            klass="tz-press",
            style={
                "display": "flex", "align-items": "center", "gap": "14px",
                "padding": "10px 12px", "border-radius": "18px",
                "background": Theme.surface_elevated_color,
                "border": f"1px solid {Theme.surface_border_color}",
                "text-decoration": "none",
            },
            children=[icon_bubble, texts, chevron],
        )
        if channel.external:
            row.props["target"] = "_blank"
            row.props["rel"] = "noopener"
        return row

    async def on_toggle(self, component, event, value, ws):
        """
        Opens or closes the sheet.
        """
        self.open = not self.open
        self.overlay.style.update(self.overlay_style())
