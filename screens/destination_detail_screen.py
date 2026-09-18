"""
Destination detail screen showing full destination information.
"""

from collections.abc import Callable

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from theme import AppTheme
from widgets.skeleton_image import SkeletonImage


class DestinationDetailScreen(MDScreen):
    """
    Displays full details for a single destination.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the detail screen and its placeholder layout.
        """
        super().__init__(**kwargs)
        self.name = "destination_detail"
        self.return_screen_name = "search"
        self.title_label: MDLabel | None = None
        self.subtitle_label: MDLabel | None = None
        self.description_label: MDLabel | None = None
        self.hero_container: FloatLayout | None = None
        self._hero_image: SkeletonImage | None = None

        # Add the placeholder root layout
        self.add_widget(self._build_root_layout())

    def display_destination(self, destination: dict, return_screen_name: str = "search") -> None:
        """
        Populates the screen with the given destination's details.

        Args:
            destination: Prepared destination fields (title, subtitle,
                description, image_url).
            return_screen_name: Screen to return to when the back button
                is pressed.
        """
        self.return_screen_name = return_screen_name

        if self.title_label is not None:
            self.title_label.text = destination.get("title", "")

        if self.subtitle_label is not None:
            self.subtitle_label.text = destination.get("subtitle", "")

        if self.description_label is not None:
            self.description_label.text = destination.get(
                "description", "No description available yet."
            )

        self._refresh_hero_image(destination.get("image_url", ""))

    def go_back(self) -> None:
        """
        Returns to the screen the detail view was opened from.
        """
        self.manager.current = self.return_screen_name

    def _refresh_hero_image(self, image_url: str) -> None:
        """
        Rebuilds the hero image for the currently displayed destination.

        Args:
            image_url: Destination image URL to display.
        """
        if self.hero_container is None:
            return

        # Remove the previous hero image before rendering a new one
        if self._hero_image is not None:
            self.hero_container.remove_widget(self._hero_image)

        # Insert the new hero image behind the floating buttons
        self._hero_image = SkeletonImage(source=image_url, size_hint=(1, 1))
        self.hero_container.add_widget(
            self._hero_image, index=len(self.hero_container.children)
        )

    def _build_root_layout(self) -> ScrollView:
        """
        Builds the scrollable root layout for the detail screen.

        Returns:
            Configured scroll view wrapping the full detail content.
        """
        self.md_bg_color = AppTheme.SCREEN_BACKGROUND_COLOR

        root_scroll = ScrollView(do_scroll_x=False)
        root_layout = MDBoxLayout(orientation="vertical", adaptive_height=True)

        # Add the hero image with floating navigation controls
        root_layout.add_widget(self._build_hero_section())

        # Add the destination information section
        root_layout.add_widget(self._build_info_section())

        root_scroll.add_widget(root_layout)
        return root_scroll

    def _build_hero_section(self) -> FloatLayout:
        """
        Builds the hero image section with floating back and save buttons.

        Returns:
            Configured hero image layout.
        """
        self.hero_container = FloatLayout(
            size_hint_y=None,
            height=AppTheme.DETAIL_HERO_HEIGHT,
        )
        self._hero_image = SkeletonImage(source="", size_hint=(1, 1))
        self.hero_container.add_widget(self._hero_image)

        # Add a floating back button over the hero image
        self.hero_container.add_widget(
            self._build_floating_button(
                icon="arrow-left",
                pos_hint={"x": 0.04, "top": 0.94},
                on_press=self.go_back,
            )
        )

        # Add a floating bookmark button over the hero image
        self.hero_container.add_widget(
            self._build_floating_button(
                icon="bookmark-outline",
                pos_hint={"right": 0.96, "top": 0.94},
            )
        )

        return self.hero_container

    def _build_floating_button(
        self,
        icon: str,
        pos_hint: dict,
        on_press: Callable[[], None] | None = None,
    ) -> MDIconButton:
        """
        Builds a circular floating icon button rendered over the hero image.

        Args:
            icon: Material icon name shown on the button.
            pos_hint: Positioning hint relative to the hero image.
            on_press: Optional callback invoked when the button is pressed.

        Returns:
            Configured floating icon button.
        """
        floating_button = MDIconButton(
            icon=icon,
            md_bg_color=AppTheme.CARD_BADGE_COLOR,
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_PRIMARY_COLOR,
            pos_hint=pos_hint,
            size_hint=(None, None),
            size=(AppTheme.DETAIL_FLOATING_BUTTON_SIZE, AppTheme.DETAIL_FLOATING_BUTTON_SIZE),
        )
        if on_press is not None:
            floating_button.bind(on_release=lambda *_: on_press())
        return floating_button

    def _build_info_section(self) -> MDBoxLayout:
        """
        Builds the destination information section below the hero image.

        Returns:
            Configured information section layout.
        """
        info_section = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=(
                AppTheme.SCREEN_HORIZONTAL_PADDING,
                AppTheme.SCREEN_VERTICAL_PADDING,
                AppTheme.SCREEN_HORIZONTAL_PADDING,
                AppTheme.SCREEN_VERTICAL_PADDING,
            ),
            spacing=AppTheme.DETAIL_CONTENT_SPACING,
        )

        # Build and store the populated text labels
        self.title_label = self._build_title_label()
        self.subtitle_label = self._build_subtitle_label()
        self.description_label = self._build_description_label()

        info_section.add_widget(self.title_label)
        info_section.add_widget(self.subtitle_label)
        info_section.add_widget(self.description_label)
        info_section.add_widget(self._build_action_bar())

        return info_section

    def _build_title_label(self) -> MDLabel:
        """
        Builds the destination title label.

        Returns:
            Configured title label.
        """
        return MDLabel(
            text="",
            font_style="H5",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_PRIMARY_COLOR,
            adaptive_height=True,
            bold=True,
        )

    def _build_subtitle_label(self) -> MDLabel:
        """
        Builds the destination location/category subtitle label.

        Returns:
            Configured subtitle label.
        """
        return MDLabel(
            text="",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=AppTheme.ACCENT_COLOR,
            adaptive_height=True,
            bold=True,
        )

    def _build_description_label(self) -> MDLabel:
        """
        Builds the full destination description label.

        Returns:
            Configured description label.
        """
        return MDLabel(
            text="",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=AppTheme.TEXT_SECONDARY_COLOR,
            adaptive_height=True,
        )

    def _build_action_bar(self) -> MDBoxLayout:
        """
        Builds the primary action bar shown below the description.

        Returns:
            Configured action bar layout.
        """
        action_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=AppTheme.DETAIL_ACTION_BAR_HEIGHT,
            padding=(0, AppTheme.SECTION_SPACING, 0, 0),
        )
        action_bar.add_widget(
            MDRaisedButton(
                text="Save Destination",
                md_bg_color=AppTheme.ACCENT_COLOR,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                elevation=0,
                size_hint=(1, 1),
                radius=[AppTheme.CHIP_RADIUS] * 4,
            )
        )
        return action_bar
