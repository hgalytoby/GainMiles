from pathlib import Path
import subprocess
import sys

# 將專案根目錄加入 sys.path 以支援直接點擊執行時的絕對導入
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.create_api.context import CreateApiContext
from scripts.create_api.templates import (
    error_codes_template,
    factory_template,
    model_template,
    repository_template,
    router_template,
    schema_template,
    service_init_template,
    service_template,
    validator_template,
)
from scripts.create_api.utils import (
    ask_required,
    singularize,
    to_pascal_case,
    to_snake_case,
    update_api_router_init,
    update_models_init,
    update_router_init,
    write_file,
)

APP_DIR = Path(__file__).resolve().parents[2] / "app"


def main() -> None:
    print("=== Create API Interactive CLI ===")

    version_input = input("API Version (default: v1): ").strip()
    version = version_input if version_input else "v1"

    api_prefix = ask_required("API Prefix (e.g. users): ")
    tag = ask_required("API Tag (e.g. User): ")

    entity_name = singularize(api_prefix)
    entity_module = to_snake_case(entity_name)
    entity_class = to_pascal_case(entity_name)

    # 防呆檢查：如果該版本的 API 已經存在，則不允許覆蓋
    router_file = APP_DIR / "routers" / version / f"{entity_module}.py"
    if router_file.exists():
        print(
            f"ERROR: API '{entity_module}' already exists in version '{version}'. Overwriting is not allowed."
        )
        return

    ctx = CreateApiContext(
        version=version,
        api_prefix=api_prefix,
        tag=tag,
        entity_name=entity_name,
        entity_module=entity_module,
        entity_class=entity_class,
    )

    write_file(
        APP_DIR / "models" / f"{entity_module}.py",
        model_template(ctx),
    )

    update_models_init(
        APP_DIR / "models" / "__init__.py",
        entity_module=entity_module,
        entity_class=f"{entity_class}Model",
    )

    write_file(
        APP_DIR / "schemas" / f"{entity_module}.py",
        schema_template(ctx),
    )

    write_file(
        APP_DIR / "repositories" / f"{entity_module}.py",
        repository_template(ctx),
    )

    write_file(
        APP_DIR / "factories" / f"{entity_module}.py",
        factory_template(ctx),
    )

    write_file(
        APP_DIR / "services" / entity_module / "__init__.py",
        service_init_template(ctx),
    )

    write_file(
        APP_DIR / "services" / entity_module / "service.py",
        service_template(ctx),
    )

    write_file(
        APP_DIR / "services" / entity_module / "validator.py",
        validator_template(ctx),
    )

    write_file(
        APP_DIR / "services" / entity_module / "error_codes.py",
        error_codes_template(ctx),
    )

    write_file(
        APP_DIR / "routers" / version / f"{entity_module}.py",
        router_template(ctx),
    )

    # 自動註冊路由
    router_init_path = APP_DIR / "routers" / version / "__init__.py"
    update_router_init(router_init_path, entity_module, version)

    # 自動註冊版本路由器
    api_router_init_path = APP_DIR / "routers" / "__init__.py"
    update_api_router_init(api_router_init_path, version)

    # 執行 ruff 檢查與格式化
    print("Running ruff check & format...")
    subprocess.run("ruff check --fix && ruff format", shell=True, cwd=APP_DIR)


if __name__ == "__main__":
    main()
