"""
Centralized design tokens for the application UI.
"""

from kivy.metrics import dp


class AppTheme:
    """
    Stores application-wide colors, spacing, and sizing values.
    """

    # Screen-level tokens
    SCREEN_BACKGROUND_COLOR = (0.96, 0.97, 0.99, 1)
    SCREEN_HORIZONTAL_PADDING = dp(18)
    SCREEN_VERTICAL_PADDING = dp(16)
    SECTION_SPACING = dp(14)

    # Surface tokens
    SURFACE_COLOR = (1, 1, 1, 1)
    SURFACE_BORDER_COLOR = (0.87, 0.89, 0.94, 1)
    ELEVATED_SURFACE_COLOR = (0.98, 0.99, 1, 1)

    # Text tokens
    TEXT_PRIMARY_COLOR = (0.09, 0.1, 0.16, 1)
    TEXT_SECONDARY_COLOR = (0.43, 0.45, 0.52, 1)
    TEXT_TERTIARY_COLOR = (0.58, 0.61, 0.69, 1)

    # Accent tokens
    ACCENT_COLOR = (0.0, 0.48, 1.0, 1)
    ACCENT_MUTED_COLOR = (0.88, 0.94, 1.0, 1)

    # Card tokens
    CARD_CORNER_RADIUS = dp(22)
    CARD_HEIGHT = dp(176)
    CARD_PADDING = dp(16)
    CARD_SPACING = dp(8)

    # Search field tokens
    SEARCH_FIELD_HEIGHT = dp(52)
    SEARCH_FIELD_RADIUS = dp(16)
    SEARCH_FIELD_PADDING = dp(14)

    # Bottom navigation tokens
    NAV_BAR_HEIGHT = dp(72)
    NAV_BAR_RADIUS = dp(24)
    NAV_BAR_PADDING = dp(8)
    NAV_BAR_MARGIN_TOP = dp(8)

    # Widget size tokens
    CHIP_HEIGHT = dp(34)
    CHIP_RADIUS = dp(12)