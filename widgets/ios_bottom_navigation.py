"""
Reusable iOS-inspired bottom navigation widget.
"""

from collections.abc import Callable

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard

from theme import AppTheme


TAB_ITEMS = (
    ("home", "Home"),
    ("search", "Explore"),
    ("saved", "Saved"),
)


class IOSBottomNavigation(MDCard):
    """
    Displays a simple rounded bottom navigation bar.
    """

    def __init__(
        self,
        current_tab: str,
        on_tab_selected: Callable[[str], None],
        **kwargs,
    ) -> None:
        """
        Initializes the bottom navigation widget.

        Args:
            current_tab: Name of the currently active tab.
            on_tab_selected: Callback invoked when a tab is selected.
        """
        super().__init__(**kwargs)

        # Apply surface styling
        self.size_hint_y = None
        self.height = AppTheme.NAV_BAR_HEIGHT
        self.radius = [
            AppTheme.NAV_BAR_RADIUS,
            AppTheme.NAV_BAR_RADIUS,
            AppTheme.NAV_BAR_RADIUS,
            AppTheme.NAV_BAR_RADIUS,
        ]
        self.padding = AppTheme.NAV_BAR_PADDING
        self.md_bg_color = AppTheme.ELEVATED_SURFACE_COLOR
        self.line_color = AppTheme.SURFACE_BORDER_COLOR
        self.elevation = 0

        # Build and add the horizontal tab row
        self.add_widget(self._build_tab_row(current_tab, on_tab_selected))

    def _build_tab_row(
        self,
        current_tab: str,
        on_tab_selected: Callable[[str], None],
    ) -> MDBoxLayout:
        """
        Builds navigation tab buttons.

        Args:
            current_tab: Name of the currently active tab.
            on_tab_selected: Callback invoked when a tab is selected.

        Returns:
            Configured horizontal tab row.
        """
        tab_row = MDBoxLayout(orientation="horizontal", spacing=AppTheme.CARD_SPACING)

        # Create and add each tab button
        for tab_name, tab_label in TAB_ITEMS:
            tab_row.add_widget(
                self._build_tab_button(
                    tab_name=tab_name,
                    tab_label=tab_label,
                    is_active=tab_name == current_tab,
                    on_tab_selected=on_tab_selected,
                )
            )

        return tab_row

    def _build_tab_button(
        self,
        tab_name: str,
        tab_label: str,
        is_active: bool,
        on_tab_selected: Callable[[str], None],
    ) -> MDFlatButton:
        """
        Builds a single tab button.

        Args:
            tab_name: Internal tab key.
            tab_label: User-facing label text.
            is_active: Whether this tab is currently selected.
            on_tab_selected: Callback invoked on selection.

        Returns:
            Configured tab button.
        """
        tab_button = MDFlatButton(
            text=tab_label,
            md_bg_color=(
                AppTheme.ACCENT_MUTED_COLOR if is_active else AppTheme.ELEVATED_SURFACE_COLOR
            ),
            theme_text_color="Custom",
            text_color=(
                AppTheme.ACCENT_COLOR if is_active else AppTheme.TEXT_SECONDARY_COLOR
            ),
        )
        tab_button.bind(on_release=lambda *_: on_tab_selected(tab_name))

        return tab_button
