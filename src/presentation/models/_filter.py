from typing import Any, ItemsView

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select


class _APIFilter(Filter):
    def sort(self, query: select) -> select:
        for field_name, _ in self._filter_fields_to_items:
            field_value = getattr(self, field_name)
            if isinstance(field_value, Filter):
                query = field_value.sort(query)
        return super().sort(query)

    @property
    def _filter_fields_to_items(self) -> ItemsView[str, Any]:
        fields = self.model_dump(exclude_none=True)
        fields.pop(self.Constants.ordering_field_name, None)
        return fields.items()
