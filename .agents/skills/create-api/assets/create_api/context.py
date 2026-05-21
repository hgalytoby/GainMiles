from dataclasses import dataclass


@dataclass(frozen=True)
class CreateApiContext:
    version: str
    api_prefix: str
    tag: str
    entity_name: str
    entity_module: str
    entity_class: str
