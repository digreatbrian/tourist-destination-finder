"""
Reusable destination preview card widget.
"""

import hashlib

from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from theme import AppTheme


FALLBACK_CARD_IMAGES = (
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=1200&q=80",
)


class DestinationCard(MDCard):
    """
    Displays destination summary details using an iOS-inspired card layout.
    """

    def __init__(
        self,
        title: str,
        subtitle: str,
        description: str,
        image_url: str = "",
        action_text: str = "View",
        **kwargs,
    ) -> None:
        """
        Initializes and builds a destination preview card.

        Args:
            title: Main destination name.
            subtitle: Secondary line (location and category).
            description: Short destination overview.
            image_url: Hero image URL for the destination card.
            action_text: Label shown on the action button.
        """
        super().__init__(**kwargs)

        # Apply card-level visual styling
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = AppTheme.CARD_HEIGHT
        self.padding = 0
        self.spacing = 0
        self.radius = [AppTheme.CARD_CORNER_RADIUS] * 4
        self.md_bg_color = AppTheme.SURFACE_COLOR
        self.line_color = AppTheme.SURFACE_BORDER_COLOR
        self.elevation = 2

        # Build image-first modern card layout
        self.add_widget(self._build_hero_image(title, subtitle, image_url))
        self.add_widget(
            self._build_content_section(
                title=title,
                subtitle=subtitle,
                description=description,
                action_text=action_text,
            )
        )

    def _build_hero_image(self, title: str, subtitle: str, image_url: str) -> FloatLayout:
        """
        Builds the image header with modern text overlay.

        Args:
            title: Destination name.
            subtitle: Destination metadata.
            image_url: Explicit destination image URL.

        Returns:
            Configured image header layout.
        """
        image_header = FloatLayout(size_hint_y=None, height=AppTheme.CARD_IMAGE_HEIGHT)
        image_header.add_widget(
            AsyncImage(
                source=self._resolve_image_url(title, image_url),
                allow_stretch=True,
                keep_ratio=False,
            )
        )
        image_header.add_widget(self._build_image_overlay())
        image_header.add_widget(
            MDLabel(
                text=subtitle.upper(),
                font_style="Caption",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.95),
                size_hint=(1, None),
                adaptive_height=True,
                halign="left",
                pos_hint={"x": 0.07, "y": 0.68},
                bold=True,
            )
        )
        image_header.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(0.86, None),
                adaptive_height=True,
                halign="left",
                pos_hint={"x": 0.07, "y": 0.16},
                bold=True,
            )
        )
        return image_header

    def _build_image_overlay(self) -> Widget:
        """
        Builds a dark overlay for better image text contrast.

        Returns:
            Configured overlay widget.
        """
        overlay = Widget()
        with overlay.canvas:
            Color(*AppTheme.CARD_OVERLAY_COLOR)
            overlay_rectangle = RoundedRectangle(radius=[0, 0, 0, 0])

        def update_overlay(*_) -> None:
            overlay_rectangle.pos = overlay.pos
            overlay_rectangle.size = overlay.size

        overlay.bind(pos=update_overlay, size=update_overlay)
        return overlay

    def _build_content_section(
        self,
        title: str,
        subtitle: str,
        description: str,
        action_text: str,
    ) -> MDBoxLayout:
        """
        Builds the lower information and action section.

        Args:
            title: Destination title.
            subtitle: Destination subtitle.
            description: Destination summary.
            action_text: Action label text.

        Returns:
            Configured content section layout.
        """
        content = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=AppTheme.CARD_PADDING,
            spacing=AppTheme.CARD_SPACING,
        )
        content.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )
        content.add_widget(self._build_subtitle_label(subtitle))
        content.add_widget(self._build_description_label(description))
        content.add_widget(self._build_action_row(action_text))
        return content

    def _build_subtitle_label(self, subtitle: str) -> MDLabel:
        """
        Builds the card subtitle label.

        Args:
            subtitle: Display subtitle text.

        Returns:
            Configured subtitle label.
        """
        return MDLabel(
            text=subtitle,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_TERTIARY_COLOR,
            adaptive_height=True,
        )

    def _build_description_label(self, description: str) -> MDLabel:
        """
        Builds the card description label.

        Args:
            description: Display description text.

        Returns:
            Configured multi-line description label.
        """
        return MDLabel(
            text=description,
            font_style="Body2",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_SECONDARY_COLOR,
            adaptive_height=True,
            shorten=True,
            shorten_from="right",
            max_lines=2,
        )

    def _build_action_row(self, action_text: str) -> MDBoxLayout:
        """
        Builds the action row shown at the bottom of the card.

        Args:
            action_text: Label shown on the action button.

        Returns:
            Configured action row with a right-aligned button.
        """
        action_row = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            padding=(0, AppTheme.CARD_SPACING, 0, 0),
        )

        # Push the button to the right side
        action_row.add_widget(MDBoxLayout())

        # Add an accent action button
        action_row.add_widget(
            MDRaisedButton(
                text=action_text,
                md_bg_color=AppTheme.ACCENT_COLOR,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                elevation=0,
            )
        )

        return action_row

    def _resolve_image_url(self, title: str, image_url: str) -> str:
        """
        Resolves the image URL shown in the card header.

        Args:
            title: Destination name used for deterministic fallback selection.
            image_url: Explicit destination image URL when available.

        Returns:
            An image URL for rendering.
        """
        if image_url.strip():
            return image_url

        title_hash = hashlib.sha256(title.encode("utf-8")).hexdigest()
        image_index = int(title_hash, 16) % len(FALLBACK_CARD_IMAGES)
        return FALLBACK_CARD_IMAGES[image_index]
