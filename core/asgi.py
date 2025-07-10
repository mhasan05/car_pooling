import os
from decouple import config

# ✅ Set settings module from .env before importing anything Django-related
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE', default='core.settings'))

# ✅ Setup Django before importing models/routing
import django
django.setup()

# ✅ Now you can import Django things
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# ✅ ASGI application definition
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
