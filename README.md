
## Docker Containerの起動
```bash
docker-compose up -d
```

## App Serverの起動
```bash
cd app && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

