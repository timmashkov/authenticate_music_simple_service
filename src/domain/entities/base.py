from dataclasses import asdict, dataclass, fields
from datetime import datetime
from typing import Any, Dict, Type, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class BaseDomainEntity:
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    data: dict

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_orm(cls: Type[T], orm_model) -> T:
        class_fields = {f.name: f for f in fields(cls)}

        entity_data = {}

        for field_name, field_info in class_fields.items():
            if hasattr(orm_model, field_name):
                value = getattr(orm_model, field_name)
                entity_data[field_name] = value
            elif hasattr(field_info, "default"):
                entity_data[field_name] = field_info.default
            elif hasattr(field_info, "default_factory"):
                entity_data[field_name] = field_info.default_factory()

        return cls(**entity_data)
