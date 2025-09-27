# Markdown Test Case to Excel Converter

Markdown で書かれたテスト仕様書を Excel ファイルに変換する。

## 機能

- `conversion_target_data`ディレクトリ内の Markdown ファイルを一括で Excel に変換
- テスト種別に応じたシート出力（テスト仕様書、単体試験、結合試験）
- 列幅の自動調整
- 13 列の詳細なテストケース管理
- 日時付きファイル名で`results`ディレクトリに出力

## 使用方法

### 基本的な使用方法

```bash
# 一括変換（デフォルト）
uv run python -m src.converter

# 単体試験シートに変換
uv run python -m src.converter --ut

# 結合試験シートに変換
uv run python -m src.converter --it

# 列幅の自動調整を無効化
uv run python -m src.converter --no-auto-width

# 入力ディレクトリを指定
uv run python -m src.converter --input-dir ./test_files

# 出力ディレクトリを指定
uv run python -m src.converter --output-dir ./custom_output
```

## 出力される列

1. **NO** - テストケース番号
2. **大分類** - セクション名（## で始まる）
3. **中分類** - サブセクション名（### で始まる）
4. **小分類** - テストケース名（#### で始まる）
5. **試験内容** - ステップ（数字. で始まる）
6. **確認事項** - 期待結果（チェックボックス形式）
7. **試験実施者** - 新規追加
8. **試験日** - 新規追加
9. **試験ステータス** - 新規追加
10. **試験結果備考** - 新規追加
11. **再試験実施者** - 新規追加
12. **再試験ステータス** - 新規追加
13. **再試験結果備考** - 新規追加

## 必要な環境

- Python 3.8+
- uv

## インストール

```bash
# 依存関係のインストール
uv sync
```

## 設定

`config.yaml`で列の設定やシート名をカスタマイズできます。

## ライセンス

MIT License
