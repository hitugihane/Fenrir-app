FROM python:3.9  

# 環境変数
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリの作成
WORKDIR /code

# 依存関係ファイルのコピーとインストール
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# プロジェクトファイルのコピー
COPY . /code/
