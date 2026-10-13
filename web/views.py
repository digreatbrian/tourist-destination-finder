"""
Views for the destination discovery app.

Each view returns a Page component directly — Duck's Lively engine
handles rendering, so there are no separate template files.
"""

from web.ui.pages.detail import DestinationDetailPage
from web.ui.pages.home import HomePage
from web.ui.pages.saved import SavedPage
from web.ui.pages.search import SearchPage


def home(request):
    """
    Renders the home page.
    """
    return HomePage(request=request)


def search(request):
    """
    Renders the search results page.
    """
    return SearchPage(request=request)


def saved(request):
    """
    Renders the saved destinations page.
    """
    return SavedPage(request=request)


def destination_detail(request):
    """
    Renders a single destination's detail page.
    """
    return DestinationDetailPage(request=request)
