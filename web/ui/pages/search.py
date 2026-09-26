"""
Search page: just the shared search experience, pre-filled from the URL.
"""

from web.meta import SEARCH_PAGE_TITLE
from web.ui.components.search_experience import SearchExperience
from web.ui.pages.base import BasePage


class SearchPage(BasePage):
    """
    Shows the search field, chips, and catalog, filtered by URL params.
    """

    page_title = SEARCH_PAGE_TITLE

    def build_page_children(self) -> list:
        query = self.request.GET.get("q", "")
        category = self.request.GET.get("category", "")

        return [SearchExperience(query=query, category=category)]
