"""
Contact channels for a destination.

Directions are always derived from the destination itself. Phone, email,
WhatsApp and website come from `CONTACT_OVERRIDES` (keyed by destination
name), falling back to `DEFAULT_WEBSITE`. Fill in real numbers there.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus

DEFAULT_WEBSITE = "https://www.zimbabwetourism.net"

# "Destination name": {"phone": "+263...", "email": "...", "whatsapp": "+263...", "website": "https://..."}
CONTACT_OVERRIDES: dict[str, dict[str, str]] = {}


@dataclass(frozen=True)
class ContactChannel:
    """
    One tappable way to reach a destination.
    """

    icon: str
    label: str
    detail: str
    url: str
    external: bool = False


def get_channels(name: str, location: str) -> list[ContactChannel]:
    """
    Returns the available contact channels for a destination.
    """
    info = CONTACT_OVERRIDES.get(name, {})
    channels: list[ContactChannel] = []

    if info.get("phone"):
        channels.append(ContactChannel(
            "bi-telephone-fill", "Call", info["phone"],
            f"tel:{info['phone'].replace(' ', '')}",
        ))
    if info.get("whatsapp"):
        digits = "".join(ch for ch in info["whatsapp"] if ch.isdigit())
        channels.append(ContactChannel(
            "bi-whatsapp", "WhatsApp", info["whatsapp"],
            f"https://wa.me/{digits}?text={quote_plus('Hi, I would like to enquire about ' + name)}",
            external=True,
        ))
    if info.get("email"):
        channels.append(ContactChannel(
            "bi-envelope-fill", "Email", info["email"],
            f"mailto:{info['email']}?subject={quote_plus('Enquiry: ' + name)}",
        ))

    website = info.get("website") or DEFAULT_WEBSITE
    channels.append(ContactChannel(
        "bi-globe2", "Website", website.replace("https://", "").rstrip("/"),
        website, external=True,
    ))
    channels.append(ContactChannel(
        "bi-sign-turn-right-fill", "Directions", location,
        f"https://www.google.com/maps/search/?api=1&query={quote_plus(name + ', ' + location + ', Zimbabwe')}",
        external=True,
    ))
    return channels
