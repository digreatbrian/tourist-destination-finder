#!/usr/bin/env python
"""
Main py script for application creation and execution.
"""

import os
import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

pythonpath = os.environ.get("PYTHONPATH", "").split(os.pathsep)
if project_root not in pythonpath:
    os.environ["PYTHONPATH"] = os.pathsep.join(
        [project_root, *(entry for entry in pythonpath if entry)]
    )

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.backend.django.duckapp.duckapp.settings",
)

if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

import django

django.setup()

from duck.app import App
import duck.native.components

app = App(port=8000, addr="0.0.0.0", domain="localhost")


if __name__ == "__main__":
    app.run()
