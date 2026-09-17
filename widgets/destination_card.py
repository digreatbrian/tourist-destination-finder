"""
Reusable destination preview card widget.
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from theme import AppTheme


class DestinationCard(MDCard):
    """
    Displays destination summary details using an iOS-inspired card layout.
    """

    def __init__(
        self,
        title: str,
        subtitle: str,
        description: str,
        action_text: str = "View",
        **kwargs,
    ) -> None:
        """
        Initializes and builds a destination preview card.

        Args:
            title: Main destination name.
            subtitle: Secondary line (location and category).
            description: Short destination overview.
            action_text: Label shown on the action button.
        """
        super().__init__(**kwargs)

        # Apply card-level visual styling
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = AppTheme.CARD_HEIGHT
        self.padding = AppTheme.CARD_PADDING
        self.spacing = AppTheme.CARD_SPACING
        self.radius = [AppTheme.CARD_CORNER_RADIUS] * 4
        self.md_bg_color = AppTheme.SURFACE_COLOR
        self.line_color = AppTheme.SURFACE_BORDER_COLOR
        self.elevation = 0

        # Build title and subtitle labels
        self.add_widget(self._build_title_label(title))
        self.add_widget(self._build_subtitle_label(subtitle))

        # Build the destination summary label
        self.add_widget(self._build_description_label(description))

        # Add a right-aligned action button row
        self.add_widget(self._build_action_row(action_text))

    def _build_title_label(self, title: str) -> MDLabel:
        """
        Builds the card title label.

        Args:
            title: Display title text.

        Returns:
            Configured title label.
        """
        return MDLabel(
            text=title,
            font_style="H6",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_PRIMARY_COLOR,
            adaptive_height=True,
            bold=True,
        )

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
            MDFlatButton(
                text=action_text,
                theme_text_color="Custom",
                text_color=AppTheme.ACCENT_COLOR,
            )
        )

        return action_row
