# md_test_case_to_excel

マークダウン形式で書いたテスト仕様書を Excel 形式に変換するためのツールです。マークダウンの編集機能と GitHub での差分管理を活用しながら、必要に応じて Excel 形式で共有できます。

![](attachments/excel-image.png)

## 環境要件

- Python 3.11 以上
- uv (Python パッケージマネージャー)
- 以下の Python パッケージ:
  - pandas 2.2.2
  - openpyxl 3.1.5
  - pydantic 2.9.1
  - pyyaml 6.0.2

## インストール手順

### 1. Python と uv のインストール

#### Python のインストール

まだ Python がインストールされていない場合は、[Python 公式サイト](https://www.python.org/downloads/)からインストールしてください。

#### uv のインストール

[uv](https://github.com/astral-sh/uv) は高速な Python パッケージマネージャーです。

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**または pip でインストール:**

```bash
pip install uv
```

### 2. md_test_case_to_excel のインストール

#### 方法 1: uv を使用してインストール（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/your-username/md_test_case_to_excel.git
cd md_test_case_to_excel

# 仮想環境を作成して依存関係をインストール
uv sync

# パッケージをインストール
uv pip install -e .
```

#### 方法 2: pip を使用してインストール

```bash
pip install md-test-case-to-excel
```

インストール後、コマンドが認識されない場合は、Python のスクリプトディレクトリがパスに追加されていない可能性があります。以下の方法で実行できます：

```bash
# コマンドが見つからない場合は、pythonモジュールとして直接実行
python3 -m md_test_case_to_excel.converter -f your_file.md --template
```

### 3. アンインストール方法

#### pip でインストールした場合

```bash
pip uninstall md-test-case-to-excel
```

#### ソースからインストールした場合

```bash
# インストールディレクトリに移動
cd path/to/md_test_case_to_excel

# アンインストール
pip uninstall md-test-case-to-excel

# もしくは以下のコマンドでも可能
python setup.py develop --uninstall
```

## 使い方

### テスト仕様書を作成する

以下の形式に従ってテスト仕様書を作成します:

```markdown
# テスト仕様書

## 大項目

### 中項目

#### [正常|異常|準正常] [OK|NG|未実施|--] テストケース名

1. 確認手順 1
2. 確認手順 2

- [ ] 想定動作 1
- [ ] 想定動作 2

* 備考内容
```

### Excel に変換する

#### 基本的な実行手順

1. **リポジトリをクローンまたはダウンロード**

   ```bash
   git clone https://github.com/your-username/md_test_case_to_excel.git
   cd md_test_case_to_excel
   ```

2. **依存関係をインストール**

   ```bash
   # uv を使用（推奨）
   uv sync

   # または pip を使用
   pip install -r requirements.txt
   ```

3. **Markdown ファイルを Excel に変換**

   ```bash
   # テンプレートを使用して変換（推奨）
   python3 converter.py -f example/sample.md --template

   # または、新規ファイルとして作成
   python3 converter.py -f example/sample.md
   ```

#### 実行方法の選択肢

**方法 1: リポジトリ直下の converter.py を使用（推奨）**

```bash
# テンプレートを使用して変換
python3 converter.py -f path/to/your/testspec.md --template

# 新規ファイルとして作成
python3 converter.py -f path/to/your/testspec.md
```

**方法 2: パッケージとしてインストール後**

```bash
# uv を使用してパッケージをインストール（推奨）
uv pip install -e .

# または pip を使用
pip install -e .

# md2excelコマンドを使用
md2excel -f path/to/your/testspec.md --template

# または、pythonモジュールとして実行
python -m md_test_case_to_excel.converter -f path/to/your/testspec.md --template
```

#### 実際の実行例

```bash
# サンプルファイルで試してみる
python3 converter.py -f example/sample.md --template

# 出力例:
# -------
#    number  ...                                        expectation
# 0   1-1-1  ...             ・アプリでエラーが表示されないこと\n画像が変更されていることを見るしんよー
# 1   1-2-1  ...  ・アプリでエラーが表示されないこと\n・アプリを再起動し、メイン画面でユーザ名が "a" と...
# ...
# [11 rows x 6 columns]
# -------
# テンプレートファイル /path/to/assets/単体・結合試験_テンプレート_md.xlsx を使用します。
# Done! The file is saved at `example/sample.xlsx` (シート: テスト仕様書).
```

## コマンドラインオプション

| オプション名    | 説明                                                        |
| :-------------- | :---------------------------------------------------------- |
| -f, --file      | 入力ファイルパス（**必須**）                                |
| -h, --help      | 引数のヘルプ表示                                            |
| --template      | テンプレート Excel ファイルを使用する場合に指定             |
| --test-type     | テストの種別（test:テスト仕様書、ut:単体試験、it:結合試験） |
| --ut            | 単体試験シートに出力する（--test-type ut のショートカット） |
| --it            | 結合試験シートに出力する（--test-type it のショートカット） |
| --no-auto-width | 列幅の自動調整を無効にする場合に指定                        |

## 応用例

### 効率的なワークフロー

1. **新規テスト仕様書の作成**:

   - テンプレートファイルから新規テスト仕様書を作成
   - マークダウン形式で作成・編集

2. **バージョン管理**:

   - Git を使用して変更履歴を管理
   - マークダウン形式のため、差分確認が容易

3. **Excel 出力と共有**:
   - レビューや提出が必要な場合は Excel 形式に変換
   - コマンドを実行するだけで最新内容を Excel に反映

### 既存 Excel ファイルの更新

既存の Excel ファイルがある場合、そのファイルに追記する形で更新できます。
Excel ファイル内の J 列以降のコメントや試験結果などのデータは自動的に保持されます。

```bash
# Markdownファイルを更新後、既存のExcelファイルに追記する
md2excel -f example/updated_sample.md
```

### シート選択機能

```bash
# 単体試験シートに書き込む
md2excel -f example/testcases.md --ut

# 結合試験シートに書き込む
md2excel -f example/testcases.md --it
```

## カスタマイズ

設定ファイル`config.yaml`を編集することで、様々なカスタマイズが可能です:

- フォント名や各シート名の変更
- 列幅や列のフォーマットの調整
- マークダウンの解析パターンの変更

```yaml
excel_settings:
  font_name: Meiryo UI
  sheet_name:
    summary: サマリー
    test: テスト仕様書
    ut: 単体試験
    it: 結合試験

columns:
  number:
    name: "NO"
    length: 6
    horizontal: "center"
    vertical: "center"
  # 他の設定は省略
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. Python 3.9 での型注釈エラー

**エラー**: `TypeError: Unable to evaluate type annotation 'str | None'`

**原因**: Python 3.9 では `str | None` の新しい型注釈構文がサポートされていません。

**解決方法**: Python 3.10 以上を使用するか、以下のコマンドで型注釈の互換性パッケージをインストール：

```bash
pip install typing-extensions
```

#### 2. テンプレートファイルが見つからない

**エラー**: `警告: テンプレートファイルが見つかりません`

**原因**: テンプレートファイルのパスが間違っているか、ファイルが存在しません。

**解決方法**:

- `assets/単体・結合試験_テンプレート_md.xlsx` ファイルが存在することを確認
- `--template` オプションを外して新規ファイルとして作成

#### 3. モジュールが見つからない

**エラー**: `ModuleNotFoundError: No module named 'md_test_case_to_excel'`

**原因**: パッケージがインストールされていないか、パスが正しくありません。

**解決方法**:

```bash
# リポジトリ直下のconverter.pyを使用（推奨）
python3 converter.py -f example/sample.md --template

# または、パッケージをインストール
pip install -e .
```

#### 4. Excel ファイルが更新できない

**エラー**: ファイルが他のアプリケーションで開かれている

**解決方法**: Excel ファイルを閉じてから再実行してください。

#### 5. 依存関係のインストールエラー

**エラー**: パッケージのインストールに失敗

**解決方法**:

```bash
# uv を使用（推奨）
uv sync

# または、最新のpipを使用
pip install --upgrade pip

# 依存関係を個別にインストール
pip install pandas>=2.2.0 openpyxl>=3.1.0 pydantic>=2.9.0 pyyaml>=6.0.0
```

### デバッグ方法

#### 詳細なエラー情報を表示

```bash
# より詳細なエラー情報を表示
python3 -v converter.py -f example/sample.md --template
```

#### パース結果の確認

実行時に表示される DataFrame の内容を確認して、Markdown の解析が正しく行われているかチェックできます。

## 謝辞

このツールは以下のオープンソースプロジェクトを参考にしています：

- マークダウン形式のテスト仕様書フォーマット
- Python での Excel ファイル操作の実装例

## 制限事項

- Excel ヘッダーは日本語のみ対応しています
