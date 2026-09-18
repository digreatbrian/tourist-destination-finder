"""
Search screen UI with iOS-inspired styling and reusable widgets.
"""

from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from models.destination import Destination
from theme import AppTheme
from widgets.app_top_bar import AppTopBar
from widgets.destination_card import DestinationCard
from widgets.ios_bottom_navigation import IOSBottomNavigation


SEARCH_FILTER_CHIPS = (
    "Popular",
    "Beach",
    "City Breaks",
    "Nature",
    "Luxury",
    "Family",
    "Adventure",
    "Culture",
)


class SearchScreen(MDScreen):
    """
    Displays discover/search-focused destination cards.
    """

    def __init__(self, destination_service, **kwargs) -> None:
        """
        Initializes the screen with dependencies and base UI.

        Args:
            destination_service: Service used to read destination records.
        """
        super().__init__(**kwargs)
        self.name = "search"
        self.destination_service = destination_service
        self.results_layout: MDBoxLayout | None = None
        self.placeholder_label: MDLabel | None = None

        # Add the main screen layout
        self.add_widget(self._build_root_layout())

    def on_pre_enter(self, *args) -> None:
        """
        Refreshes destination cards before the screen appears.
        """
        super().on_pre_enter(*args)
        self.populate_destination_cards()

    def switch_to_screen(self, screen_name: str) -> None:
        """
        Navigates to another registered screen.

        Args:
            screen_name: Registered screen name to display.
        """
        self.manager.current = screen_name

    def view_destination(self, destination: Destination) -> None:
        """
        Displays full details for the selected destination.

        Args:
            destination: Destination selected from the results list.
        """
        detail_screen = self.manager.get_screen("destination_detail")
        detail_screen.display_destination(
            destination={
                "title": destination.name,
                "subtitle": f"{destination.location} - {destination.category}",
                "description": destination.description
                or "Curated destination idea ready to explore.",
                "image_url": destination.image_url,
            },
            return_screen_name="search",
        )
        self.manager.current = "destination_detail"

    def populate_destination_cards(self) -> None:
        """
        Populates the destination card list using service data.
        """
        if self.results_layout is None:
            return

        # Clear previously rendered cards
        self.results_layout.clear_widgets()

        # Fetch catalog data for display
        destinations = self.destination_service.get_destinations()

        # Render cards for each available destination
        if destinations:
            for destination in destinations:
                self.results_layout.add_widget(self._build_destination_card(destination))
            return

        # Show an empty-state message when no results are available
        if self.placeholder_label is not None:
            self.placeholder_label.text = "No destinations available yet."
            self.results_layout.add_widget(self.placeholder_label)

    def _build_root_layout(self) -> MDBoxLayout:
        """
        Builds the root layout for the search screen.

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

        # Add the top navigation bar
        root_layout.add_widget(AppTopBar(title="Explore"))

        # Add the screen heading
        root_layout.add_widget(self._build_header())

        # Add faux search field and filter chips
        root_layout.add_widget(self._build_search_field())
        root_layout.add_widget(self._build_filter_row())

        # Add scrollable destination content
        root_layout.add_widget(self._build_results_area())

        # Add the shared bottom navigation bar
        root_layout.add_widget(
            IOSBottomNavigation(current_tab="search", on_tab_selected=self.switch_to_screen)
        )

        return root_layout

    def _build_header(self) -> MDBoxLayout:
        """
        Builds the title and subtitle header.

        Returns:
            Configured header layout.
        """
        header_layout = MDBoxLayout(orientation="vertical", adaptive_height=True)
        header_layout.add_widget(
            MDLabel(
                text="Explore Destinations",
                font_style="H5",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_PRIMARY_COLOR,
                adaptive_height=True,
                bold=True,
            )
        )
        header_layout.add_widget(
            MDLabel(
                text="Discover places curated for your next unforgettable trip.",
                font_style="Body2",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_SECONDARY_COLOR,
                adaptive_height=True,
            )
        )
        return header_layout

    def _build_search_field(self) -> MDCard:
        """
        Builds a stylized static search input shell.

        Returns:
            Configured search field card.
        """
        search_field = MDCard(
            size_hint_y=None,
            height=AppTheme.SEARCH_FIELD_HEIGHT,
            radius=[AppTheme.SEARCH_FIELD_RADIUS] * 4,
            md_bg_color=AppTheme.SURFACE_COLOR,
            line_color=AppTheme.SURFACE_BORDER_COLOR,
            padding=AppTheme.SEARCH_FIELD_PADDING,
            elevation=0,
        )
        search_field.add_widget(
            MDLabel(
                text="Search places, countries, or experiences",
                font_style="Body2",
                theme_text_color="Custom",
                text_color=AppTheme.TEXT_TERTIARY_COLOR,
            )
        )
        return search_field

    def _build_filter_row(self) -> ScrollView:
        """
        Builds a horizontal row of filter chips.

        Returns:
            Configured horizontal scroll view with chips.
        """
        chips_scroll = ScrollView(
            do_scroll_y=False,
            do_scroll_x=True,
            size_hint_y=None,
            height=AppTheme.CHIP_HEIGHT + AppTheme.SECTION_SPACING,
            bar_width=0,
        )
        chip_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            adaptive_height=True,
            spacing=AppTheme.CARD_SPACING,
            padding=(0, 0, AppTheme.CARD_SPACING, 0),
        )
        chip_layout.bind(minimum_width=chip_layout.setter("width"))

        # Add visual chips representing category filters
        for filter_name in SEARCH_FILTER_CHIPS:
            chip_layout.add_widget(self._build_filter_chip(filter_name))

        chips_scroll.add_widget(chip_layout)
        return chips_scroll

    def _build_filter_chip(self, filter_name: str) -> MDCard:
        """
        Builds a single rounded filter chip.

        Args:
            filter_name: Display text for the chip.

        Returns:
            Configured chip card.
        """
        chip_card = MDCard(
            size_hint=(None, None),
            height=AppTheme.CHIP_HEIGHT,
            width=max(dp(108), len(filter_name) * dp(7.5)),
            radius=[AppTheme.CHIP_RADIUS] * 4,
            md_bg_color=AppTheme.ACCENT_MUTED_COLOR,
            elevation=0,
            padding=(AppTheme.SEARCH_FIELD_PADDING, 0, AppTheme.SEARCH_FIELD_PADDING, 0),
        )
        chip_card.add_widget(
            MDLabel(
                text=filter_name,
                theme_text_color="Custom",
                text_color=AppTheme.ACCENT_COLOR,
                halign="center",
                valign="middle",
            )
        )
        return chip_card

    def _build_results_area(self) -> ScrollView:
        """
        Builds the destination results list container.

        Returns:
            Configured scroll view with dynamic results area.
        """
        results_scroll = ScrollView(do_scroll_x=False)
        self.results_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=AppTheme.SECTION_SPACING,
        )
        self.placeholder_label = MDLabel(
            text="Loading destinations...",
            font_style="Body2",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_SECONDARY_COLOR,
            adaptive_height=True,
        )

        # Add a placeholder status line
        self.results_layout.add_widget(self.placeholder_label)

        results_scroll.add_widget(self.results_layout)
        return results_scroll

    def _build_destination_card(self, destination: Destination) -> DestinationCard:
        """
        Builds a destination preview card from model data.

        Args:
            destination: Destination model used for card content.

        Returns:
            Configured destination card widget.
        """
        subtitle = f"{destination.location} - {destination.category}"
        description = destination.description or "Curated destination idea ready to explore."
        return DestinationCard(
            title=destination.name,
            subtitle=subtitle,
            description=description,
            image_url=destination.image_url,
            action_text="View",
            on_view=lambda destination=destination: self.view_destination(destination),
        )
