from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter.base.filter import BaseFilterModel, FilterDepends
from pydantic import BaseModel

from application.use_cases import CommandPermissionUseCases, QueryPermissionUseCases
from presentation.models.permission import (
    PermissionFilter,
    PermissionReadModel,
    PermissionWriteModel,
)


class PermissionRouter:
    api_router: APIRouter = APIRouter(prefix="/permissions", tags=["Permission"])
    filters: type[BaseFilterModel]
    input_model: BaseModel = PermissionWriteModel
    output_model: BaseModel = PermissionReadModel

    @staticmethod
    @api_router.get("/{perm_uuid}", response_model=output_model)
    @inject
    async def get_perm_by_name(
        perm_uuid: UUID,
        perm_provider: FromDishka[QueryPermissionUseCases],
    ):
        return await perm_provider.execute_read_perm(perm_uuid)

    @staticmethod
    @api_router.get("/", response_model=list[output_model])
    @inject
    async def get_perms_list(
        perm_provider: FromDishka[QueryPermissionUseCases],
        filters: PermissionFilter = FilterDepends(PermissionFilter),
    ):
        return await perm_provider.execute_read_perms(filters)

    @staticmethod
    @api_router.post("/", response_model=output_model)
    @inject
    async def create_perm(
        role_data: input_model, perm_provider: FromDishka[CommandPermissionUseCases]
    ):
        return await perm_provider.execute_create_permission(**role_data.model_dump())

    @staticmethod
    @api_router.patch("/{perm_uuid}", response_model=output_model)
    @inject
    async def update_perm(
        perm_uuid: UUID,
        role_data: PermissionWriteModel,
        perm_provider: FromDishka[CommandPermissionUseCases],
    ):
        return await perm_provider.execute_update_permission(
            **role_data.model_dump(), uuid=perm_uuid
        )

    @staticmethod
    @api_router.delete("/{perm_uuid}", response_model=output_model)
    @inject
    async def delete_perm(
        perm_uuid: UUID, perm_provider: FromDishka[CommandPermissionUseCases]
    ):
        return await perm_provider.execute_delete_permission(role_id=perm_uuid)
