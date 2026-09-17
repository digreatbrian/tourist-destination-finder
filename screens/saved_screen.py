"""
Saved destinations screen with reusable iOS-style components.
"""

from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from models.destination import Destination
from theme import AppTheme
from widgets.destination_card import DestinationCard
from widgets.ios_bottom_navigation import IOSBottomNavigation


class SavedScreen(MDScreen):
    """
    Displays saved destinations in a polished card list.
    """

    def __init__(self, destination_service, **kwargs) -> None:
        """
        Initializes the saved screen and reusable UI layout.

        Args:
            destination_service: Service used to read saved destinations.
        """
        super().__init__(**kwargs)
        self.name = "saved"
        self.destination_service = destination_service
        self.saved_results_layout: MDBoxLayout | None = None
        self.empty_state_label: MDLabel | None = None

        # Add the top-level screen layout
        self.add_widget(self._build_root_layout())

    def on_pre_enter(self, *args) -> None:
        """
        Refreshes saved cards before the screen appears.
        """
        super().on_pre_enter(*args)
        self.populate_saved_cards()

    def switch_to_screen(self, screen_name: str) -> None:
        """
        Navigates to another registered screen.

        Args:
            screen_name: Registered screen name to display.
        """
        self.manager.current = screen_name

    def populate_saved_cards(self) -> None:
        """
        Populates saved destination cards from the service layer.
        """
        if self.saved_results_layout is None:
            return

        # Clear previously rendered saved cards
        self.saved_results_layout.clear_widgets()

        # Fetch saved destinations for display
        saved_destinations = self.destination_service.get_saved_destinations()

        # Add destination cards when saved entries exist
        if saved_destinations:
            for destination in saved_destinations:
                self.saved_results_layout.add_widget(self._build_saved_card(destination))
            return

        # Update empty state visibility text
        if self.empty_state_label is not None:
            self.empty_state_label.text = "No saved destinations yet. Tap View from Explore to save one."
            self.saved_results_layout.add_widget(self.empty_state_label)

    def _build_root_layout(self) -> MDBoxLayout:
        """
        Builds the root layout for the saved screen.

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

        # Add title and subtitle content
        root_layout.add_widget(self._build_header())

        # Add a scrollable saved-destination list
        root_layout.add_widget(self._build_saved_content())

        # Add the shared bottom navigation control
        root_layout.add_widget(
            IOSBottomNavigation(current_tab="saved", on_tab_selected=self.switch_to_screen)
        )

        return root_layout

    def _build_header(self) -> MDBoxLayout:
        """
        Builds the saved screen header block.

        Returns:
            Configured header layout.
        """
        header_layout = MDBoxLayout(orientation="vertical", adaptive_height=True)
        header_layout.add_widget(
            MDLabel(
                text="Saved Trips",
                font_style="H5",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )
        header_layout.add_widget(
            MDLabel(
                text="Your personal collection of places to revisit.",
                font_style="Body2",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_SECONDARY_COLOR,
                adaptive_height=True,
            )
        )
        return header_layout

    def _build_saved_content(self) -> ScrollView:
        """
        Builds the scrollable content wrapper for saved cards.

        Returns:
            Configured scroll view with dynamic saved card area.
        """
        saved_scroll = ScrollView(do_scroll_x=False)
        self.saved_results_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=AppTheme.SECTION_SPACING,
        )
        self.empty_state_label = MDLabel(
            text="Loading saved destinations...",
            font_style="Body2",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_SECONDARY_COLOR,
            adaptive_height=True,
        )

        # Add empty state messaging
        self.saved_results_layout.add_widget(self.empty_state_label)

        saved_scroll.add_widget(self.saved_results_layout)
        return saved_scroll

    def _build_saved_card(self, destination: Destination) -> DestinationCard:
        """
        Builds a saved destination card widget.

        Args:
            destination: Destination model used for card content.

        Returns:
            Configured destination card for saved list display.
        """
        subtitle = f"{destination.location} • {destination.category}"
        description = destination.description or "Saved destination ready for trip planning."
        return DestinationCard(
            title=destination.name,
            subtitle=subtitle,
            description=description,
            action_text="Saved",
        )
