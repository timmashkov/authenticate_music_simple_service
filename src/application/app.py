from application.config import settings
from application.server import APIServer
from presentation.routers.user import UserRouter

auth_app = APIServer(
    name=settings.NAME,
    routers=[UserRouter().api_router],
    start_callbacks=[],
    stop_callbacks=[],
).app
