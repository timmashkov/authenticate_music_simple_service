import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI

from application.config import settings
from application.providers import ProvidersManager


class APIServer:
    def __init__(
        self,
        name: str,
        routers: list[APIRouter] | None = None,
        start_callbacks: list[Callable] | None = None,
        stop_callbacks: list[Callable] | None = None,
    ) -> None:
        self._init_logger()
        self.name = name
        self.container = ProvidersManager().make_container()
        self.app = FastAPI(
            title=name,
            lifespan=self._lifespan,
        )
        self._init_dishka()
        self.routers = routers or []
        self._init_routers()
        self.start_callbacks = start_callbacks or []
        self.stop_callbacks = stop_callbacks or []

    @staticmethod
    def _init_logger() -> None:
        logging.basicConfig(
            level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _init_dishka(self) -> None:
        if self.container:
            setup_dishka(app=self.app, container=self.container)
            logging.info("Dishka init successfully!")

    def _init_routers(self) -> None:
        for router in self.routers:
            self.app.include_router(router)
        logging.info("Routers init successfully!")

    @asynccontextmanager
    async def _lifespan(self, _app: FastAPI) -> AsyncGenerator:
        for callback in self.start_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        logging.info("Startup callbacks init successfully!")

        yield

        for callback in self.stop_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        else:
            await self.container.close()
        logging.info("Shutdown callbacks init successfully!")
