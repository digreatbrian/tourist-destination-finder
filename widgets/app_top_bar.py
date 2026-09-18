"""
Reusable top navigation bar shown across app screens.
"""

from collections.abc import Callable

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

from theme import AppTheme


class AppTopBar(MDBoxLayout):
    """
    Displays the top bar in either a branded mode or a back-navigation mode.
    """

    def __init__(
        self,
        title: str,
        on_back: Callable[[], None] | None = None,
        trailing_icon: str = "bell-outline",
        on_trailing_pressed: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        """
        Initializes the top bar layout.

        Args:
            title: Text shown next to the leading control.
            on_back: Callback invoked when the back button is pressed. When
                provided, a back button replaces the branded logo badge.
            trailing_icon: Material icon name for the trailing action button.
            on_trailing_pressed: Callback invoked when the trailing button
                is pressed.
        """
        super().__init__(**kwargs)

        # Apply top bar layout styling
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = AppTheme.TOP_BAR_HEIGHT
        self.spacing = AppTheme.TOP_BAR_SPACING

        # Add the leading logo/back control with the title
        self.add_widget(self._build_leading_section(title, on_back))

        # Add the trailing action button
        self.add_widget(self._build_trailing_button(trailing_icon, on_trailing_pressed))

    def _build_leading_section(
        self,
        title: str,
        on_back: Callable[[], None] | None,
    ) -> MDBoxLayout:
        """
        Builds the leading logo/back button and title label.

        Args:
            title: Text shown next to the leading control.
            on_back: Callback invoked when the back button is pressed.

        Returns:
            Configured leading section layout.
        """
        leading_section = MDBoxLayout(
            orientation="horizontal",
            spacing=AppTheme.TOP_BAR_SPACING,
        )

        # Show a back button on detail screens, otherwise the app logo
        if on_back is not None:
            leading_section.add_widget(self._build_back_button(on_back))
        else:
            leading_section.add_widget(self._build_logo_badge())

        leading_section.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )
        return leading_section

    def _build_back_button(self, on_back: Callable[[], None]) -> MDIconButton:
        """
        Builds the back navigation button.

        Args:
            on_back: Callback invoked when the button is pressed.

        Returns:
            Configured back button.
        """
        back_button = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_PRIMARY_COLOR,
        )
        back_button.bind(on_release=lambda *_: on_back())
        return back_button

    def _build_logo_badge(self) -> MDIconButton:
        """
        Builds the branded app logo badge shown on primary screens.

        Returns:
            Configured logo icon badge.
        """
        return MDIconButton(
            icon="compass-outline",
            md_bg_color=AppTheme.ACCENT_MUTED_COLOR,
            theme_text_color="Custom",
            text_color=AppTheme.ACCENT_COLOR,
            disabled=True,
        )

    def _build_trailing_button(
        self,
        trailing_icon: str,
        on_trailing_pressed: Callable[[], None] | None,
    ) -> MDIconButton:
        """
        Builds the trailing action button.

        Args:
            trailing_icon: Material icon name for the button.
            on_trailing_pressed: Callback invoked when the button is pressed.

        Returns:
            Configured trailing icon button.
        """
        trailing_button = MDIconButton(
            icon=trailing_icon,
            md_bg_color=AppTheme.ELEVATED_SURFACE_COLOR,
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_SECONDARY_COLOR,
        )
        if on_trailing_pressed is not None:
            trailing_button.bind(on_release=lambda *_: on_trailing_pressed())
        return trailing_button
