from dataclasses import dataclass


@dataclass(frozen=True)
class Destination:
    name: str
    location: str
    category: str
