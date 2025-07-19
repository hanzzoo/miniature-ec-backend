
## Docker Containerの起動
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## App Serverの起動
```bash
cd app && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


## 動作確認

- 商品一覧取得API
```bash
curl -i http://localhost:8000/products
```

- 商品詳細取得API
```bash
curl -i http://localhost:8000/products/550e8400-e29b-41d4-a716-446655440000
```

- カート追加API
```bash
curl -X POST http://localhost:8000/add_to_cart \
  -H "Content-Type: application/json" \
  -d '["550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001"]'
```