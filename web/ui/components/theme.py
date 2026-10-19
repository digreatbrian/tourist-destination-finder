"""
Centralized design tokens for the application UI.

Referenced directly from component style dicts (e.g. `Theme.accent_color`)
instead of hardcoding colors or spacing anywhere else. Soft, blended
gradients over a light tinted canvas give the app a modern, native feel.
"""


class Theme:
    """
    Stores application-wide colors, spacing, and sizing values.
    """

    # Screen tokens
    screen_bg_color = "#F4F6FB"
    screen_padding_x = "18px"
    screen_padding_y = "14px"
    section_spacing = "14px"

    # Surface tokens
    surface_color = "#FFFFFF"
    surface_border_color = "rgba(15, 23, 42, 0.07)"
    surface_elevated_color = "#F8FAFE"
    glass_bg_color = "rgba(255, 255, 255, 0.78)"
    glass_blur = "saturate(180%) blur(18px)"
    scrim_color = "rgba(15, 23, 42, 0.38)"

    # Text tokens
    text_primary_color = "#0F172A"
    text_secondary_color = "#475569"
    text_tertiary_color = "#94A3B8"

    # Accent tokens
    accent_color = "#3B6CF6"
    accent_muted_color = "#EAF0FF"
    accent_gradient = "linear-gradient(135deg, #3B82F6 0%, #7C5CFA 55%, #C25CF5 100%)"
    accent_soft_gradient = (
        "linear-gradient(135deg, rgba(59,130,246,0.14) 0%, "
        "rgba(124,92,250,0.14) 55%, rgba(34,211,238,0.14) 100%)"
    )
    success_color = "#10B981"
    danger_color = "#EF4444"
    danger_muted_color = "#FEECEC"

    image_credit_bg_color = "rgba(15, 23, 42, 0.55)"
    image_credit_text_color = "#FFFFFF"
    image_overlay = "linear-gradient(180deg, rgba(15,23,42,0) 45%, rgba(15,23,42,0.55) 100%)"

    # Card tokens
    card_radius = "24px"
    card_padding = "16px"
    card_spacing = "10px"
    card_image_height = "190px"
    card_badge_color = "rgba(255, 255, 255, 0.88)"
    card_shadow = "0 1px 2px rgba(15, 23, 42, 0.04), 0 10px 28px rgba(15, 23, 42, 0.07)"
    float_shadow = "0 10px 30px rgba(59, 108, 246, 0.35), 0 2px 6px rgba(15, 23, 42, 0.12)"
    sheet_shadow = "0 -12px 48px rgba(15, 23, 42, 0.18)"

    # AI assistant tokens
    ai_mode_button_padding = "7px 14px"
    ai_message_padding = "11px 14px"
    ai_fab_size = "56px"

    # Search field tokens
    search_field_height = "54px"
    search_field_radius = "999px"
    search_field_padding = "18px"

    # Top bar tokens
    top_bar_height = "64px"
    top_bar_spacing = "10px"
    top_bar_bg_color = glass_bg_color

    # Bottom navigation tokens
    nav_bar_height = "68px"
    nav_bar_radius = "999px"
    nav_bar_margin = "12px"
    nav_bar_gap = "6px"
    nav_bar_padding = "8px"

    # Chip tokens
    chip_height = "38px"
    chip_radius = "999px"

    # Size
    max_content_width = "720px"
