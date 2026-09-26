"""
Bottom toast that briefly confirms an action, then fades out on its
own via CSS keyframes — no client JavaScript or extra round trip.
"""

from duck.html.components.container import Container

from web.ui.components.theme import Theme


class Snackbar(Container):
    """
    Fixed-position toast, hidden until `show()` is called.

    Any click handler that calls `show()` must also list this
    component in its `update_targets` so the new message reaches
    the client.
    """

    def on_create(self):
        super().on_create()

        self._flip = False
        self.style.update({"display": "none"})

    def show(self, message: str):
        """
        Displays `message`, replaying the fade animation on every call.
        """
        self._flip = not self._flip
        self.text = message
        self.style.update(self.visible_style())

    def visible_style(self) -> dict:
        """
        Returns the style dict for a visible toast.

        Alternates between two identical keyframe animations so the
        browser always replays the fade-out, even for repeated calls.
        """
        animation_name = "duck-snackbar-a" if self._flip else "duck-snackbar-b"

        return {
            "display": "flex",
            "position": "fixed",
            "left": "50%",
            "bottom": f"calc({Theme.nav_bar_height} + {Theme.nav_bar_margin} * 2 + 14px)",
            "transform": "translateX(-50%)",
            "padding": "12px 22px",
            "border-radius": "12px",
            "background": Theme.text_primary_color,
            "color": "#fff",
            "font-size": "0.85rem",
            "font-weight": "600",
            "box-shadow": "0 12px 30px rgba(18, 26, 51, 0.25)",
            "z-index": "50",
            "pointer-events": "none",
            "animation": f"{animation_name} 2.4s ease forwards",
        }
