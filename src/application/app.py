from application.config import settings
from application.server import APIServer
from presentation.routers import AuthRouter, PermissionRouter, RoleRouter, UserRouter

auth_app = APIServer(
    name=settings.NAME,
    routers=[
        UserRouter().api_router,
        AuthRouter().api_router,
        RoleRouter().api_router,
        PermissionRouter().api_router,
    ],
    start_callbacks=[],
    stop_callbacks=[],
).app
