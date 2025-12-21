from dishka import Provider, Scope, provide

from application.config import settings
from domain.services.auth_services import TokenProvider
from infrastructure.authenticate.cookie_manager import CookieManager
from infrastructure.authenticate.security_manager import SecurityManager
from infrastructure.authenticate.session_manager import SessionManager
from infrastructure.authenticate.token_manager import TokenManager
from infrastructure.database.redis_adapter import RedisAdapter


class AuthProvider(Provider):

    @provide(scope=Scope.REQUEST, provides=CookieManager)
    def provide_cookie_manager(self) -> CookieManager:
        return CookieManager()

    @provide(scope=Scope.REQUEST, provides=SecurityManager)
    def provide_security_manager(self) -> SecurityManager:
        return SecurityManager(
            iterations=settings.AUTH.iterations,
            hash_name=settings.AUTH.hash_name,
            formats=settings.AUTH.formats,
        )

    @provide(scope=Scope.REQUEST, provides=TokenProvider)
    def provide_token_provider(self) -> TokenManager:
        return TokenManager(
            secret_key=settings.AUTH.secret,
            algorithm=settings.AUTH.algorythm,
            access_token_expire_minutes=settings.AUTH.expiration,
            refresh_token_expire_days=settings.AUTH.expiration,
        )

    @provide(scope=Scope.APP, provides=SessionManager)
    def provide_session_manager(self, redis_adapter: RedisAdapter) -> SessionManager:
        return SessionManager(
            redis_client=redis_adapter, session_ttl=settings.AUTH.expiration
        )
