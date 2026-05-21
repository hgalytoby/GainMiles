from pathlib import Path


def to_pascal_case(name: str) -> str:
    return "".join(word.capitalize() for word in name.replace("-", "_").split("_"))


def to_snake_case(name: str) -> str:
    return name.replace("-", "_").lower()


def singularize(name: str) -> str:
    if name.endswith("ies"):
        return name[:-3] + "y"

    if name.endswith("s"):
        return name[:-1]

    return name


def write_file(path: Path, content: str) -> None:
    if path.exists():
        print(f"SKIP exists: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"CREATE: {path}")


def ask_required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field is required.")


def update_router_init(init_file: Path, entity_module: str, version: str) -> None:
    import_line = f"from .{entity_module} import router as {entity_module}_router"
    include_line = f"router.include_router({entity_module}_router)"

    if not init_file.exists():
        content = f"""from fastapi import APIRouter

{import_line}

router = APIRouter(prefix="/{version}")

{include_line}
"""
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.write_text(content, encoding="utf-8")
        return

    content = init_file.read_text(encoding="utf-8")

    # 確保 APIRouter 帶有 prefix
    if "APIRouter()" in content:
        content = content.replace("APIRouter()", f'APIRouter(prefix="/{version}")')

    lines = content.splitlines()

    # 檢查是否已經導入與包含
    has_import = any(import_line in line for line in lines)
    has_include = any(include_line in line for line in lines)

    if has_import and has_include:
        init_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    # 解析行，尋找適合插入 import 與 include 的位置
    last_from_idx = -1
    last_include_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("from ."):
            last_from_idx = i
        if "include_router" in line:
            last_include_idx = i

    # 插入 import
    if not has_import:
        if last_from_idx != -1:
            lines.insert(last_from_idx + 1, import_line)
            if last_include_idx > last_from_idx:
                last_include_idx += 1
        else:
            insert_idx = 0
            for i, line in enumerate(lines):
                if "APIRouter" in line or line.strip() == "":
                    insert_idx = i
                    break
            lines.insert(insert_idx, import_line)
            if last_include_idx >= insert_idx:
                last_include_idx += 1

    # 插入 include
    if not has_include:
        if last_include_idx != -1:
            lines.insert(last_include_idx + 1, include_line)
        else:
            lines.append("")
            lines.append(include_line)

    init_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_api_router_init(init_file: Path, version: str) -> None:
    import_line = f"from .{version} import router as {version}_router"
    include_line = f"router.include_router({version}_router)"

    if not init_file.exists():
        content = f"""from fastapi import APIRouter

{import_line}

router = APIRouter(prefix="/api")

{include_line}
"""
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.write_text(content, encoding="utf-8")
        return

    content = init_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # 檢查是否已經導入與包含
    has_import = any(import_line in line for line in lines)
    has_include = any(include_line in line for line in lines)

    if has_import and has_include:
        return

    # 解析行，尋找適合插入 import 與 include 的位置
    last_from_idx = -1
    last_include_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("from ."):
            last_from_idx = i
        if "include_router" in line:
            last_include_idx = i

    # 插入 import
    if not has_import:
        if last_from_idx != -1:
            lines.insert(last_from_idx + 1, import_line)
            if last_include_idx > last_from_idx:
                last_include_idx += 1
        else:
            insert_idx = 0
            for i, line in enumerate(lines):
                if "APIRouter" in line or line.strip() == "":
                    insert_idx = i
                    break
            lines.insert(insert_idx, import_line)
            if last_include_idx >= insert_idx:
                last_include_idx += 1

    # 插入 include
    if not has_include:
        if last_include_idx != -1:
            lines.insert(last_include_idx + 1, include_line)
        else:
            lines.append("")
            lines.append(include_line)

    init_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_models_init(init_file: Path, entity_module: str, entity_class: str) -> None:
    import_line = f"from .{entity_module} import {entity_class}"
    all_entry = f'    "{entity_class}",'

    if not init_file.exists():
        content = f"""from .base import BaseSQL
{import_line}

__all__ = [
    "BaseSQL",
    "{entity_class}",
]
"""
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.write_text(content, encoding="utf-8")
        return

    content = init_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # 檢查是否已經導入
    has_import = any(import_line in line for line in lines)
    # 檢查是否已經在 __all__
    has_all = any(f'"{entity_class}"' in line or f"'{entity_class}'" in line for line in lines)

    if has_import and has_all:
        return

    # 插入 import
    if not has_import:
        last_from_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("from ."):
                last_from_idx = i
        if last_from_idx != -1:
            lines.insert(last_from_idx + 1, import_line)
        else:
            lines.insert(0, import_line)

    # 插入 __all__
    if not has_all:
        # 重新掃描以獲取正確的索引
        all_start_idx = -1
        for i, line in enumerate(lines):
            if "__all__ =" in line and "[" in line:
                all_start_idx = i
                break

        if all_start_idx != -1:
            # 尋找接下來的 ]
            insert_idx = -1
            for i in range(all_start_idx + 1, len(lines)):
                if "]" in lines[i]:
                    insert_idx = i
                    break
            if insert_idx != -1:
                lines.insert(insert_idx, all_entry)
            else:
                lines.insert(all_start_idx + 1, all_entry)
        else:
            lines.append("")
            lines.append("__all__ = [")
            lines.append(all_entry)
            lines.append("]")

    init_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
