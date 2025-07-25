
## API一覧

### 商品一覧取得API
```bash
curl "http://localhost:8000/products" | jq
```

### 商品詳細取得API
```bash
curl "http://localhost:8000/products/550e8400-e29b-41d4-a716-446655440000" | jq
```

### ユーザー登録API
- ユーザー登録APIのレスポンスには `token`が含まれ、<br>ログインAPI /カートアイテム追加・更新・削除API / カートアイテム取得APIで利用する必要があります。（` -H "Authorization: Bearer <token>"`）
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
      "user_name": "your-name"
      "user_email": "your-email",
      "user_password": "your-password"
    }
  }'
```

### ログインAPI
- ログインAPIのレスポンスには、ユーザー登録APIで払い出される `token`ではなく、リフレッシュされた`token` が含まれます。<br> ログインAPIの実行後は リフレッシュされた`token`を利用し、HTTPHeaderに含めたリクエストを行う必要があります。
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
      "user_email": "your-email",
      "user_password": "your-password"
    }
  }'
```

### カートアイテム追加・更新・削除API

- カートアイテムの追加
```bash
curl -X POST http://localhost:8000/cart/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "products": [
      { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 1 },
      { "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 2 }
    ]
  }'
```
  - すでに商品がある場合、`quantity`を加算することで元の数量増加（更新）が可能

```diff
curl -X POST http://localhost:8000/cart/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "products": [
- { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 1 },
+ { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 2 }
      { "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 2 }
    ]
  }
```

- カートアイテムの削除
 - 削除したい商品を `quantity: 0` で指定
```diff
curl -X POST http://localhost:8000/cart/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "products": [
- { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 1 },
+ { "product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 0 }
      { "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 2 }
    ]
  }
```

### カートアイテム取得API
```bash
curl "http://localhost:8000/cart/items" -H "Authorization: Bearer <token>" | jq
```

### TODO: 購入API



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