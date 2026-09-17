"""
Centralized design tokens for the application UI.
"""

from kivy.metrics import dp


class AppTheme:
    """
    Stores application-wide colors, spacing, and sizing values.
    """

    # Screen-level tokens
    SCREEN_BACKGROUND_COLOR = (0.94, 0.96, 1, 1)
    SCREEN_HORIZONTAL_PADDING = dp(18)
    SCREEN_VERTICAL_PADDING = dp(16)
    SECTION_SPACING = dp(14)

    # Surface tokens
    SURFACE_COLOR = (1, 1, 1, 1)
    SURFACE_BORDER_COLOR = (0.85, 0.9, 0.97, 1)
    ELEVATED_SURFACE_COLOR = (0.98, 0.99, 1, 1)

    # Text tokens
    TEXT_PRIMARY_COLOR = (0.07, 0.1, 0.2, 1)
    TEXT_SECONDARY_COLOR = (0.34, 0.4, 0.5, 1)
    TEXT_TERTIARY_COLOR = (0.53, 0.6, 0.69, 1)

    # Accent tokens
    ACCENT_COLOR = (0.0, 0.56, 0.98, 1)
    ACCENT_MUTED_COLOR = (0.87, 0.95, 1.0, 1)
    SUCCESS_COLOR = (0.0, 0.7, 0.45, 1)

    # Card tokens
    CARD_CORNER_RADIUS = dp(24)
    CARD_HEIGHT = dp(292)
    CARD_PADDING = dp(16)
    CARD_SPACING = dp(10)
    CARD_IMAGE_HEIGHT = dp(148)
    CARD_OVERLAY_COLOR = (0.03, 0.06, 0.14, 0.35)
    CARD_BADGE_COLOR = (1, 1, 1, 0.9)

    # Search field tokens
    SEARCH_FIELD_HEIGHT = dp(56)
    SEARCH_FIELD_RADIUS = dp(18)
    SEARCH_FIELD_PADDING = dp(14)

    # Bottom navigation tokens
    NAV_BAR_HEIGHT = dp(74)
    NAV_BAR_RADIUS = dp(26)
    NAV_BAR_PADDING = dp(8)
    NAV_BAR_MARGIN_TOP = dp(8)

    # Widget size tokens
    CHIP_HEIGHT = dp(36)
    CHIP_RADIUS = dp(14)