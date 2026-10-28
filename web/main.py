#!/usr/bin/env python
"""
Main py script for application creation and execution.
"""
import os

from duck.settings import SETTINGS

# Modify debug settings in place for fast deployment and testing
# DEPLOYMENT SETTINGS (Heroku compatible)
DEBUG = bool(os.getenv('DEBUG', True))
PORT = int(os.getenv("PORT") or 8000)
DOMAIN = os.getenv('DOMAIN') or "localhost"
SERVER_URL = os.getenv('SERVER_URL')

SETTINGS['DEBUG'] = DEBUG
SETTINGS['LOG_TO_FILE'] = 1 if DEBUG else 0
SETTINGS['EXTRA_HEADERS'] = {"cache-control": "no-cache"} if DEBUG else {}
SETTINGS['ALLOWED_HOSTS'] = [DOMAIN, f"*.{DOMAIN}"] if not DEBUG else ["*"]
SETTINGS['ASYNC_HANDLING'] = 1
SETTINGS['ASYNC_LOOP'] = "uvloop" if not DEBUG else "asyncio"

from duck.app import App
from prefill_db import prefill_db
from superuser import create_superuser


def on_start(*a, **k):
    create_superuser()
    prefill_db(*a, **k)
    

app = App(
    port=PORT,
    addr="0.0.0.0",
    domain=DOMAIN,
    workers=5,
    server_url=SERVER_URL,
    events={"on_start": on_start},
)


if __name__ == "__main__":
    app.run()
