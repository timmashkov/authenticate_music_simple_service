from dishka import Provider, Scope, provide

from application.config import settings
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.redis_adapter import RedisAdapter


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_db_adapter(self) -> DatabaseAdapter:
        return DatabaseAdapter(
            host=settings.POSTGRES.host,
            port=settings.POSTGRES.port,
            dialect=settings.POSTGRES.dialect,
            login=settings.POSTGRES.login,
            password=settings.POSTGRES.password,
            database=settings.POSTGRES.database,
            echo=settings.POSTGRES.echo,
        )

    @provide(scope=Scope.APP)
    def provide_redis(self) -> RedisAdapter:
        return RedisAdapter()
