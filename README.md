### 後端 (Backend) - 使用 uv
1. **安裝依賴**：`uv sync`
2. **資料庫遷移**：`uv run alembic upgrade head`
3. **啟動伺服器**：`uv run fastapi dev app/main.py`


## 環境變數 (.env)
```env
# 資料庫連線 (Docker 部署時 Host 請設為 postgres)
SQL_URL=postgresql+asyncpg://user:password@postgres:5432/GainMiles
```

## 快速啟動 (Docker)
```bash
docker compose up -d --build
```

## 用到的 Command
```bash
fastapi dev app/main.py

alembic init migrations
alembic revision --autogenerate -m "init table"
alembic upgrade head

windos: ruff check --fix ; ruff format
other ruff check --fix && ruff format
```