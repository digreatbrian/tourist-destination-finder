"""
Reusable async image widget with a skeleton loading placeholder.
"""

import os

from kivy.core.image import Image as CoreImage
from kivy.loader import Loader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage

from widgets.skeleton_loader import SkeletonLoader


# Path to a transparent 1x1 placeholder used while an image loads
LOADING_PLACEHOLDER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "loading_placeholder.png",
)

# Replace Kivy's default loading spinner with a transparent placeholder,
# since the skeleton widget below provides the actual loading feedback
Loader.loading_image = CoreImage(LOADING_PLACEHOLDER_PATH)


class SkeletonImage(FloatLayout):
    """
    Displays an async image with a skeleton placeholder while it loads.
    """

    def __init__(self, source: str, radius: list[float] | None = None, **kwargs) -> None:
        """
        Initializes the async image and its skeleton placeholder.

        Args:
            source: Image URL to load.
            radius: Corner radius applied to the skeleton placeholder.
        """
        super().__init__(**kwargs)
        self.radius = radius or [0, 0, 0, 0]

        # Show a skeleton placeholder until the image finishes loading
        self._skeleton = SkeletonLoader(radius=self.radius)
        self.add_widget(self._skeleton)

        # Load the destination image asynchronously
        self._image = AsyncImage(source=source, allow_stretch=True, keep_ratio=False)
        self._image.bind(texture=self._on_texture_loaded)
        self.add_widget(self._image)

    def _on_texture_loaded(self, _instance: AsyncImage, texture) -> None:
        """
        Hides the skeleton placeholder once the image texture is ready.

        Args:
            _instance: AsyncImage instance that triggered the event.
            texture: Loaded image texture, or None while still loading.
        """
        if texture is not None:
            self._skeleton.stop()
