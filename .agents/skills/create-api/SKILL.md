---
name: create-api
description: create or extend api modules using a create_api scaffold workflow. use when the user asks to create a new api, api module, endpoint group, repository/service/factory/schema/model set, or mentions version, api_prefix, tag, db schema, model schema, constraints, or scaffold generation with a create_api script.
---

# Create API

## Purpose

Use this skill to create or extend API modules in a Python web project that uses a `create_api` scaffold workflow. The expected layered output commonly includes some or all of these files:

- `app/models/<entity>.py`
- `app/schemas/<entity>.py`
- `app/repositories/<entity>.py`
- `app/factories/<entity>.py`
- `app/routers/<version>/<entity>.py`
- `app/services/<entity>/service.py`
- `app/services/<entity>/validator.py`
- `app/services/<entity>/__init__.py`

Treat the target project's local scaffold command as the source of truth for creating initial files. Do not hard-code any project name.

## Bundled scaffold script

This skill includes the `create_api` scaffold script as a bundled asset:

```text
assets/create_api/
```

Treat the bundled script as the source of truth for scaffold generation. Do not ask the user to provide or remember an execution path for the scaffold script. The assistant should use the bundled asset automatically when the user asks to create an API.

Keep only the unpacked `assets/create_api/` directory in the skill; do not include a duplicate nested zip of the same script.

When executing against a target project filesystem, prepare the bundled script automatically before running it. The expected project-side location is `scripts/create_api/` because the script imports `scripts.create_api.*` and derives the project root from that package location. If the target project already contains `scripts/create_api/`, inspect it and prefer the newer or user-provided version instead of overwriting silently. If the target project does not contain it, copy the bundled `assets/create_api/` directory there before running the scaffold.

Do not show the execution path or scaffold command to the user unless execution is impossible in the current environment or the user explicitly asks for the command.

## Required interaction

When the user asks to create an API, collect these values before running the scaffold command:

1. `version`, for example `v1` or `v2`.
2. `api_prefix`, for example the plural API resource path the user wants.
3. `tag`, for example the router/OpenAPI tag label the user wants.
4. Whether they already have a desired database schema.
5. If they have a desired database schema, ask for its fields and validation/constraint rules unless they already provided them.

Ask only for missing information. Do not ask again for values already provided in the conversation.

## Workflow

### 1. Determine scaffold inputs

Normalize only when safe:

- Keep `version` exactly as the user gives it, such as `v1`.
- Keep `api_prefix` exactly as the user gives it for the router prefix.
- Keep `tag` exactly as the user gives it for router/OpenAPI tags.
- Infer the entity module from the scaffold script behavior after running it, or from the singular form of `api_prefix` when needed.

### 2. Ask about schema intent

Ask:

```text
有沒有已經想好的 db schema？如果有，請給欄位、型別、required/unique/index/default/限制條件。
```

If the user says no schema is planned yet, run the scaffold command with only `version`, `api_prefix`, and `tag`.

If the user gives a schema but not constraints, ask for constraints. Examples of constraints:

- required / nullable
- unique / index
- string length
- numeric range
- date format
- enum values
- default values
- relationship / foreign key
- business uniqueness rules

### 3. Run the bundled scaffold

Run the `create_api` scaffold using the bundled script and the collected `version`, `api_prefix`, and `tag`. Do not manually create all scaffold files before running the script. The script must create the initial model, schema, repository, factory, service, validator, error codes, and router files.

Operational rules:

- Do not ask the user for a scaffold script path.
- Do not require the user to type the scaffold command when the assistant has filesystem execution access.
- If the target project already has `scripts/create_api/`, use that local copy unless the bundled asset is explicitly newer or the user asks to replace it.
- If the target project does not have `scripts/create_api/`, copy the bundled `assets/create_api/` directory into `scripts/create_api/` first, then run it from the project root.
- If the environment cannot access the user's local filesystem, explain the limitation and tell the user that the bundled `create_api` script must be copied into the project before execution.

After scaffold execution, inspect which files were created before applying model/schema edits.

### 3.1 Do not run migrations automatically

Do not run Alembic revision generation or database upgrade commands automatically after creating or editing an API scaffold. The user may still need to review and change generated models, schemas, validators, factories, repositories, or services before creating a migration.

Never automatically run:

```bash
uv run alembic revision --autogenerate -m "..."
uv run alembic upgrade head
```

Only mention these commands as manual follow-up after the user confirms the generated API and database model are finalized.

### 4. Edit generated model when schema is provided

After the scaffold command succeeds, edit:

```text
app/models/<entity_module>.py
```

Follow these rules:

- Preserve the target project's existing SQLAlchemy base class and internal primary key convention by default.
- If the project uses a base model such as `BaseSQL` with `id`, `created_at`, and `updated_at`, do not redeclare those fields in entity models by default.
- If the user explicitly says an entity should not use one or more inherited `BaseSQL` fields, override the inherited field intentionally. For SQLAlchemy declarative models, the project allows patterns such as `id = None` followed by a custom primary key column.
- If the user explicitly asks for a custom primary key, remove/override the inherited `id` field and declare the custom primary key in that entity model.
- If the user explicitly asks to omit inherited timestamps, override those inherited timestamp fields intentionally as well, following the project's proven pattern.
- Do not replace an internal `id` primary key with business identifiers such as `external_id`, unless the user explicitly asks.
- Add business identifiers as normal columns with `unique=True` and/or `index=True` when required.
- Use SQLAlchemy 2 style `Mapped[...]` and `mapped_column(...)` when the project uses SQLAlchemy 2 style models.
- Use appropriate column types such as `String`, `Integer`, `Date`, `DateTime`, `Boolean`, `Enum`, `ForeignKey`, and `Numeric`.
- Use `nullable=False` for required fields.
- Use `String(max_length)` when a length limit is provided.
- Use DB constraints for rules that belong in the database, such as `unique=True`, `index=True`, `ForeignKey`, and table-level constraints.

Example model style:

```python
from datetime import date

from sqlalchemy import CheckConstraint, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseSQL


class EntityModel(BaseSQL):
    __tablename__ = "entities"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_entities_amount_positive"),
    )

    external_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
```

Example when the user explicitly wants to replace an inherited primary key from `BaseSQL`:

```python
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseSQL


class EntityModel(BaseSQL):
    __tablename__ = "entities"

    id = None
    custom_pk: Mapped[int] = mapped_column(Integer, primary_key=True)
```

### 5. Edit generated schema when schema is provided

After editing the model, edit:

```text
app/schemas/<entity_module>.py
```

Follow these rules:

- Preserve the target project's base schema imports and mixin conventions.
- If the project uses read mixins for `id`, `created_at`, or `updated_at`, use those mixins instead of repeating the fields.
- Pydantic validation is allowed in schemas, including `Field(...)` constraints, `@field_validator(...)`, `@model_validator(...)`, custom validation methods, and schema-level validation logic when it makes the generated API code clearer.
- Prefer simple `Field(...)` constraints for straightforward shape validation such as length, numeric range, pattern, defaults, descriptions, and examples.
- Put validations that need project-specific error codes, service/repository access, database lookups, or reusable business rules in `app/services/<entity_module>/validator.py` and add corresponding codes in `error_codes.py`.
- Keep create schemas required when a field must be provided by normal API calls.
- Keep update schemas partial, using `None` defaults and `exclude_unset=True` usage in service/repository.
- Use `EmailStr` for email-like values when the user wants schema-level email validation; otherwise use `str` and validate in the entity validator if project-specific error codes are needed.
- Use `date` when the project wants Pydantic to parse and type dates; use `str` when the user wants looser fake/test data or custom date error codes in the entity validator.
- For query schemas, simple defaults and descriptions are allowed, but do not add validation constraints beyond project conventions.

Example schema style:

```python
from datetime import date
from enum import StrEnum

from pydantic import Field

from .base import ApiPageQuery, ApiQuery, BaseModel, IdCreatedAtUpdatedAtMixin


class BaseEntity(BaseModel):
    external_id: str
    display_name: str
    contact_email: str
    category: str
    amount: int
    effective_date: date


class EntityCreate(BaseEntity):
    pass


class EntityUpdate(BaseModel):
    display_name: str | None = None
    contact_email: str | None = None
    category: str | None = None
    amount: int | None = None
    effective_date: date | None = None


class EntityRead(IdCreatedAtUpdatedAtMixin, BaseEntity):
    pass


class EntityWebRead(EntityRead):
    pass


class EntityOrderByEnum(StrEnum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class EntityApiQuery(ApiQuery):
    pass


class EntityApiPageQuery(EntityApiQuery, ApiPageQuery):
    order_by: EntityOrderByEnum | None = Field(default=None, description="排序")
```

### 5.1 Add validator rules when project-specific error codes are needed

When the user provides validation requirements that should produce project-specific error codes or require service/database context, implement them in:

```text
app/services/<entity_module>/validator.py
```

Use the entity validator for rules such as:

- required / non-empty string
- unique business key checks
- string length limits
- numeric range, such as positive integer
- email format
- date string format and valid calendar dates
- enum-like allowed values
- cross-field validation
- file-level validation, such as duplicate values inside one uploaded file

For each validation failure, raise the project's application/validator exception style and use a specific error code from the entity's `error_codes.py`. If the exact exception helper is unclear, follow the existing generated validator pattern and add TODO comments rather than inventing a different project-wide error system.

Example validator style:

```python
from datetime import datetime
import re

from ...models.entity import EntityModel
from ...schemas.entity import EntityCreate, EntityUpdate
from ...utils.base_validator import BaseValidator
from .error_codes import EntityErrorCode


class EntityValidator(BaseValidator):
    @classmethod
    def get_by_id(cls, obj: EntityModel | None):
        cls.db_exist(obj=obj)

    @classmethod
    def create(cls, create_item: EntityCreate):
        cls.validate_display_name(create_item.display_name)
        cls.validate_contact_email(create_item.contact_email)
        cls.validate_amount(create_item.amount)
        cls.validate_effective_date(create_item.effective_date)

    @classmethod
    def update(cls, update_item: EntityUpdate, obj: EntityModel | None):
        cls.db_exist(obj=obj)

        if update_item.display_name is not None:
            cls.validate_display_name(update_item.display_name)

        if update_item.contact_email is not None:
            cls.validate_contact_email(update_item.contact_email)

        if update_item.amount is not None:
            cls.validate_amount(update_item.amount)

        if update_item.effective_date is not None:
            cls.validate_effective_date(update_item.effective_date)

    @classmethod
    def delete(cls, obj: EntityModel | None):
        cls.db_exist(obj=obj)

    @classmethod
    def validate_display_name(cls, value: str):
        if not value or not value.strip():
            cls.raise_error(EntityErrorCode.ENTITY_DISPLAY_NAME_REQUIRED, "display_name is required")

        if len(value) > 50:
            cls.raise_error(EntityErrorCode.ENTITY_DISPLAY_NAME_TOO_LONG, "display_name is too long")

    @classmethod
    def validate_contact_email(cls, value: str):
        if not value or not value.strip():
            cls.raise_error(EntityErrorCode.ENTITY_CONTACT_EMAIL_REQUIRED, "contact_email is required")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            cls.raise_error(EntityErrorCode.ENTITY_CONTACT_EMAIL_INVALID, "contact_email is invalid")

    @classmethod
    def validate_amount(cls, value: int):
        if value <= 0:
            cls.raise_error(EntityErrorCode.ENTITY_AMOUNT_NOT_POSITIVE, "amount must be positive")

    @classmethod
    def validate_effective_date(cls, value):
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                cls.raise_error(EntityErrorCode.ENTITY_EFFECTIVE_DATE_INVALID, "effective_date is invalid")
```

Adjust the helper method names to match the target project's actual `BaseValidator` API.

### 5.2 Add validation error codes

When adding validator rules, also edit:

```text
app/services/<entity_module>/error_codes.py
```

Add one enum member for each distinct validation failure. Keep names entity-scoped and specific.

Example:

```python
from enum import StrEnum, auto


class EntityErrorCode(StrEnum):
    ENTITY_NOT_FOUND = auto()
    ENTITY_DISPLAY_NAME_REQUIRED = auto()
    ENTITY_DISPLAY_NAME_TOO_LONG = auto()
    ENTITY_CONTACT_EMAIL_REQUIRED = auto()
    ENTITY_CONTACT_EMAIL_INVALID = auto()
    ENTITY_AMOUNT_NOT_POSITIVE = auto()
    ENTITY_EFFECTIVE_DATE_INVALID = auto()
```

## Database model versus API schema and validator constraints

Pydantic schema validation is allowed, including `Field(...)` constraints and validator decorators. However, if a validation failure must return a project-specific error code, depend on database/service context, or be reused across create/update/import workflows, place that rule in the entity validator and add the matching error code.

Recommended split:

- Put simple input-shape validation in Pydantic schemas when useful.
- Put request/business validation that needs explicit error codes in `app/services/<entity_module>/validator.py`.
- Put one specific error code per validator failure in `app/services/<entity_module>/error_codes.py`.
- Keep Pydantic schemas focused on fields, optional update fields, read mixins, query defaults, serialization shape, and validation that is acceptable to run during schema construction.
- Keep database model constraints only for storage integrity and relational structure, such as `nullable=False`, `unique=True`, `UniqueConstraint`, `index=True`, `ForeignKey`, `String(length)`, and `CheckConstraint` when the user explicitly wants the database to enforce the invariant.
- Use `nullable=False` for required persisted fields when the user confirms they are required in the database.
- Use `unique=True` or `UniqueConstraint` for values that must be unique across persisted rows. Also validate earlier in the validator if a user-facing error code is needed.
- Use indexes in the database model when the field is searched, filtered, joined, or must be unique.
- Use `String(length)` in the database model when the column storage should be capped, but enforce the user-facing length error in the entity validator.
- Use foreign keys and relationships in the database model.
- `@field_validator(...)`, `@model_validator(...)`, and custom Pydantic validator methods are allowed. Use the entity validator instead when the user wants project-specific error codes or looser fake/test data construction.
- Put file-level validation, such as "unique across the entire uploaded file," in a file/import validator, not as a primary key change. Add DB uniqueness only when the value must also be unique across persisted records.

Do not make business identifiers such as `external_id` the primary key unless the user explicitly asks. Keep the project's internal primary key convention.

### 6. Preserve target project conventions

Follow the target project's existing conventions unless the user explicitly changes them:

- Preserve its internal primary key strategy by default.
- Business IDs such as `external_id` are usually normal unique/indexed fields, not primary keys.
- If the user explicitly asks for a custom primary key or to omit inherited `BaseSQL` fields, override the inherited field in the generated model instead of arguing against it.
- Preserve its service, repository, factory, schema, model, router, and validator layer organization.
- Use repository/factory/service/validator layers when the project already has them, rather than putting business logic in routers.
- Use `204 No Content` delete endpoints when the user says no deleted object should be returned.
- Prefer `model_dump()` over deprecated Pydantic `.dict()` when editing Pydantic v2 code.

### 7. Verify after changes

After generating and editing files, inspect the generated paths and summarize:

- Files created by the scaffold script.
- Files edited after generation.
- Any assumptions made about schema or constraints.
- Any manual follow-up needed, such as router inclusion, Alembic migration, or project-specific validator implementation details.

When the user has reviewed and finalized the generated model/schema, remind them they can manually run:

```bash
uv run alembic revision --autogenerate -m "create <entity> table"
uv run alembic upgrade head
```
