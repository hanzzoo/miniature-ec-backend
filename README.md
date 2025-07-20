
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

### 商品一覧取得API
```bash
curl -i http://localhost:8000/products
```

### 商品詳細取得API
```bash
curl -i http://localhost:8000/products/550e8400-e29b-41d4-a716-446655440000
```

### カートアイテム追加・削除API

- カートアイテムの追加
 - すでに商品がある場合、`quantity`を加算することで元の数量増加（更新）が可能
```bash
curl -X POST http://localhost:8000/add_to_cart \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 1 },
      { "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 2 }
    ]
  }
```

- カートアイテムの削除
 - 削除したい商品を `quantity: 0` で指定
```bash
curl -X POST http://localhost:8000/add_to_cart \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 1 },
      { "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 0 }
    ]
  }
```