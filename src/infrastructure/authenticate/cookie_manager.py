from typing import Literal

from fastapi import Response


class CookieManager:
    def __init__(
        self,
        access_token_cookie_name: str = "access_token",
        refresh_token_cookie_name: str = "refresh_token",
        http_only: bool = True,
        secure: bool = True,
        same_site: Literal["lax", "strict", "none"] = "lax",
        domain: str = None,
    ) -> None:
        self.access_token_cookie_name = access_token_cookie_name
        self.refresh_token_cookie_name = refresh_token_cookie_name
        self.http_only = http_only
        self.secure = secure
        self.same_site = same_site
        self.domain = domain

    def set_tokens(
        self,
        response: Response,
        access_token: str,
        refresh_token: str,
        access_token_max_age: int = 3600,
        refresh_token_max_age: int = 2592000,
    ) -> None:
        response.set_cookie(
            key=self.access_token_cookie_name,
            value=access_token,
            max_age=access_token_max_age,
            httponly=self.http_only,
            secure=self.secure,
            samesite=self.same_site,
            domain=self.domain,
        )

        response.set_cookie(
            key=self.refresh_token_cookie_name,
            value=refresh_token,
            max_age=refresh_token_max_age,
            httponly=self.http_only,
            secure=self.secure,
            samesite=self.same_site,
            domain=self.domain,
        )

    def clear_tokens(self, response: Response) -> None:
        response.delete_cookie(self.access_token_cookie_name)
        response.delete_cookie(self.refresh_token_cookie_name)
