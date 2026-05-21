from ..models.employee import EmployeeModel
from ..schemas.employee import EmployeeWebCreated, EmployeeWebRead


class EmployeeFactory:
    @classmethod
    def build_web_read(cls, obj: EmployeeModel) -> EmployeeWebRead:
        return EmployeeWebRead.model_validate(obj)

    @classmethod
    def build_web_read_items(cls, items: list[EmployeeModel]) -> list[EmployeeWebRead]:
        return [cls.build_web_read(obj=item) for item in items]

    @classmethod
    def build_wer_created(cls, obj: EmployeeModel) -> EmployeeWebCreated:
        return EmployeeWebCreated.model_validate(obj)
