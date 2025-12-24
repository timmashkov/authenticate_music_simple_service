from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter.base.filter import BaseFilterModel, FilterDepends
from pydantic import BaseModel

from application.use_cases import CommandUserUseCases, QueryUserUseCases
from presentation.models.user import (
    UserFilter,
    UserReadModel,
    UserWriteModel,
    UserWritePartialModel,
)


class UserRouter:
    api_router: APIRouter = APIRouter(prefix="/users", tags=["User"])
    filters: type[BaseFilterModel]
    input_model: BaseModel = UserWriteModel
    output_model: BaseModel = UserReadModel

    @staticmethod
    @api_router.get("/{user_uuid}", response_model=output_model)
    @inject
    async def get_user_by_uuid(
        user_uuid: UUID, user_provider: FromDishka[QueryUserUseCases]
    ):
        return await user_provider.execute_read_user(user_uuid)

    @staticmethod
    @api_router.get("/{user_uuid}/roles", response_model=UserReadModel)
    @inject
    async def get_user_with_roles(
        user_uuid: UUID, user_provider: FromDishka[QueryUserUseCases]
    ):
        return await user_provider.execute_read_user_with_roles(user_uuid)

    @staticmethod
    @api_router.get("/", response_model=list[output_model])
    @inject
    async def get_users_list(
        user_provider: FromDishka[QueryUserUseCases],
        filters: UserFilter = FilterDepends(UserFilter),
    ):
        return await user_provider.execute_read_users(filters)

    @staticmethod
    @api_router.post("/", response_model=output_model)
    @inject
    async def create_user(
        user_data: input_model, user_provider: FromDishka[CommandUserUseCases]
    ):
        return await user_provider.execute_create_user(**user_data.model_dump())

    @staticmethod
    @api_router.patch("/{user_uuid}", response_model=output_model)
    @inject
    async def update_user(
        user_uuid: UUID,
        user_data: UserWritePartialModel,
        user_provider: FromDishka[CommandUserUseCases],
    ):
        return await user_provider.execute_update_user(
            **user_data.model_dump(), uuid=user_uuid
        )

    @staticmethod
    @api_router.delete("/{user_uuid}", response_model=output_model)
    @inject
    async def delete_user(
        user_uuid: UUID, user_provider: FromDishka[CommandUserUseCases]
    ):
        return await user_provider.execute_delete_user(user_id=user_uuid)
