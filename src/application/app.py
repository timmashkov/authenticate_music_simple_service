from application.config import settings
from application.server import APIServer
from presentation.routers import AuthRouter, UserRouter

auth_app = APIServer(
    name=settings.NAME,
    routers=[UserRouter().api_router, AuthRouter().api_router],
    start_callbacks=[],
    stop_callbacks=[],
).app
