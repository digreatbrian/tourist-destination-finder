#!/usr/bin/env python
"""
Main py script for application creation and execution.
"""

from duck.app import App
import duck.native.components

from prefill_db import prefill_db

app = App(
    port=8000,
    addr="0.0.0.0",
    domain="localhost",
    events={"on_start": prefill_db},
)


if __name__ == "__main__":
    app.run()
