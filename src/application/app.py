from application.config import settings
from application.server import APIServer

auth_app = APIServer(
    name=settings.NAME,
    routers=[],
    start_callbacks=[],
    stop_callbacks=[],
).app
