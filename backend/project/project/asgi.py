# backend/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Main application
application = ProtocolTypeRouter({
    # Handles traditional HTTP requests
    "http": get_asgi_application(),

    # Will handle WebSocket connections
    # We'll define URLRouter later
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Example: path('ws/highlight/...')
            # We’ll add actual routes soon
        ])
    ),
})