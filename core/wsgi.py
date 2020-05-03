"""
WSGI config for gettingstarted project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from core.app import app

os.environ.setdefault("FLASK_APP", "core.app")

if __name__ == '__main__':
    app.run()
