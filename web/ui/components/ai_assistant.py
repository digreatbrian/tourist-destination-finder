"""
Floating AI assistant: a gradient FAB that opens a compact panel with a
live status pill (thinking / working / done / error), using Duck's Lively
component updates. Progress is pushed to the browser mid-request via
`ws.execute_js`, and the final state is mirrored on the server components.
"""

import json
import logging
import time

from duck.html.components.button import Button
from duck.html.components.container import Container, FlexContainer
from duck.html.components.heading import Heading
from duck.html.components.icon import Icon
from duck.html.components.input import Input
from duck.html.components.link import Link
from duck.html.components.paragraph import Paragraph

from web.services import ai as ai_service
from web.ui.components.theme import Theme


logger = logging.getLogger(__name__)

SUGGESTIONS = [
    ("chat", "Best time to visit Victoria Falls?"),
    ("recommendations", "Wildlife and safaris"),
    ("recommendations", "Quiet mountain escapes"),
]
NOT_CONFIGURED = (
    "AI assistance is not configured yet. Set AI_PROVIDER and AI_API_KEY "
    "in settings to enable questions and recommendations."
)


class AIAssistant(Container):
    """
    Floating assistant for travel questions and catalog recommendations.

    AI calls run from Lively event handlers and patch the panel directly,
    without adding an app-owned JSON API endpoint.
    """

    def on_create(self):
        super().on_create()

        self.mode = "chat"
        self.prompt = ""
        self.history = []
        self.open = False
        self.recommendations = []

        self.fab_bottom = f"calc({Theme.nav_bar_height} + {Theme.nav_bar_margin} * 2 + 12px)"

        self.output = Container(style={
            "display": "flex", "flex-direction": "column", "gap": "10px",
            "flex": "1", "min-height": "0", "overflow-y": "auto", "padding": "2px 2px 4px",
        }, klass="tz-hide-scroll")
        self.output.id = "ai-output"
        self.status_text = Paragraph(text="", style={"margin": "0"})
        self.status_text.id = "ai-status-text"
        self.status = FlexContainer(
            children=[Container(klass="tz-dot"), self.status_text],
            style={"align-self": "flex-start"},
        )
        self.status.id = "ai-status"
        self.status.props["data-state"] = "idle"

        self.panel = Container(style=self.panel_style())
        self.fab = self.build_fab()
        self.panel.add_children(self.build_panel_children())

        self.add_children([self.panel, self.fab])
        self.show_empty()

    # Layout
    def build_fab(self) -> Button:
        fab = Button(klass="tz-press", style={
            "display": "flex", "align-items": "center", "justify-content": "center",
            "position": "fixed", "right": Theme.screen_padding_x, "bottom": self.fab_bottom,
            "z-index": "55", "width": Theme.ai_fab_size, "height": Theme.ai_fab_size,
            "border": "none", "border-radius": "50%", "cursor": "pointer",
            "background": Theme.accent_gradient, "box-shadow": Theme.float_shadow,
        })
        fab.id = "ai-fab"
        fab.props["aria-label"] = "Open AI assistant"
        fab.add_child(self.fab_icon())
        fab.bind("click", self.on_toggle, update_targets=[self.panel, fab], update_self=False)
        return fab

    def fab_icon(self) -> Icon:
        return Icon(
            klass="bi bi-chevron-down" if self.open else "bi bi-stars",
            style={"font-size": "1.5rem", "color": "#fff"},
        )

    def panel_style(self) -> dict:
        return {
            "display": "flex" if self.open else "none",
            "flex-direction": "column", "gap": "10px",
            "position": "fixed", "z-index": "50",
            "left": Theme.screen_padding_x, "right": Theme.screen_padding_x,
            "bottom": f"calc({self.fab_bottom} + {Theme.ai_fab_size} + 10px)",
            "max-width": "420px", "margin-left": "auto",
            "height": "min(520px, 62vh)", "padding": "14px",
            "background": Theme.glass_bg_color,
            "backdrop-filter": Theme.glass_blur, "-webkit-backdrop-filter": Theme.glass_blur,
            "border": "1px solid rgba(255,255,255,0.7)",
            "border-radius": "28px",
            "box-shadow": "0 24px 60px rgba(15, 23, 42, 0.22), 0 0 0 1px rgba(124,92,250,0.08)",
            "animation": "tz-pop .22s cubic-bezier(.2,.8,.2,1)",
        }

    def build_panel_children(self) -> list:
        orb = FlexContainer(style={
            "display": "flex", "align-items": "center", "justify-content": "center",
            "width": "34px", "height": "34px", "border-radius": "12px",
            "background": Theme.accent_gradient,
        }, children=[Icon(klass="bi bi-stars", style={"font-size": "1rem", "color": "#fff"})])

        header = FlexContainer(style={
            "display": "flex", "align-items": "center", "gap": "10px",
        }, children=[
            orb,
            Heading(type="h2", text="Trip assistant", style={
                "margin": "0", "font-size": "1.02rem", "font-weight": "800",
                "letter-spacing": "-0.02em", "flex": "1"}),
        ])

        self.mode_buttons = FlexContainer(style={
            "display": "flex", "gap": "4px", "padding": "4px",
            "background": "rgba(15,23,42,0.05)", "border-radius": "999px",
        })
        self.mode_buttons.add_children([
            self.build_mode_button("Ask", "chat"),
            self.build_mode_button("Recommend", "recommendations"),
        ])

        self.prompt_input = Input(
            type="text", name="ai-prompt", maxlength=2000,
            placeholder="Ask anything about Zimbabwe…",
            style={
                "flex": "1", "min-width": "0", "border": "none", "outline": "none",
                "box-shadow": "none", "background": "transparent",
                "font-size": "0.97rem", "color": Theme.text_primary_color, "padding": "0 6px",
            },
        )
        self.prompt_input.bind("input", self.on_input, update_self=False)

        send = Button(klass="tz-press", style={
            "display": "flex", "align-items": "center", "justify-content": "center",
            "flex": "0 0 auto", "width": "38px", "height": "38px", "border": "none",
            "border-radius": "50%", "cursor": "pointer", "background": Theme.accent_gradient,
        }, children=[Icon(klass="bi bi-arrow-up", style={"font-size": "1.1rem", "color": "#fff"})])
        send.props["aria-label"] = "Send"
        send.bind(
            "click", self.on_submit,
            update_targets=[self.output, self.status, self.fab], update_self=False,
        )

        input_row = FlexContainer(style={
            "display": "flex", "align-items": "center", "gap": "6px",
            "padding": "5px 5px 5px 14px", "background": Theme.surface_color,
            "border": f"1px solid {Theme.surface_border_color}", "border-radius": "999px",
        }, children=[self.prompt_input, send])

        return [header, self.mode_buttons, self.output, self.status, input_row]

    def build_mode_button(self, label: str, mode: str) -> Button:
        button = Button(text=label, klass="tz-press", style=self.mode_button_style(mode == self.mode))
        button.bind(
            "click", self.build_mode_handler(mode),
            update_targets=[self.mode_buttons], update_self=False,
        )
        button.mode = mode
        return button

    def build_mode_handler(self, mode: str):
        async def on_click(component, event, value, ws):
            self.mode = mode
            for button in self.mode_buttons.children:
                button.style.update(self.mode_button_style(button.mode == self.mode))
        return on_click

    @staticmethod
    def mode_button_style(is_active: bool) -> dict:
        return {
            "flex": "1", "padding": Theme.ai_mode_button_padding, "border": "none",
            "border-radius": "999px", "cursor": "pointer",
            "background": Theme.surface_color if is_active else "transparent",
            "color": Theme.accent_color if is_active else Theme.text_secondary_color,
            "box-shadow": "0 1px 4px rgba(15,23,42,0.12)" if is_active else "none",
            "font-size": "0.84rem", "font-weight": "700",
        }

    # Events
    async def on_toggle(self, component, event, value, ws):
        self.open = not self.open
        self.panel.style.update(self.panel_style())
        self.fab.clear_children()
        self.fab.add_child(self.fab_icon())

    async def on_input(self, component, event, value, ws):
        self.prompt = str(value or "")[:2000]

    async def set_status(self, ws, state: str, text: str):
        """
        Updates the status pill on the server and pushes it to the browser
        immediately, so progress is visible while the request is in flight.
        """
        self.status.props["data-state"] = state
        self.status_text.text = text
        busy = "1" if state in ("thinking", "working") else "0"
        self.fab.props["data-busy"] = busy
        await ws.execute_js(
            "var s=document.getElementById('ai-status');"
            f"if(s)s.setAttribute('data-state',{json.dumps(state)});"
            f"var t=document.getElementById('ai-status-text');if(t)t.textContent={json.dumps(text)};"
            f"var f=document.getElementById('ai-fab');if(f)f.setAttribute('data-busy','{busy}');"
        )

    async def on_submit(self, component, event, value, ws):
        await self.run(ws)

    async def run(self, ws):
        """
        Calls the AI service, reporting each stage through the status pill.
        """
        prompt = self.prompt.strip()
        if not prompt:
            await self.set_status(ws, "error", "Type a question or a few interests first")
            return
        if not ai_service.is_configured():
            await self.set_status(ws, "error", "AI isn't configured yet")
            self.show_message(NOT_CONFIGURED)
            return

        self.prompt = ""
        await self.set_input(ws, "")
        await ws.execute_js(
            "var o=document.getElementById('ai-output');"
            "if(o){o.querySelectorAll('.tz-empty').forEach(function(e){e.style.display='none'});}"
            "var u=document.getElementById('ai-live-user');"
            f"if(u){{u.textContent={json.dumps(prompt)};u.style.display='block';}}"
            "var l=document.getElementById('ai-live');if(l){l.textContent='';l.style.display='none';}"
            "if(o)o.scrollTop=o.scrollHeight;"
        )

        try:
            if self.mode == "recommendations":
                await self.set_status(ws, "thinking", "Understanding your interests…")
                await self.set_status(ws, "working", "Matching places in the catalog…")
                recommendations = await ai_service.recommend_destinations(prompt, 5)
                self.show_recommendations(recommendations)
                count = len(recommendations)
                await self.set_status(
                    ws, "done",
                    f"Found {count} place{'s' if count != 1 else ''} for you" if count
                    else "No close match found",
                )
                return

            await self.set_status(ws, "thinking", "Thinking…")
            answer = await self.stream_answer(ws, prompt)
        except (ai_service.AIConfigurationError, ai_service.AIServiceError) as error:
            if not isinstance(error, ai_service.AIConfigurationError):
                logger.warning("The AI assistant request failed: %s", error)
            await self.fail(ws, prompt, str(error))
            return
        except Exception:
            logger.exception("The AI assistant request failed unexpectedly.")
            await self.fail(ws, prompt, "Something went wrong — try again")
            return

        self.history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ])
        self.history = self.history[-10:]
        self.show_chat_history()
        await self.set_status(ws, "done", "Answered using the destination catalog")

    async def stream_answer(self, ws, prompt: str) -> str:
        """
        Streams the answer into the live bubble, batching browser updates.
        """
        parts, buffer, last_push, started = [], "", 0.0, False

        async for chunk in ai_service.stream_travel_answer(prompt, self.history[-10:]):
            if not started:
                started = True
                await self.set_status(ws, "working", "Writing your answer…")
                await ws.execute_js(
                    "var l=document.getElementById('ai-live');if(l){l.textContent='';l.style.display='block';}"
                )
            parts.append(chunk)
            buffer += chunk
            if time.monotonic() - last_push >= 0.06:
                await self.push_text(ws, buffer)
                buffer, last_push = "", time.monotonic()

        if buffer:
            await self.push_text(ws, buffer)

        answer = "".join(parts).strip()
        if not answer:
            raise ai_service.AIServiceError("The AI provider returned an empty response.")
        return answer

    async def push_text(self, ws, text: str):
        await ws.execute_js(
            "var l=document.getElementById('ai-live');if(l){l.textContent+="
            f"{json.dumps(text)};}}var o=document.getElementById('ai-output');"
            "if(o)o.scrollTop=o.scrollHeight;"
        )

    async def set_input(self, ws, text: str):
        await ws.execute_js(
            "var i=document.querySelector('input[name=\"ai-prompt\"]');"
            f"if(i)i.value={json.dumps(text)};"
        )

    async def fail(self, ws, prompt: str, message: str):
        """
        Reports an error and restores the prompt so it can be resent.
        """
        self.prompt = prompt
        await self.set_input(ws, prompt)
        await self.set_status(ws, "error", message)

    # Output rendering
    def bubble(self, text: str, is_assistant: bool) -> Paragraph:
        return Paragraph(text=text, style={
            "margin": "0", "padding": Theme.ai_message_padding, "line-height": "1.5",
            "max-width": "88%", "font-size": "0.92rem", "white-space": "pre-wrap",
            "align-self": "flex-start" if is_assistant else "flex-end",
            "border-radius": "18px 18px 18px 6px" if is_assistant else "18px 18px 6px 18px",
            "background": Theme.surface_color if is_assistant else Theme.accent_gradient,
            "color": Theme.text_primary_color if is_assistant else "#fff",
            "border": f"1px solid {Theme.surface_border_color}" if is_assistant else "none",
        })

    def append_live(self):
        """
        Appends hidden bubbles that the browser fills while an answer streams.
        """
        live_user = self.bubble("", False)
        live_user.id = "ai-live-user"
        live_user.style["display"] = "none"
        live_answer = self.bubble("", True)
        live_answer.id = "ai-live"
        live_answer.style["display"] = "none"
        self.output.add_children([live_user, live_answer])

    def show_empty(self):
        """
        Shows the greeting and tappable starter prompts.
        """
        self.output.clear_children()
        if not ai_service.is_configured():
            self.show_message(NOT_CONFIGURED)
            return

        self.output.add_child(Paragraph(
            text="Ask a question or tell me what you enjoy — I'll suggest places from the catalog.",
            klass="tz-empty",
            style={"margin": "0", "color": Theme.text_secondary_color, "line-height": "1.5", "font-size": "0.92rem"},
        ))
        for mode, text in SUGGESTIONS:
            chip = Button(text=text, klass="tz-press tz-empty", style={
                "align-self": "flex-start", "padding": "8px 14px", "cursor": "pointer",
                "border-radius": "999px", "border": f"1px solid {Theme.surface_border_color}",
                "background": Theme.accent_soft_gradient, "color": Theme.accent_color,
                "font-size": "0.85rem", "font-weight": "650",
            })
            chip.bind(
                "click", self.build_suggestion_handler(mode, text),
                update_targets=[self.output, self.status, self.fab, self.mode_buttons],
                update_self=False,
            )
            self.output.add_child(chip)
        self.append_live()

    def build_suggestion_handler(self, mode: str, text: str):
        async def on_click(component, event, value, ws):
            self.mode = mode
            for button in self.mode_buttons.children:
                button.style.update(self.mode_button_style(button.mode == self.mode))
            self.prompt = text
            await self.run(ws)
        return on_click

    def show_message(self, message: str):
        self.output.clear_children()
        self.output.add_child(self.bubble(message, True))
        self.append_live()

    def show_chat_history(self):
        self.output.clear_children()
        for message in self.history:
            self.output.add_child(self.bubble(message["content"], message["role"] == "assistant"))
        self.append_live()

    def show_recommendations(self, recommendations: list[dict]):
        self.output.clear_children()
        if not recommendations:
            self.show_message("I couldn't find a close match in the catalog. Try different interests.")
            return

        for destination in recommendations:
            icon = FlexContainer(style={
                "display": "flex", "align-items": "center", "justify-content": "center",
                "flex": "0 0 auto", "width": "38px", "height": "38px", "border-radius": "12px",
                "background": Theme.accent_soft_gradient,
            }, children=[Icon(klass="bi bi-geo-alt-fill", style={"color": Theme.accent_color})])
            text = FlexContainer(style={
                "display": "flex", "flex-direction": "column", "gap": "3px", "min-width": "0",
            }, children=[
                Heading(type="h3", text=destination["name"], style={
                    "margin": "0", "font-size": "0.98rem", "font-weight": "750"}),
                Paragraph(text=f'{destination["category"]} · {destination["location"]}', style={
                    "margin": "0", "color": Theme.text_tertiary_color, "font-size": "0.78rem"}),
                Paragraph(text=destination["reason"], style={
                    "margin": "2px 0 0", "line-height": "1.45", "font-size": "0.88rem",
                    "color": Theme.text_secondary_color}),
                Link(url=f'/destination?id={destination["destination_id"]}', text="View destination →", style={
                    "margin-top": "4px", "color": Theme.accent_color, "font-weight": "700",
                    "font-size": "0.85rem", "text-decoration": "none"}),
            ])
            self.output.add_child(FlexContainer(style={
                "display": "flex", "gap": "12px", "padding": "12px",
                "background": Theme.surface_color, "border-radius": "18px",
                "border": f"1px solid {Theme.surface_border_color}",
            }, children=[icon, text]))
        self.append_live()
