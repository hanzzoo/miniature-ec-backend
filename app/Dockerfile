FROM --platform=arm64 python:3.12-slim

# cryptographyビルドに必要なパッケージを追加
RUN apt-get update && apt-get install -y build-essential libssl-dev && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 作業ディレクトリ作成
WORKDIR /app

# 依存関係ファイルをコピー
COPY pyproject.toml .
COPY requirements.txt .

# 依存関係をインストール
RUN uv pip install --system --no-cache -r requirements.txt

# アプリケーションのコードをコピー
COPY . /app

# ポートを公開
EXPOSE 8000

# サーバー起動コマンド
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
