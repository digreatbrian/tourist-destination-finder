"""
Reusable animated skeleton placeholder widget.
"""

from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget

from theme import AppTheme


class SkeletonLoader(Widget):
    """
    Displays a pulsing rounded rectangle used as a modern loading placeholder.
    """

    def __init__(self, radius: list[float] | None = None, **kwargs) -> None:
        """
        Initializes and starts the skeleton pulse animation.

        Args:
            radius: Corner radius applied to the skeleton shape.
        """
        super().__init__(**kwargs)
        self.radius = radius or [0, 0, 0, 0]

        # Draw the base skeleton rectangle
        with self.canvas:
            self._fill_color = Color(*AppTheme.SKELETON_BASE_COLOR)
            self._rectangle = RoundedRectangle(radius=self.radius)

        # Keep the drawn shape synced with widget geometry
        self.bind(pos=self._sync_shape, size=self._sync_shape)

        # Start the looping shimmer animation
        self._start_pulse_animation()

    def stop(self) -> None:
        """
        Stops the pulse animation and fades the skeleton shape out.
        """
        Animation.cancel_all(self._fill_color)
        Animation(a=0, duration=AppTheme.SKELETON_PULSE_DURATION / 2).start(self._fill_color)

    def _sync_shape(self, *_) -> None:
        """
        Syncs the drawn rectangle with the widget's current geometry.
        """
        self._rectangle.pos = self.pos
        self._rectangle.size = self.size

    def _start_pulse_animation(self) -> None:
        """
        Runs a looping opacity pulse to simulate a shimmering skeleton.
        """
        pulse = Animation(
            a=AppTheme.SKELETON_PULSE_MIN_ALPHA, duration=AppTheme.SKELETON_PULSE_DURATION
        ) + Animation(a=1, duration=AppTheme.SKELETON_PULSE_DURATION)
        pulse.repeat = True
        pulse.start(self._fill_color)
