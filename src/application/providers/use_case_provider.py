from dishka import Provider, Scope, provide

from application.use_cases import CommandUserUseCases, QueryUserUseCases
from infrastructure.database import UserReadRepository, UserWriteRepository


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_query_use_cases(
        self, user_repository: UserReadRepository
    ) -> QueryUserUseCases:
        return QueryUserUseCases(user_repository)

    @provide(scope=Scope.REQUEST)
    def provide_command_user_cases(
        self, user_repository: UserWriteRepository
    ) -> CommandUserUseCases:
        return CommandUserUseCases(user_repository)
