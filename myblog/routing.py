from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import blog.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            blog.routing.websocket_urlpatterns
        )
    ),
})


# from channels.routing import route
# from blog.consumers import ws_connect, ws_disconnect,ws_receive

# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.receive', ws_receive),
#     route('websocket.disconnect', ws_disconnect),
# ]