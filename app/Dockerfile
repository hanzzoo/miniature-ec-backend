FROM --platform=arm64 python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 作業ディレクトリ作成
WORKDIR /app

# 依存関係ファイルをコピー
COPY pyproject.toml .

# 依存関係をインストール
RUN uv pip install --system --no-cache fastapi[standard]

# アプリケーションのコードをコピー
COPY app/ .

# ポートを公開
EXPOSE 8000

# サーバー起動コマンド
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
