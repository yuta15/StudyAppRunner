# StudyAppRunner

StudyAppRunner は、教材に紐づいた実行用コンテナを作成し、ブラウザ上の Web Terminal から接続できる学習環境 Runner です。

ユーザーが教材を読みながら Linux / CLI / ネットワーク検証環境を実際に操作し、知識だけでなく手を動かして技術を学べる状態を提供します。

アプリケーションコードは `src/app` 配下に、テストコードは `src/tests` 配下に配置します。アプリケーションコードは以下の層に分けて整理します。

- `endpoints`: 外部からの入出力を受け付ける層
- `applications`: ユースケースやアプリケーション固有の処理を扱う層
- `domain`: アプリケーションの中核となる概念やルールを扱う層
- `infra`: 外部サービス、永続化、フレームワーク依存の処理を扱う層

## Directory README

各ディレクトリの詳細は、それぞれの README を参照してください。

| Directory | README |
| --- | --- |
| `src/tests` | [src/tests/README.md](src/tests/README.md) |
| `src/app/endpoints` | [src/app/endpoints/README.md](src/app/endpoints/README.md) |
| `src/app/applications` | [src/app/applications/README.md](src/app/applications/README.md) |
| `src/app/domain` | [src/app/domain/README.md](src/app/domain/README.md) |
| `src/app/infra` | [src/app/infra/README.md](src/app/infra/README.md) |
| `src/tests/endpoints` | [src/tests/endpoints/README.md](src/tests/endpoints/README.md) |
| `src/tests/applications` | [src/tests/applications/README.md](src/tests/applications/README.md) |
| `src/tests/domain` | [src/tests/domain/README.md](src/tests/domain/README.md) |
| `src/tests/infra` | [src/tests/infra/README.md](src/tests/infra/README.md) |
