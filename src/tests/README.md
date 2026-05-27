# StudyAppRunner

## テストケース提示ルール

テストケースを出す指示の場合は、テスト関数の形で提示する。

その際、各テスト関数の Docstring に「何を確認するテストか」だけを記述し、テスト実装自体は記述しない。

## テスト実装ルール

- テスト関数には、検証対象の振る舞いと assertion を中心に記述する。
- fixture、factory、stub、mock の共通生成処理は、対象に最も近い `conftest.py` に書き出す。
- 複数テストで使い回す固定値は、対象に最も近い `parameters.py` に書き出す。
- `pytest.mark.parametrize` の値は、テストコードから観点が読めるようにテスト関数の近くへ直接書いてよい。
- 外部サービス、DB、Docker などに依存しないテストは `src/tests/unit` に配置する。
- 外部サービス、DB、Docker など実体に接続するテストは `src/tests/integration` に配置し、`pytest.mark.integration` を付ける。
- integration test は、必要な外部サービスや image が利用できない場合は `pytest.skip` で明示的に skip する。
- 各テスト関数の Docstring には「何を確認するテストか」だけを記述する。
