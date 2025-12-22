from dishka import Provider, Scope, provide

from application.use_cases import (
    CommandPermissionUseCases,
    CommandRoleUseCases,
    CommandUserUseCases,
    QueryPermissionUseCases,
    QueryRoleUseCases,
    QueryUserUseCases,
)
from application.use_cases.auth_use_cases import AuthenticateUserUseCase
from domain.services.auth_services import TokenProvider
from infrastructure.authenticate.cookie_manager import CookieManager
from infrastructure.authenticate.security_manager import SecurityManager
from infrastructure.authenticate.session_manager import SessionManager
from infrastructure.database import (
    PermissionReadRepository,
    PermissionWriteRepository,
    RoleReadRepository,
    RoleWriteRepository,
    UserReadRepository,
    UserWriteRepository,
)


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
    def provide_query_role_cases(
        self,
        role_repository: RoleReadRepository,
    ) -> QueryRoleUseCases:
        return QueryRoleUseCases(role_repository)

    @provide(scope=Scope.REQUEST)
    def provide_command_role_cases(
        self,
        role_repository: RoleWriteRepository,
    ) -> CommandRoleUseCases:
        return CommandRoleUseCases(role_repository)

    @provide(scope=Scope.REQUEST)
    def provide_query_perm_cases(
        self,
        perm_repository: PermissionReadRepository,
    ) -> QueryPermissionUseCases:
        return QueryPermissionUseCases(perm_repository)

    @provide(scope=Scope.REQUEST)
    def provide_command_perm_cases(
        self,
        perm_repository: PermissionWriteRepository,
    ) -> CommandPermissionUseCases:
        return CommandPermissionUseCases(perm_repository)

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
