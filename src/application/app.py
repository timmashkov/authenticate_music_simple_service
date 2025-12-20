from application.server import APIServer
from application.config import settings

auth_app = APIServer(
    name=settings.NAME,
    routers=[],
    start_callbacks=[],
    stop_callbacks=[],
).app
