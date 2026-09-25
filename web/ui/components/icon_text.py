"""
Inline icon + text pairing, used for location lines and similar labels.
"""

from duck.html.components.container import FlexContainer
from duck.html.components.icon import Icon
from duck.html.components.paragraph import Paragraph


class IconText(FlexContainer):
    """
    Renders a small Bootstrap icon followed by a line of text.
    """

    def on_create(self):
        super().on_create()
        
        icon_class = self.get_kwarg_or_raise("icon_class")
        text = self.get_kwarg_or_raise("text")
        text_style = self.kwargs.get("text_style", {})
        icon_style = self.kwargs.get("icon_style", {})
        
        # Reset self text
        self.text = ""
        
        # Update the style
        self.style.update({
            "display": "flex",
            "align-items": "center",
            "gap": "6px",
        })

        icon = Icon(klass=f"bi {icon_class}", style={"font-size": "0.9rem", **icon_style})
        label = Paragraph(text=text, style={"margin": "0", **text_style})
        
        self.add_children([icon, label])
