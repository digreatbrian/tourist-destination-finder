"""
Application routing and screen registration.
"""

from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.saved_screen import SavedScreen
from screens.search_screen import SearchScreen
from theme import AppTheme
from widgets.destination_card import DestinationCard
from widgets.ios_bottom_navigation import IOSBottomNavigation


HOME_FEATURED_DESTINATIONS = (
    {
        "title": "Santorini Escape",
        "subtitle": "Greece • Coastal",
        "description": "Whitewashed villages, blue domes, and sunset views over the caldera.",
    },
    {
        "title": "Kyoto Gardens",
        "subtitle": "Japan • Culture",
        "description": "Temples, tea houses, and peaceful gardens with seasonal colors.",
    },
)


class HomeScreen(MDScreen):
    """
    Presents the home dashboard with featured destinations.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the home screen and UI layout.
        """
        super().__init__(**kwargs)
        self.name = "home"

        # Add the primary vertical layout
        self.add_widget(self._build_root_layout())

    def switch_to_screen(self, screen_name: str) -> None:
        """
        Navigates to another screen.

        Args:
            screen_name: Registered destination screen name.
        """
        self.manager.current = screen_name

    def _build_root_layout(self) -> MDBoxLayout:
        """
        Builds the root layout for the home screen.

        Returns:
            Configured vertical root layout.
        """
        root_layout = MDBoxLayout(
            orientation="vertical",
            padding=(
                AppTheme.SCREEN_HORIZONTAL_PADDING,
                AppTheme.SCREEN_VERTICAL_PADDING,
                AppTheme.SCREEN_HORIZONTAL_PADDING,
                AppTheme.SCREEN_VERTICAL_PADDING,
            ),
            spacing=AppTheme.SECTION_SPACING,
        )
        self.md_bg_color = AppTheme.SCREEN_BACKGROUND_COLOR

        # Add title and subtitle text
        root_layout.add_widget(self._build_header())

        # Add a scrollable featured destinations section
        root_layout.add_widget(self._build_featured_content())

        # Add the bottom navigation control
        root_layout.add_widget(
            IOSBottomNavigation(current_tab="home", on_tab_selected=self.switch_to_screen)
        )

        return root_layout

    def _build_header(self) -> MDBoxLayout:
        """
        Builds the home header block.

        Returns:
            Configured header layout.
        """
        header_layout = MDBoxLayout(orientation="vertical", adaptive_height=True)

        # Add the main page heading
        header_layout.add_widget(
            MDLabel(
                text="Discover Your Next Getaway",
                font_style="H5",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )

        # Add the supporting subtitle text
        header_layout.add_widget(
            MDLabel(
                text="iOS-inspired travel browsing with calm, clean cards.",
                font_style="Body2",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_SECONDARY_COLOR,
                adaptive_height=True,
            )
        )

        return header_layout

    def _build_featured_content(self) -> ScrollView:
        """
        Builds the scrollable list of featured destination cards.

        Returns:
            Configured scroll view with card content.
        """
        scroll_view = ScrollView(do_scroll_x=False)
        content_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=AppTheme.SECTION_SPACING,
        )

        # Add the section heading
        content_layout.add_widget(
            MDLabel(
                text="Featured",
                font_style="Subtitle1",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )

        # Add one card for each featured destination
        for destination in HOME_FEATURED_DESTINATIONS:
            content_layout.add_widget(
                DestinationCard(
                    title=destination["title"],
                    subtitle=destination["subtitle"],
                    description=destination["description"],
                    action_text="Explore",
                )
            )

        scroll_view.add_widget(content_layout)
        return scroll_view


class AppRouter:
    """
    Owns screen registration and route setup.
    """

    def __init__(self, container) -> None:
        self.container = container

    def build_root(self) -> MDScreenManager:
        """
        Builds and returns the root screen manager.

        Returns:
            Registered application screen manager.
        """
        manager = MDScreenManager()

        # Add screens
        manager.add_widget(HomeScreen())
        manager.add_widget(SearchScreen(destination_service=self.container.destination_service))
        manager.add_widget(SavedScreen(destination_service=self.container.destination_service))

        # Return the manager
        return manager
