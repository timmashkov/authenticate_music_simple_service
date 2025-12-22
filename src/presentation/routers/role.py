from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter.base.filter import BaseFilterModel, FilterDepends
from pydantic import BaseModel

from application.use_cases import CommandRoleUseCases, QueryUserUseCases
from presentation.models.role import (
    RoleFilter,
    RoleReadModel,
    RoleWriteModel,
)


class RoleRouter:
    api_router: APIRouter = APIRouter(prefix="/roles", tags=["Role"])
    filters: type[BaseFilterModel]
    input_model: BaseModel = RoleWriteModel
    output_model: BaseModel = RoleReadModel

    # @staticmethod
    # @api_router.get("/{role_name}", response_model=output_model)
    # @inject
    # async def get_role_by_name(
    #     role_name: str, role_provider,
    # ):
    #     return await role_provider.execute_read_user(user_uuid)
    #
    # @staticmethod
    # @api_router.get("/", response_model=list[output_model])
    # @inject
    # async def get_roles_list(
    #     user_provider: FromDishka[QueryUserUseCases],
    #     filters: RoleFilter = FilterDepends(RoleFilter),
    # ):
    #     return await user_provider.execute_read_users(filters)

    @staticmethod
    @api_router.post("/", response_model=output_model)
    @inject
    async def create_role(
        role_data: input_model, role_provider: FromDishka[CommandRoleUseCases]
    ):
        return await role_provider.execute_create_role(**role_data.model_dump())

    # @staticmethod
    # @api_router.patch("/{role_uuid}", response_model=output_model)
    # @inject
    # async def update_role(
    #     user_uuid: UUID,
    #     user_data: UserWritePartialModel,
    #     user_provider: FromDishka[CommandUserUseCases],
    # ):
    #     return await user_provider.execute_update_user(
    #         **user_data.model_dump(), uuid=user_uuid
    #     )
    #
    # @staticmethod
    # @api_router.delete("/{role_uuid}", response_model=output_model)
    # @inject
    # async def delete_role(
    #     user_uuid: UUID, user_provider: FromDishka[CommandUserUseCases]
    # ):
    #     return await user_provider.execute_delete_user(user_id=user_uuid)
