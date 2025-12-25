from datetime import UTC, datetime, timedelta, timezone

from fastapi import Request, Response

from application.exceptions import EntityNotFoundError, Unauthorized
from domain.entities.auth import AuthenticationResult, AuthSession
from domain.repositories.user_repositories import UserABSReadRepository
from domain.services.auth_services import TokenProvider
from infrastructure.authenticate.cookie_manager import CookieManager
from infrastructure.authenticate.security_manager import SecurityManager
from infrastructure.authenticate.session_manager import SessionManager


class AuthenticateUserUseCase:
    def __init__(
        self,
        token_provider: TokenProvider,
        cookie_manager: CookieManager,
        user_repository: UserABSReadRepository,
        security_manager: SecurityManager,
        session_manager: SessionManager,
    ) -> None:
        self.token_provider = token_provider
        self.cookie_manager = cookie_manager
        self.user_repository = user_repository
        self.security_manager = security_manager
        self.session_manager = session_manager

    def _get_both_tokens(self, request: Request) -> tuple[str, AuthSession]:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            current_session = self.token_provider.verify_token(refresh_token)
            return refresh_token, current_session
        raise Unauthorized(None)

    async def execute_login(
        self,
        login: str,
        password: str,
        response: Response,
    ) -> AuthenticationResult:
        if user := await self.user_repository.get_user_by_login_data(
            login, self.security_manager.encode_pass(password, login)
        ):

            session = AuthSession(
                user_id=user.uuid,
                permissions=[],
                issued_at=datetime.now(timezone.utc),
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            )

            access_token = self.token_provider.create_access_token(session)
            refresh_token = self.token_provider.create_refresh_token(session)
            await self.session_manager.save_session(
                user.uuid, access_token, refresh_token
            )
            self.cookie_manager.set_tokens(response, access_token, refresh_token)

            return AuthenticationResult(
                user_id=user.uuid,
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=3600,
            )

        raise EntityNotFoundError(login)

    async def execute_logout(
        self,
        response: Response,
        request: Request,
    ) -> None:
        refresh_token ,current_session = self._get_both_tokens(request)
        if user := await self.user_repository.get_by_id(current_session.user_id):
            self.cookie_manager.clear_tokens(response)
            await self.session_manager.delete_session(user.uuid)
            return await self.session_manager.get_session(user.uuid)
        raise EntityNotFoundError(current_session.user_id)

    async def execute_refresh_tokens(
            self,
            response: Response,
            request: Request,
    ) -> AuthenticationResult:
        refresh_token ,current_session = self._get_both_tokens(request)
        if all((refresh_token, current_session)):
            new_access_toke, new_refresh_toke = self.token_provider.refresh_tokens(refresh_token)
            await self.session_manager.save_session(
                current_session.user_id, new_access_toke, new_refresh_toke
            )
            self.cookie_manager.set_tokens(response, new_access_toke, new_refresh_toke)
            print(current_session)
            return AuthenticationResult(
                user_id=current_session.user_id,
                access_token=new_access_toke,
                refresh_token=new_refresh_toke,
                token_type="bearer",
                expires_in=3600,
            )
        raise Unauthorized

    async def execute_check_auth(self, request: Request) -> AuthenticationResult:
        refresh_token, current_session = self._get_both_tokens(request)
        if user := await self.user_repository.get_by_id(current_session.user_id):
            return AuthenticationResult(
                user_id=user.uuid,
                access_token=request.get("access_token"),
                refresh_token=current_session.refresh_token,
                token_type="bearer",
                expires_in=3600,
                time_left_for_token=current_session.time_until_expiry()
            )
        raise Unauthorized(None)
