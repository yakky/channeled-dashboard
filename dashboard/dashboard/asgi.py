"""
ASGI entrypoint file for default channel layer.

Points to the channel layer configured as "default" so you can point
ASGI applications at "multichat.asgi:channel_layer" as their channel layer.
"""

import os
from channels.asgi import get_channel_layer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
application = get_channel_layer()
