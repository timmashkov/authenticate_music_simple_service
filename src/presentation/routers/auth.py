from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Request, Response

from application.use_cases.auth_use_cases import AuthenticateUserUseCase
from presentation.models.auth import LoginDataModel, LogoutResultModel


class AuthRouter:
    api_router = APIRouter(prefix="/auth", tags=["auth"])

    @staticmethod
    @api_router.post("/login")
    @inject
    async def login(
        data: LoginDataModel,
        auth_provider: FromDishka[AuthenticateUserUseCase],
        response: Response,
    ):
        return await auth_provider.execute_login(data.login, data.password, response)

    @staticmethod
    @api_router.post("/logout")
    @inject
    async def logout(
        auth_provider: FromDishka[AuthenticateUserUseCase],
        response: Response,
        request: Request,
    ):
        result = await auth_provider.execute_logout(response, request)
        if not result:
            return LogoutResultModel(status=True)
        raise HTTPException(status_code=400, detail="Logout failed")
