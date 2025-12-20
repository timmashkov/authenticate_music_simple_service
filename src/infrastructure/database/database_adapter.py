from sqlalchemy import AsyncAdaptedQueuePool, Pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DatabaseAdapter:
    def __init__(
        self,
        host: str,
        port: int,
        dialect: str,
        login: str,
        password: str,
        database: str,
        echo: bool,
        pool_class: Pool = AsyncAdaptedQueuePool,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
    ) -> None:
        self.dialect = dialect
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.echo = echo
        self.database = database
        self.pool_class = pool_class
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle

        self._engine = create_async_engine(
            url=self._db_url,
            echo=self.echo,
            **self.pool_config,
        )
        self._autocommit_session = self._engine.execution_options(
            isolation_level="AUTOCOMMIT",
        )
        self._transactional_session = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )
        self._autocommit_session = async_sessionmaker(self._autocommit_session)

    @property
    def _db_url(self) -> str:
        return f"postgresql+{self.dialect}://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def pool_config(self) -> dict[str:int]:
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "poolclass": self.pool_class,
        }

    @property
    def transactional_session(self) -> async_sessionmaker[AsyncSession]:
        return self._transactional_session

    @property
    def autocommit_session(self) -> async_sessionmaker[AsyncSession]:
        return self._autocommit_session
