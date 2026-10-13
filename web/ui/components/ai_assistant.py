"""
In-page AI assistant using Duck's Lively component updates.
"""

import logging

from duck.contrib.sync import ensure_async
from duck.html.components.button import Button
from duck.html.components.container import Container, FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.input import Input
from duck.html.components.link import Link
from duck.html.components.paragraph import Paragraph

from web.services import ai as ai_service
from web.ui.components.theme import Theme


logger = logging.getLogger(__name__)


class AIAssistant(Container):
    """
    Lets visitors ask travel questions or request destination recommendations.

    AI calls run from Lively event handlers and patch the answer container
    directly, without adding an app-owned JSON API endpoint.
    """

    def on_create(self):
        super().on_create()

        self.mode = "chat"
        self.prompt = ""
        self.history = []

        self.style.update({
            "display": "flex",
            "flex-direction": "column",
            "gap": "12px",
            "padding": Theme.card_padding,
            "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}",
            "border-radius": Theme.card_radius,
            "box-shadow": Theme.card_shadow,
        })

        self.output = Container(
            style={
                "display": "flex",
                "flex-direction": "column",
                "gap": "10px",
            },
        )
        self.prompt_input = Input(
            type="text",
            name="ai-prompt",
            placeholder="Ask about Zimbabwe destinations or share trip interests",
            maxlength=2000,
            style={
                "flex": "1",
                "width": "100%",
                "border": f"1px solid {Theme.surface_border_color}",
                "border-radius": Theme.search_field_radius,
                "background": Theme.surface_elevated_color,
                "font-size": "1rem",
            },
        )
        self.prompt_input.bind(
            "input",
            self.on_input,
            update_self=False,
        )
        self.submit_button = Button(
            text="Ask AI",
            style={
                "background": Theme.accent_color,
                "color": Theme.surface_color,
                "font-size": "0.95rem",
                "font-weight": "700",
            },
        )
        self.submit_button.bind(
            "click",
            self.on_submit,
            update_targets=[self.output],
            update_self=False,
        )

        self.mode_buttons = FlexContainer(
            style={
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": "8px",
            },
        )
        self.mode_buttons.add_children([
            self.build_mode_button("Ask a question", "chat"),
            self.build_mode_button("Recommend places", "recommendations"),
        ])

        self.add_children([
            Heading(
                type="h2",
                text="Plan with AI",
                style={
                    "margin": "0",
                    "font-size": "1.2rem",
                    "font-weight": "750",
                },
            ),
            Paragraph(
                text=(
                    "Ask how to use the app or find places that fit your "
                    "interests. Suggestions come from the destination catalog."
                ),
                style={
                    "margin": "0",
                    "color": Theme.text_secondary_color,
                    "line-height": "1.5",
                },
            ),
            self.mode_buttons,
            FlexContainer(
                style={
                    "display": "flex",
                    "flex-wrap": "wrap",
                    "gap": "8px",
                    "align-items": "stretch",
                },
                children=[
                    self.prompt_input,
                    self.submit_button,
                ],
            ),
            self.output,
        ])

        if not ai_service.is_configured():
            self.show_message(
                "AI assistance is not configured yet. Set AI_API_KEY on the "
                "server to enable questions and recommendations."
            )

    def build_mode_button(self, label: str, mode: str) -> Button:
        """
        Builds a Lively button for switching the assistant's task.
        """
        button = Button(
            text=label,
            style=self.mode_button_style(mode == self.mode),
        )
        button.bind(
            "click",
            self.build_mode_handler(mode),
            update_targets=[self.mode_buttons],
            update_self=False,
        )
        button.mode = mode
        return button

    def build_mode_handler(self, mode: str):
        """
        Returns an event handler that updates the selected AI task in place.
        """
        async def on_click(component, event, value, ws):
            self.mode = mode
            for button in self.mode_buttons.children:
                button.style.update(
                    self.mode_button_style(button.mode == self.mode)
                )

        return on_click

    @staticmethod
    def mode_button_style(is_active: bool) -> dict:
        """
        Returns shared styling for the assistant task buttons.
        """
        return {
            "padding": Theme.ai_mode_button_padding,
            "border-radius": Theme.chip_radius,
            "background": Theme.accent_color if is_active else Theme.surface_color,
            "border": (
                f"1px solid {Theme.accent_color if is_active else Theme.surface_border_color}"
            ),
            "color": Theme.surface_color if is_active else Theme.text_secondary_color,
            "font-size": "0.85rem",
            "font-weight": "650",
            "cursor": "pointer",
        }

    async def on_input(self, component, event, value, ws):
        """
        Keeps the current prompt on the live component instance.
        """
        self.prompt = str(value or "")[:2000]

    async def on_submit(self, component, event, value, ws):
        """
        Calls the AI service and patches only the answer container.
        """
        prompt = self.prompt.strip()
        if not prompt:
            self.show_message("Enter a question or a few trip interests first.")
            return

        if not ai_service.is_configured():
            self.show_message(
                "AI assistance is not configured yet. Set AI_API_KEY on the "
                "server to enable questions and recommendations."
            )
            return

        try:
            if self.mode == "recommendations":
                recommendations = await ensure_async(
                    ai_service.recommend_destinations
                )(prompt, 5)
                self.show_recommendations(recommendations)
                return

            earlier_messages = self.history[-10:]
            answer = await ensure_async(
                ai_service.answer_travel_question
            )(prompt, earlier_messages)
        except ai_service.AIConfigurationError as error:
            self.show_message(str(error))
            return
        except ai_service.AIServiceError:
            logger.exception("The live AI assistant request failed.")
            self.show_message(
                "AI assistance is temporarily unavailable. Please try again."
            )
            return

        self.history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ])
        self.history = self.history[-10:]
        self.show_chat_history()

    def show_message(self, message: str):
        """
        Replaces the live response area with a status or error message.
        """
        self.output.clear_children()
        self.output.add_child(Paragraph(
            text=message,
            style={
                "margin": "0",
                "color": Theme.text_secondary_color,
                "line-height": "1.5",
            },
        ))

    def show_chat_history(self):
        """
        Renders recent user and assistant messages in the Lively response area.
        """
        self.output.clear_children()
        for message in self.history:
            is_assistant = message["role"] == "assistant"
            self.output.add_child(Paragraph(
                text=message["content"],
                style={
                    "margin": "0",
                    "padding": Theme.ai_message_padding,
                    "border-radius": Theme.search_field_radius,
                    "background": (
                        Theme.accent_muted_color
                        if is_assistant
                        else Theme.surface_elevated_color
                    ),
                    "color": Theme.text_primary_color,
                    "line-height": "1.5",
                },
            ))

    def show_recommendations(self, recommendations: list[dict]):
        """
        Renders catalog recommendations directly into the live component tree.
        """
        self.output.clear_children()
        if not recommendations:
            self.show_message(
                "I couldn't find a close match in the catalog. Try different interests."
            )
            return

        for destination in recommendations:
            self.output.add_child(Heading(
                type="h3",
                text=destination["name"],
                style={
                    "margin": "0",
                    "font-size": "1rem",
                    "font-weight": "700",
                },
            ))
            self.output.add_child(Paragraph(
                text=(
                    f'{destination["category"]} · {destination["location"]}'
                ),
                style={
                    "margin": "0",
                    "color": Theme.text_secondary_color,
                },
            ))
            self.output.add_child(Paragraph(
                text=destination["reason"],
                style={"margin": "0", "line-height": "1.5"},
            ))
            self.output.add_child(Link(
                url=f'/destination?id={destination["destination_id"]}',
                text="View destination",
                style={
                    "color": Theme.accent_color,
                    "font-weight": "650",
                    "text-decoration": "none",
                },
            ))
