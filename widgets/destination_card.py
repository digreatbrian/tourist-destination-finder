"""
Reusable destination preview card widget.
"""

import hashlib
from collections.abc import Callable

from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from theme import AppTheme
from widgets.skeleton_image import SkeletonImage


FALLBACK_CARD_IMAGES = (
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=1200&q=80",
)


def resolve_destination_image_url(seed: str, image_url: str) -> str:
    """
    Resolves the image URL used for a destination visual.

    Args:
        seed: Stable text (e.g. destination title) used to deterministically
            pick a fallback image when no explicit URL is provided.
        image_url: Explicit destination image URL when available.

    Returns:
        An image URL ready for rendering.
    """
    if image_url.strip():
        return image_url

    # Pick a deterministic fallback image based on the seed text
    seed_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return FALLBACK_CARD_IMAGES[int(seed_hash, 16) % len(FALLBACK_CARD_IMAGES)]


class DestinationCard(MDCard):
    """
    Displays destination summary details using a modern image-first layout.
    """

    def __init__(
        self,
        title: str,
        subtitle: str,
        description: str,
        image_url: str = "",
        action_text: str = "View",
        on_view: Callable[[], None] | None = None,
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
            on_view: Callback invoked when the action button is pressed.
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
        self.elevation = 3

        # Build the image-on-top layout, followed by text and widgets
        self.add_widget(self._build_hero_image(title, image_url))
        self.add_widget(
            self._build_content_section(
                title=title,
                subtitle=subtitle,
                description=description,
                action_text=action_text,
                on_view=on_view,
            )
        )

    def _build_hero_image(self, title: str, image_url: str) -> FloatLayout:
        """
        Builds the top hero image with a skeleton loading state.

        Args:
            title: Destination name used for deterministic fallback selection.
            image_url: Explicit destination image URL.

        Returns:
            Configured image header layout.
        """
        image_header = FloatLayout(size_hint_y=None, height=AppTheme.CARD_IMAGE_HEIGHT)
        image_header.add_widget(
            SkeletonImage(
                source=resolve_destination_image_url(title, image_url),
                radius=[AppTheme.CARD_CORNER_RADIUS, AppTheme.CARD_CORNER_RADIUS, 0, 0],
                size_hint=(1, 1),
            )
        )
        return image_header

    def _build_content_section(
        self,
        title: str,
        subtitle: str,
        description: str,
        action_text: str,
        on_view: Callable[[], None] | None,
    ) -> MDBoxLayout:
        """
        Builds the lower information and action section shown below the image.

        Args:
            title: Destination title.
            subtitle: Destination subtitle.
            description: Destination summary.
            action_text: Action label text.
            on_view: Callback invoked when the action button is pressed.

        Returns:
            Configured content section layout.
        """
        content = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=AppTheme.CARD_PADDING,
            spacing=AppTheme.CARD_SPACING,
        )
        content.add_widget(self._build_title_row(title))
        content.add_widget(self._build_subtitle_label(subtitle))
        content.add_widget(self._build_description_label(description))
        content.add_widget(self._build_action_row(action_text, on_view))
        return content

    def _build_title_row(self, title: str) -> MDBoxLayout:
        """
        Builds the title row with a bookmark icon accent.

        Args:
            title: Destination title text.

        Returns:
            Configured title row layout.
        """
        title_row = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        title_row.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )
        title_row.add_widget(
            MDIconButton(
                icon="bookmark-outline",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_TERTIARY_COLOR,
                size_hint=(None, None),
                size=(AppTheme.CHIP_HEIGHT, AppTheme.CHIP_HEIGHT),
            )
        )
        return title_row

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
            text_color=AppTheme.ACCENT_COLOR,
            adaptive_height=True,
            bold=True,
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

    def _build_action_row(
        self,
        action_text: str,
        on_view: Callable[[], None] | None,
    ) -> MDBoxLayout:
        """
        Builds the action row shown at the bottom of the card.

        Args:
            action_text: Label shown on the action button.
            on_view: Callback invoked when the action button is pressed.

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

        # Add an accent action button wired to the view callback
        action_button = MDRaisedButton(
            text=action_text,
            md_bg_color=AppTheme.ACCENT_COLOR,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            elevation=0,
            radius=[AppTheme.CHIP_RADIUS] * 4,
        )
        if on_view is not None:
            action_button.bind(on_release=lambda *_: on_view())
        action_row.add_widget(action_button)

        return action_row
