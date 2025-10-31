# ベースイメージ
FROM python:3.11

# 作業ディレクトリ
WORKDIR /bot

# 依存関係をコピーしてインストール
COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

# Botのコードをコピー
COPY . /bot

# コンテナ起動時に bot.py を実行
CMD ["python", "bot.py"]
