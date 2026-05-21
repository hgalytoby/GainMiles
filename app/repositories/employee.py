from ..models.employee import EmployeeModel
from .base import BaseRepository, OptionsType


class EmployeeRepository(BaseRepository[EmployeeModel]):
    @classmethod
    def get_model(cls) -> type[EmployeeModel]:
        return EmployeeModel

    async def get_by_employee_id(
        self,
        employee_id: str,
        options: OptionsType = None,
    ) -> EmployeeModel | None:
        stmt = self._build_query(
            filters=[self.model.employee_id == employee_id],
            options=options,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
