"""
Centralized design tokens for the application UI.

Referenced directly from component style dicts (e.g. `Theme.accent_color`)
instead of hardcoding colors or spacing anywhere else. Sizes are tuned a
notch larger than typical desktop defaults for a comfortable mobile feel.
"""


class Theme:
    """
    Stores application-wide colors, spacing, and sizing values.
    """

    # Screen tokens
    screen_bg_color = "#F0F5FF"
    screen_padding_x = "20px"
    screen_padding_y = "18px"
    section_spacing = "16px"

    # Surface tokens
    surface_color = "#FFFFFF"
    surface_border_color = "#D9E6F7"
    surface_elevated_color = "#FAFCFF"

    # Text tokens
    text_primary_color = "#121A33"
    text_secondary_color = "#576680"
    text_tertiary_color = "#8799B0"

    # Accent tokens
    accent_color = "#008FFA"
    accent_muted_color = "#DEF2FF"
    success_color = "#00B373"

    # Card tokens
    card_radius = "24px"
    card_padding = "18px"
    card_spacing = "10px"
    card_image_height = "168px"
    card_badge_color = "rgba(255, 255, 255, 0.92)"

    # Search field tokens
    search_field_height = "60px"
    search_field_radius = "20px"
    search_field_padding = "16px"

    # Top bar tokens
    top_bar_height = "76px"
    top_bar_spacing = "10px"
    top_bar_bg_color = accent_color

    # Bottom navigation tokens
    nav_bar_height = "80px"
    nav_bar_radius = "28px"
    nav_bar_margin = "10px"
    nav_bar_gap = "8px"
    nav_bar_padding = "10px"

    # Chip tokens
    chip_height = "42px"
    chip_radius = "18px"
    
    # Size
    max_content_width = "720px"
