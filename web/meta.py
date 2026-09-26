"""
Centralized application metadata and UI copy.

Single source of truth for app identity, page titles, and static copy
so components stay reusable and no user-facing string is hardcoded.
"""

# App identity
APP_NAME = "Tour Zimbabwe"
APP_TAGLINE = "Discover Zimbabwe"
APP_TAGLINE_SUBTITLE = "Falls, wildlife, and ancient ruins — all in one place."
APP_LOGO_PATH = "images/duck-logo.png"

# Page titles
HOME_PAGE_TITLE = f"{APP_NAME} — Home"
SEARCH_PAGE_TITLE = f"{APP_NAME} — Search"
SAVED_PAGE_TITLE = f"{APP_NAME} — Saved"

# Search & results copy
SEARCH_PLACEHOLDER = "Search destinations or cities"
SEARCH_EMPTY_MESSAGE = "No destinations match your search."
SAVED_HEADING = "Saved places"
SAVED_EMPTY_MESSAGE = "No saved destinations yet — tap ♡ on any place to save it."
BACK_LABEL = "Back"
NOT_FOUND_MESSAGE = "Destination not found."

# Bottom navigation: (route name, active icon, inactive icon, label)
NAV_ITEMS = [
    ("home", "bi-house-fill", "bi-house", "Home"),
    ("search", "bi-search", "bi-search", "Search"),
    ("saved", "bi-heart-fill", "bi-heart", "Saved"),
]

# Top bar overflow menu
MENU_ITEMS = ["Settings", "About", "Help & Support", "Share App"]
SNACKBAR_COMING_SOON = "Coming soon"
