# KivyMD Code Style Guide

> This guide applies specifically to the KivyMD codebase (tourist destination finder app) and must be strictly followed by every contributor on that project.

## Core Principles

Write clean, intentional Python and KV-language code. Code should be easy to read, maintain, and extend — readability and unambiguous structure come first.

Follow existing project patterns before introducing new ones. Prefer consistency over personal preference.

Never remove existing docstrings, comments, or documentation unless they are incorrect or obsolete.

Avoid unnecessary complexity. Do not introduce abstractions, files, classes, functions, or variables unless they provide clear value.

---

## Strict Rules

- Always check for and reuse existing widgets, screens, helpers, or patterns before creating new ones. Never duplicate existing functionality.
- Never introduce invisible, non-standard, or unexpected characters into files (this applies to `.py` and `.kv` files alike).
- Never hardcode metadata such as app name, version, colors, spacing values, API keys, or URLs. Source these from a central config/theme module.
- Always use consistent and predictable patterns across screens and widgets.
- Never create unused files. Only create screens, widgets, or modules that are referenced and required by the project.
- Keep source files small and focused. When a screen or widget file grows too large, split related logic into clearly named modules.
- Never introduce ambiguous or duplicate configuration values (e.g. two constants meaning the same spacing or color).

Example:

```python
# Bad:
class AppTheme:
    accent = "red"
    accent_color = "red"


# Good:
class AppTheme:
    accent_color = "red"
```

Avoid conflicting sources of truth:

```python
# Bad:
class AppTheme:
    accent_color = "red"


THEME = {
    "accent_color": "blue",
}


# Good:
class AppTheme:
    accent_color = "red"
```

---

## Naming

Use predictable naming conventions.

- `snake_case` for functions, variables, and modules.
- `PascalCase` for classes (including KivyMD widget/screen subclasses, e.g. `DestinationCard`, `HomeScreen`).
- Use descriptive names. Avoid vague names such as `data`, `thing`, `item`, or `process` unless the context is obvious.
- Do not prefix methods or globals with `_` unless required by Python (`__init__`, etc.).
- Kivy event-handler callbacks keep Kivy's own naming convention (`on_press`, `on_release`, `on_pre_enter`) — do not rename these.
- Async functions (if used, e.g. for network calls) must start with `async_`.

Examples:

```python
# Good

class DestinationCard(MDCard):
    CARD_RADIUS = "10dp"

    def build_price_tag(self):
        ...


# Avoid

CARD_RADIUS = "10dp"


class DestinationCard(MDCard):
    def _build_price_tag(self):
        ...
```

---

## Formatting

Spacing exists to make structure visible at a glance — treat it as part of the code, not an afterthought.

- Use two blank lines between top-level definitions (classes, top-level functions).
- Use one blank line between logical blocks inside functions and methods.
- Use f-strings instead of `.format()` or `%`.
- Add type hints to all public functions and methods.
- Do not add unnecessary whitespace — no trailing spaces, no padding around `=` for alignment.
- Keep KV files spaced the same way: one blank line between widget rules, indentation strictly 4 spaces, no trailing whitespace.

Example:

```python
# Good

class AppTheme:
    """
    Stores application design tokens.
    """

    primary_color = "#000000"
    surface_color = "#111111"


# Bad

class AppTheme:
    """
    Stores application design tokens.
    """

    primary_color       = "#000000"
    surface_color       = "#111111"
```

### Module Variables and Constants

- Keep module-level constants and configuration values at the top of the file, after imports.
- Group related constants together before classes and functions.
- Use uppercase `SCREAMING_SNAKE_CASE` names for constants.
- Do not hide important configuration values inside functions or classes unless they are class-specific.
- Avoid unnecessary global variables. Only define values globally when they are reused, configurable, or represent a constant.
- Keep global state immutable where possible.

Example:

```python
import os


# API configuration
API_TIMEOUT = 8.0
API_BASE_URL = "https://example.com/api"


# Map defaults
DEFAULT_ZOOM_LEVEL = 12


def fetch_destinations(city: str) -> list:
    """
    Fetches destinations for a given city.

    Args:
        city: Name of the city to search.

    Returns:
        List of destination records.
    """
    ...
```

---

## KivyMD Project Structure

- Keep `main.py` limited to app bootstrap (`MDApp` subclass, `build()`, screen manager setup) — never bury business logic here.
- Screens live in `screens/`, one file per screen (e.g. `screens/home_screen.py`), each defining a single `MDScreen` subclass.
- Reusable widgets live in `widgets/` (e.g. `widgets/destination_card.py`), never redefined inline inside a screen file.
- KV layout files mirror their Python counterpart by name (`home_screen.py` ↔ `home_screen.kv`) and live alongside or in a matching `kv/` directory — pick one convention and apply it everywhere.
- Data access (API calls, local database/storage reads and writes) belongs in `services/`, never directly inside a screen or widget.
- App-wide constants and design tokens (colors, spacing, fonts) live in a single `theme.py` — never raw hex codes or magic spacing values inside screens or widgets.
- `ScreenManager` transitions and screen names are registered in one place (e.g. `screens/manager.py`), not scattered across files.
- Never create a screen, widget, or KV file that isn't referenced by the app.

---

## Code Organization and Readability

Code must be arranged to be clean, beautiful, and easy to understand. Prioritize readability, clear flow, and maintainability.

Organize files in this order:

1. Imports
2. Module-level constants/configuration
3. Classes
4. Class constants
5. Initialization methods (`__init__`, `on_pre_enter`, etc.)
6. Public methods
7. Helper methods

Example:

```python
import os

from kivymd.uix.screen import MDScreen

from services.destinations import fetch_destinations


# Screen configuration
DEFAULT_RESULTS_LIMIT = 20


class SearchScreen(MDScreen):
    """
    Handles destination search and results display.
    """

    # Cache settings
    CACHE_PREFIX = "search"

    def __init__(self, **kwargs):
        """
        Initializes the search screen.
        """
        super().__init__(**kwargs)

        self.cache = {}

    def get_results(self, query: str) -> list:
        """
        Returns cached or freshly fetched search results.

        Args:
            query: Search term entered by the user.

        Returns:
            List of matching destinations.
        """
        # Return cached results when available
        if query in self.cache:
            return self.cache[query]

        # Fetch and cache fresh results
        results = fetch_destinations(query)
        self.cache[query] = results

        # Return the freshly fetched results
        return results
```

### Visual Flow

Keep related code together and arrange methods in a logical order.

Example:

```python
class DestinationService:
    """
    Handles destination data retrieval.
    """

    # Retrieval operations
    def get_destination(self, destination_id: str):
        ...

    def get_destinations(self):
        ...

    # Mutation operations
    def save_destination(self, destination):
        ...

    def update_destination(self, destination):
        ...
```

Avoid randomly ordered methods or compressed code.

---

## Docstrings

Every module, class, and non-trivial function must have a docstring.

Docstrings are the primary documentation layer.

Rules:

- Always use Google-style docstrings.
- Triple quotes must always be on their own lines.
- Docstrings must be readable and sections must be easy to identify.
- Never use inline single-line docstrings.

Bad:

```python
"""Returns a value."""
```

Good:

```python
"""
Returns a calculated value based on the provided input.
"""
```

Docstrings should explain:
- What the code does.
- Why it exists when the purpose is not obvious.
- Arguments and return values where applicable.

Example:

```python
def get_display_name(city: str, fallback: str = "Unknown") -> str:
    """
    Returns a display-friendly name for a city.

    Args:
        city: Raw city name from the data source.
        fallback: Value used when no city name exists.

    Returns:
        Display-ready city name.
    """
    name = city or fallback

    # Return the formatted display name
    return name.title()
```

Required:

| Target | Docstring |
|---|---|
| Module | Required |
| Class | Required |
| Public function | Required |
| Public method | Required |
| Kivy event callback with non-trivial logic | Required |
| Complex private logic | Recommended |
| Simple helpers | Optional |

---

## Comments

Comments are part of the code's readability. Their job is to make structure and intent visible at a glance — especially where several distinct operations (variable assignments, function calls, widget updates) sit next to each other.

Comments serve two purposes:

1. Explain the intent of a meaningful operation.
2. Visually separate distinct operations when several appear in the same logical block.

Rules:

- Every meaningful logical block gets a short comment.
- Comments are written as action phrases ("Fetch the...", "Update the...", "Notify...").
- Avoid comments that only restate obvious syntax.
- Decorative separator comments (bars, dashes, boxes) are forbidden.

Bad:

```python
# -----------------
# Get user location
# -----------------

location = get_user_location()
```

Good:

```python
# Fetch the user's current location
location = get_user_location()
```

### Separating Variables, Calls, and Distinct Operations

When a block mixes variable assignments, function/method calls, and widget updates, give each distinct operation its own short comment — even inside the same loop or block — so the sequence reads clearly without tracing execution mentally.

Good:

```python
def refresh_results(self, query: str):
    """
    Refreshes the results list for a new search query.
    """
    # Fetch fresh results for the query
    results = self.destination_service.get_destinations(query)

    # Clear the previous results from the list
    self.ids.results_list.clear_widgets()

    # Build a card for each result
    for destination in results:
        card = DestinationCard(destination=destination)

        # Add the card to the results list
        self.ids.results_list.add_widget(card)
```

Avoid folding unrelated operations under one broad comment:

```python
# Bad — hides three distinct operations behind one comment
def refresh_results(self, query: str):
    results = self.destination_service.get_destinations(query)
    self.ids.results_list.clear_widgets()
    for destination in results:
        self.ids.results_list.add_widget(DestinationCard(destination=destination))
```

### Comment Hierarchy

Use a higher-level comment for a group of closely related operations that form one conceptual step:

```python
# Reset the search state
self.query = ""
self.results = []
self.page = 1
```

Use individual comments when the statements perform genuinely different operations:

```python
# Show the loading spinner
self.ids.spinner.active = True

# Request destinations from the service layer
results = self.destination_service.get_destinations(query)

# Hide the loading spinner
self.ids.spinner.active = False

# Populate the results list
self.populate_results(results)
```

Do not combine unrelated operations simply to reduce the number of comments — clarity takes priority over comment count.

---

## Functions and Methods

- Keep functions focused on one responsibility.
- Avoid functions that are too large — if a method mixes fetching, transforming, and rendering, split it.
- Extract repeated logic into reusable functions or service methods.
- Do not create unnecessary helper functions.
- Prefer readable code over excessive abstraction.

Bad:

```python
def process():
    ...
```

Good:

```python
def calculate_trip_distance():
    ...
```

---

## Variables

- Avoid unnecessary temporary variables.
- Create variables only when they improve readability or are reused.
- Do not create variables that are used once without improving clarity.
- Name variables unambiguously — prefer `selected_destination` over `dest` or `d`.

Bad:

```python
result = calculate_distance()
return result
```

Good:

```python
# Return the calculated distance
return calculate_distance()
```

---

## Classes

- Classes should represent a clear responsibility (one screen, one widget, one service).
- Avoid creating classes that only wrap one function.
- Keep related methods together.
- Constants should belong to the class when they are class-specific.

Example:

```python
class DestinationCard(MDCard):
    """
    Represents a reusable destination preview card.
    """

    BORDER_RADIUS = "8dp"
```

---

## Imports

Use clean and predictable imports.

Rules:

- Prefer absolute imports.
- Separate standard library, third-party (Kivy/KivyMD), and local imports into three groups.
- Import specific objects instead of entire modules.
- Group related imports together.

Example:

```python
import os

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard

from services.destinations import fetch_destinations
from widgets.destination_card import DestinationCard
```

Avoid:

```python
from widgets import destination_card
```

Prefer:

```python
from widgets.destination_card import DestinationCard
```

---

## Widgets, Screens, and KV Files

- Widgets and screens should receive prepared data instead of directly querying services or the database themselves where practical.
- Keep KV layout definitions (structure/styling) separate from Python logic — logic belongs in the Python class, not in KV `on_press:` one-liners beyond a single method call.
- Break large screens into smaller focused widgets rather than one large monolithic KV rule.
- Give composite widgets unique `id`s within their KV rule when referenced from Python (`self.ids.destination_list`).
- Bind dynamic behavior in `on_pre_enter` / `on_enter` where the screen's widgets are guaranteed to exist, not in `__init__`.

Example:

```python
# Bad

DestinationCard(destination=destination_model)


# Good

DestinationCard(
    destination={
        "name": destination.name,
        "image_url": destination.image_url,
    }
)
```

---

## Final Checklist

Before completing code:

- Does it follow existing project patterns?
- Are docstrings present and Google-style?
- Are comments present and do they clearly separate distinct operations (variables, calls, widget updates)?
- Is spacing consistent (blank lines between definitions and logical blocks, no compressed code)?
- Are names clear and unambiguous?
- Is there duplicated functionality?
- Are there unnecessary variables or functions?
- Are configuration values (colors, spacing, URLs) centralized in `theme.py` / config?
- Is the code easy for another contributor to understand at a glance?
