from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter.base.filter import BaseFilterModel, FilterDepends
from pydantic import BaseModel

from application.use_cases import CommandRoleUseCases, QueryRoleUseCases
from presentation.models.role import RoleFilter, RoleReadModel, RoleWriteModel


class RoleRouter:
    api_router: APIRouter = APIRouter(prefix="/roles", tags=["Role"])
    filters: type[BaseFilterModel]
    input_model: BaseModel = RoleWriteModel
    output_model: BaseModel = RoleReadModel

    @staticmethod
    @api_router.get("/{role_name}", response_model=output_model)
    @inject
    async def get_role_by_name(
        role_name: str,
        role_provider: FromDishka[QueryRoleUseCases],
    ):
        return await role_provider.execute_read_role(role_name)

    @staticmethod
    @api_router.get("/", response_model=list[output_model])
    @inject
    async def get_roles_list(
        role_provider: FromDishka[QueryRoleUseCases],
        filters: RoleFilter = FilterDepends(RoleFilter),
    ):
        return await role_provider.execute_read_roles(filters)

    @staticmethod
    @api_router.post("/", response_model=output_model)
    @inject
    async def create_role(
        role_data: input_model, role_provider: FromDishka[CommandRoleUseCases]
    ):
        return await role_provider.execute_create_role(**role_data.model_dump())

    @staticmethod
    @api_router.patch("/{role_uuid}", response_model=output_model)
    @inject
    async def update_role(
        role_uuid: UUID,
        role_data: RoleWriteModel,
        role_provider: FromDishka[CommandRoleUseCases],
    ):
        return await role_provider.execute_update_role(
            **role_data.model_dump(), uuid=role_uuid
        )

    @staticmethod
    @api_router.delete("/{role_uuid}", response_model=output_model)
    @inject
    async def delete_role(
        role_uuid: UUID, role_provider: FromDishka[CommandRoleUseCases]
    ):
        return await role_provider.execute_delete_role(role_id=role_uuid)
