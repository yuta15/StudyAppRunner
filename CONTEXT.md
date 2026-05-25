# Project Context

このリポジトリでは、ブラウザから実行可能な学習環境を提供する勉強アプリの Runner 基盤を作る。

ユーザーは教材を読みながら、ブラウザ上の Terminal で Linux / CLI / ネットワーク検証環境を操作できる。  
知識を読むだけではなく、実際にコマンドを打って技術を学べるアプリを目指す。

Runner は、教材に紐づいたコンテナ環境を作成し、Web Terminal からその環境へ接続できるようにする。

MVP では Docker を使う。  
将来的には Kubernetes や AWS ECS など、別の実行基盤にも拡張できる構成を目指す。

## Tech Stack

Python, FastAPI, WebSocket, Docker, Docker Compose, Docker SDK for Python, asyncio, pty/tty, Pydantic, pytest, ruff, uv.

Optional: gRPC, Protocol Buffers, Kubernetes, AWS ECS.