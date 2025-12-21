from dishka import Provider, Scope, provide

from application.use_cases import CommandUserUseCases, QueryUserUseCases
from application.use_cases.auth_use_cases import AuthenticateUserUseCase
from domain.services.auth_services import TokenProvider
from infrastructure.authenticate.cookie_manager import CookieManager
from infrastructure.authenticate.security_manager import SecurityManager
from infrastructure.authenticate.session_manager import SessionManager
from infrastructure.database import UserReadRepository, UserWriteRepository


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_query_use_cases(
        self, user_repository: UserReadRepository
    ) -> QueryUserUseCases:
        return QueryUserUseCases(user_repository)

    @provide(scope=Scope.REQUEST)
    def provide_command_user_cases(
        self, user_repository: UserWriteRepository, security_manager: SecurityManager
    ) -> CommandUserUseCases:
        return CommandUserUseCases(user_repository, security_manager)

    @provide(scope=Scope.REQUEST)
    def provide_authenticate(
        self,
        user_repository: UserReadRepository,
        token_provider: TokenProvider,
        cookie_manager: CookieManager,
        security_manager: SecurityManager,
        session_manager: SessionManager,
    ) -> AuthenticateUserUseCase:
        return AuthenticateUserUseCase(
            token_provider,
            cookie_manager,
            user_repository,
            security_manager,
            session_manager,
        )
