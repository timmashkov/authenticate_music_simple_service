from dishka import Provider, Scope, provide

from infrastructure.database import UserReadRepository, UserWriteRepository, RoleReadRepository, RoleWriteRepository
from infrastructure.database.database_adapter import DatabaseAdapter


class UserRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_read_repository(
        self, database_adapter: DatabaseAdapter
    ) -> UserReadRepository:
        return UserReadRepository(database_adapter)

    @provide(scope=Scope.REQUEST)
    def provide_user_write_repository(
        self, database_adapter: DatabaseAdapter
    ) -> UserWriteRepository:
        return UserWriteRepository(database_adapter)

    @provide(scope=Scope.REQUEST)
    def provide_role_read_repository(
            self, database_adapter: DatabaseAdapter
    ) -> RoleReadRepository:
        return RoleReadRepository(database_adapter)

    @provide(scope=Scope.REQUEST)
    def provide_role_write_repository(
            self, database_adapter: DatabaseAdapter
    ) -> RoleWriteRepository:
        return RoleWriteRepository(database_adapter)
